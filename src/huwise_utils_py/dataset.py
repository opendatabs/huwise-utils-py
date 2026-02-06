"""HuwiseDataset class for dataset operations.

This module provides a dataclass-based interface for interacting with
Huwise datasets, supporting method chaining and dependency injection.
"""

import time
from dataclasses import dataclass, field
from typing import Any, Self

from huwise_utils_py.config import HuwiseConfig
from huwise_utils_py.http import HttpClient
from huwise_utils_py.logger import get_logger

logger = get_logger(__name__)


@dataclass
class HuwiseDataset:
    """Represents a Huwise dataset with metadata operations.

    Provides a fluent interface for reading and modifying dataset metadata.
    Supports method chaining for convenient batch updates.

    Attributes:
        uid: The unique string identifier of the dataset.
        config: Optional HuwiseConfig (uses default if not provided).

    Example:
        >>> # Create and modify a dataset
        >>> dataset = HuwiseDataset(uid="da_abc123")
        >>> dataset.set_title("New Title", publish=False) \\
        ...        .set_description("Description") \\
        ...        .publish()

        >>> # Create from numeric ID
        >>> dataset = HuwiseDataset.from_id("12345")
        >>> title = dataset.get_title()
    """

    uid: str
    config: HuwiseConfig = field(default_factory=HuwiseConfig.from_env)
    _client: HttpClient = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """Initialize the HTTP client after dataclass initialization."""
        self._client = HttpClient(self.config)

    @classmethod
    def from_id(cls, dataset_id: str, config: HuwiseConfig | None = None) -> Self:
        """Create a dataset instance from a numeric dataset ID.

        Args:
            dataset_id: The numeric identifier of the dataset.
            config: Optional HuwiseConfig instance.

        Returns:
            HuwiseDataset instance with resolved UID.

        Raises:
            IndexError: If no dataset is found with the given ID.
        """
        config = config or HuwiseConfig.from_env()
        client = HttpClient(config)

        response = client.get("/datasets/", params={"dataset_id": dataset_id})
        uid: str = response.json()["results"][0]["uid"]

        logger.info("Resolved dataset ID to UID", dataset_id=dataset_id, uid=uid)
        return cls(uid=uid, config=config)

    def _wait_for_idle(self) -> None:
        """Wait until the dataset status is idle."""
        while True:
            response = self._client.get(f"/datasets/{self.uid}/status")
            status = response.json()["status"]
            if status == "idle":
                break
            logger.debug("Waiting for dataset to be idle", uid=self.uid, status=status)
            time.sleep(3)

    def _get_metadata_value(self, template: str, field_name: str) -> Any | None:
        """Get a specific metadata field value.

        Args:
            template: Metadata template name (e.g., "default").
            field_name: Field name within the template.

        Returns:
            The field value or None if not set.
        """
        metadata = self.get_metadata()
        return metadata.get(template, {}).get(field_name, {}).get("value")

    def _set_metadata_value(
        self, template: str, field_name: str, value: Any, *, publish: bool = True
    ) -> Self:
        """Set a specific metadata field value.

        Args:
            template: Metadata template name (e.g., "default").
            field_name: Field name within the template.
            value: The value to set.
            publish: Whether to publish after updating.

        Returns:
            Self for method chaining.
        """
        response = self._client.get(f"/datasets/{self.uid}/metadata/")
        metadata: dict[str, Any] = response.json()

        if template not in metadata:
            metadata[template] = {}
        if field_name not in metadata[template]:
            metadata[template][field_name] = {}

        metadata[template][field_name]["value"] = value

        self._wait_for_idle()
        self._client.put(f"/datasets/{self.uid}/metadata/", json=metadata)

        logger.info(
            "Updated metadata field",
            uid=self.uid,
            template=template,
            field=field_name,
        )

        if publish:
            self.publish()

        return self

    # =========================================================================
    # Getters
    # =========================================================================

    def get_metadata(self) -> dict[str, Any]:
        """Retrieve the full metadata of the dataset.

        Returns:
            Dictionary containing all metadata templates and fields.
        """
        response = self._client.get(f"/datasets/{self.uid}")
        metadata: dict[str, Any] = response.json()["metadata"]
        logger.debug("Retrieved metadata", uid=self.uid, templates=list(metadata.keys()))
        return metadata

    def get_title(self) -> str | None:
        """Retrieve the dataset title.

        Returns:
            The dataset title or None if not set.
        """
        return self._get_metadata_value("default", "title")

    def get_description(self) -> str | None:
        """Retrieve the dataset description.

        Returns:
            The dataset description or None if not set.
        """
        return self._get_metadata_value("default", "description")

    def get_keywords(self) -> list[str] | None:
        """Retrieve the dataset keywords.

        Returns:
            List of keywords or None if not set.
        """
        return self._get_metadata_value("default", "keyword")

    def get_language(self) -> str | None:
        """Retrieve the dataset language.

        Returns:
            The language code or None if not set.
        """
        return self._get_metadata_value("default", "language")

    def get_publisher(self) -> str | None:
        """Retrieve the dataset publisher.

        Returns:
            The publisher name or None if not set.
        """
        return self._get_metadata_value("default", "publisher")

    def get_theme(self) -> str | None:
        """Retrieve the dataset theme.

        Returns:
            The theme ID or None if not set.
        """
        return self._get_metadata_value("default", "theme_id")

    def get_license(self) -> str | None:
        """Retrieve the dataset license.

        Returns:
            The license ID or None if not set.
        """
        return self._get_metadata_value("default", "license_id")

    def get_custom_view(self) -> dict[str, Any] | None:
        """Retrieve the dataset custom view configuration.

        Returns:
            Custom view dictionary or None if not set.
        """
        return self._get_metadata_value("visualization", "custom_view")

    # =========================================================================
    # Setters (return Self for method chaining)
    # =========================================================================

    def set_title(self, title: str, *, publish: bool = True) -> Self:
        """Set the dataset title.

        Args:
            title: The new title for the dataset.
            publish: Whether to publish after updating.

        Returns:
            Self for method chaining.
        """
        return self._set_metadata_value("default", "title", title, publish=publish)

    def set_description(self, description: str, *, publish: bool = True) -> Self:
        """Set the dataset description.

        Args:
            description: The new description for the dataset.
            publish: Whether to publish after updating.

        Returns:
            Self for method chaining.
        """
        return self._set_metadata_value("default", "description", description, publish=publish)

    def set_keywords(self, keywords: list[str], *, publish: bool = True) -> Self:
        """Set the dataset keywords.

        Args:
            keywords: List of keywords for the dataset.
            publish: Whether to publish after updating.

        Returns:
            Self for method chaining.
        """
        return self._set_metadata_value("default", "keyword", keywords, publish=publish)

    def set_language(self, language: str, *, publish: bool = True) -> Self:
        """Set the dataset language.

        Args:
            language: Language code (e.g., "en", "de", "fr").
            publish: Whether to publish after updating.

        Returns:
            Self for method chaining.
        """
        return self._set_metadata_value("default", "language", language, publish=publish)

    def set_publisher(self, publisher: str, *, publish: bool = True) -> Self:
        """Set the dataset publisher.

        Args:
            publisher: Publisher name.
            publish: Whether to publish after updating.

        Returns:
            Self for method chaining.
        """
        return self._set_metadata_value("default", "publisher", publisher, publish=publish)

    def set_theme(self, theme_id: str, *, publish: bool = True) -> Self:
        """Set the dataset theme.

        Args:
            theme_id: Theme identifier.
            publish: Whether to publish after updating.

        Returns:
            Self for method chaining.
        """
        return self._set_metadata_value("default", "theme_id", theme_id, publish=publish)

    def set_license(self, license_id: str, *, publish: bool = True) -> Self:
        """Set the dataset license.

        Args:
            license_id: License identifier.
            publish: Whether to publish after updating.

        Returns:
            Self for method chaining.
        """
        return self._set_metadata_value("default", "license_id", license_id, publish=publish)

    # =========================================================================
    # Actions
    # =========================================================================

    def publish(self) -> Self:
        """Publish the dataset to make changes visible.

        Returns:
            Self for method chaining.
        """
        self._client.post(f"/datasets/{self.uid}/publish/")
        logger.info("Published dataset", uid=self.uid)
        return self

    def unpublish(self) -> Self:
        """Unpublish the dataset.

        Returns:
            Self for method chaining.
        """
        self._client.post(f"/datasets/{self.uid}/unpublish/")
        logger.info("Unpublished dataset", uid=self.uid)
        return self

    def refresh(self) -> Self:
        """Refresh the dataset (re-process data).

        Returns:
            Self for method chaining.
        """
        self._client.put(f"/datasets/{self.uid}/")
        logger.info("Refreshed dataset", uid=self.uid)
        return self
