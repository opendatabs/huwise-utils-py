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

# Map of Huwise license_id values to license URLs
LICENSE_MAP: dict[str, str] = {
    "4bj8ceb": "https://creativecommons.org/publicdomain/zero/1.0/",  # CC0 1.0
    "cc_by": "https://creativecommons.org/licenses/by/3.0/ch/",  # CC BY 3.0 CH
    "5sylls5": "https://creativecommons.org/licenses/by/4.0/",  # CC BY 4.0
    "t2kf10u": "https://data-bs.ch/stata/dataspot/permalinks/20210113_OSM-Vektordaten.pdf",  # CC BY 3.0 CH + OpenStreetMap
    "353v4r": "https://data-bs.ch/stata/dataspot/permalinks/20240822-osm-vektordaten.pdf",  # CC BY 4.0 + OpenStreetMap
    "vzo5u7j": "https://www.gnu.org/licenses/gpl-3.0",  # GNU General Public License 3
    "r617wgj": "https://www.bs.ch/bvd/grundbuch-und-vermessungsamt/geo/anwendungen/agb",  # Nutzungsbedingungen für Geodaten des Kantons Basel-Stadt
    "ce0mv1b": "https://opendata.swiss/de/terms-of-use/",  # Freie Nutzung. Quellenangabe ist Pflicht. Kommerzielle Nutzung nur mit Bewilligung des Datenlieferanten zulässig.
}


@dataclass
class HuwiseDataset:
    """Represents a Huwise dataset with metadata operations.

    Provides a fluent interface for reading and modifying dataset metadata.
    Supports method chaining for convenient batch updates.

    Attributes:
        uid: The unique string identifier of the dataset.
        config: Optional HuwiseConfig (uses default if not provided).

    Examples:
        Create from a dataset ID and modify with method chaining:

        ```python
        dataset = HuwiseDataset.from_id("100123")
        dataset.set_title("New Title", publish=False) \
               .set_description("Description") \
               .publish()
        ```

        Read metadata:

        ```python
        dataset = HuwiseDataset.from_id("100123")
        title = dataset.get_title()
        ```
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

        Uses the per-template endpoint
        ``GET /datasets/{uid}/metadata/{template}/``

        Args:
            template: Metadata template name (e.g., "default").
            field_name: Field name within the template.

        Returns:
            The field value or None if not set.
        """
        response = self._client.get(f"/datasets/{self.uid}/metadata/{template}/")
        template_data: dict[str, Any] = response.json()
        return template_data.get(field_name, {}).get("value")

    def _set_metadata_value(self, template: str, field_name: str, value: Any, *, publish: bool = True) -> Self:
        """Set a specific metadata field value.

        Uses the per-field endpoint
        ``PUT /datasets/{uid}/metadata/{template}/{field_name}/``

        Args:
            template: Metadata template name (e.g., "default").
            field_name: Field name within the template.
            value: The value to set.
            publish: Whether to publish after updating.

        Returns:
            Self for method chaining.
        """
        self._wait_for_idle()
        self._client.put(
            f"/datasets/{self.uid}/metadata/{template}/{field_name}/",
            json={"value": value},
        )

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

        Checks ``internal.license_id`` first (where the platform stores the
        canonical license ID, e.g. ``"5sylls5"``).  Falls back to
        ``default.license`` (human-readable string used by older datasets,
        e.g. ``"CC BY"``).

        Returns:
            The license identifier/name, or None if neither field is set.
        """
        value = self._get_metadata_value("internal", "license_id")
        if value is None:
            value = self._get_metadata_value("default", "license")
        return value

    def get_custom_view(self) -> dict[str, Any] | None:
        """Retrieve the dataset custom view configuration.

        Returns:
            Custom view dictionary or None if not set.
        """
        return self._get_metadata_value("visualization", "custom_view")

    def get_dcat_ap_ch_rights(self) -> str | None:
        """Retrieve the DCAT-AP-CH rights statement.

        Returns:
            The rights statement string (e.g.
            ``"NonCommercialAllowed-CommercialAllowed-ReferenceNotRequired"``)
            or None if not set.
        """
        return self._get_metadata_value("dcat_ap_ch", "rights")

    def get_dcat_ap_ch_license(self) -> str | None:
        """Retrieve the DCAT-AP-CH license code.

        Returns:
            The license code (e.g. ``"terms_open"``) or None if not set.
        """
        return self._get_metadata_value("dcat_ap_ch", "license")

    def get_created(self) -> str | None:
        """Retrieve the dataset creation date (``dcat.created``).

        Returns:
            ISO datetime string or None if not set.
        """
        return self._get_metadata_value("dcat", "created")

    def get_issued(self) -> str | None:
        """Retrieve the dataset publication date (``dcat.issued``).

        Returns:
            ISO datetime string or None if not set.
        """
        return self._get_metadata_value("dcat", "issued")

    def get_creator(self) -> str | None:
        """Retrieve the dataset creator.

        Returns:
            The creator name or None if not set.
        """
        return self._get_metadata_value("dcat", "creator")

    def get_contributor(self) -> str | None:
        """Retrieve the dataset contributor.

        Returns:
            The contributor name or None if not set.
        """
        return self._get_metadata_value("dcat", "contributor")

    def get_contact_name(self) -> str | None:
        """Retrieve the dataset contact name.

        Returns:
            The contact name or None if not set.
        """
        return self._get_metadata_value("dcat", "contact_name")

    def get_contact_email(self) -> str | None:
        """Retrieve the dataset contact email.

        Returns:
            The contact email address or None if not set.
        """
        return self._get_metadata_value("dcat", "contact_email")

    def get_accrualperiodicity(self) -> str | None:
        """Retrieve the dataset accrual periodicity.

        Returns:
            EU frequency URI string (e.g.
            ``"http://publications.europa.eu/resource/authority/frequency/DAILY"``)
            or None if not set.
        """
        return self._get_metadata_value("dcat", "accrualperiodicity")

    def get_relation(self) -> str | None:
        """Retrieve the dataset relation URL.

        Returns:
            The relation URL string or None if not set.
        """
        return self._get_metadata_value("dcat", "relation")

    def get_modified(self) -> str | None:
        """Retrieve the dataset last-modified date (``default.modified``).

        Returns:
            ISO datetime string or None if not set.
        """
        return self._get_metadata_value("default", "modified")

    def get_geographic_reference(self) -> list[str] | None:
        """Retrieve the dataset geographic reference codes.

        Returns:
            List of geographic reference codes (e.g.
            ``["ch_40_12"]``) or None if not set.
        """
        return self._get_metadata_value("default", "geographic_reference")

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

    def set_license(
        self,
        license_id: str,
        *,
        license_name: str | None = None,
        publish: bool = True,
    ) -> Self:
        """Set the dataset license.

        Uses per-field ``PUT`` endpoints to update ``default.license_id``
        (and optionally ``default.license``) without risking overwrites to
        other metadata fields.  The platform propagates ``license_id`` to
        ``internal.license_id`` automatically.

        Args:
            license_id: License identifier (e.g. ``"5sylls5"``).
            license_name: Optional human-readable name (e.g. ``"CC BY 4.0"``).
                If provided, ``default.license`` is updated alongside
                ``default.license_id``.
            publish: Whether to publish after updating.

        Returns:
            Self for method chaining.
        """
        self._wait_for_idle()

        # Set the writable license_id (platform propagates to internal.license_id)
        self._client.put(
            f"/datasets/{self.uid}/metadata/default/license_id/",
            json={"value": license_id},
        )

        # Optionally set the human-readable license string
        if license_name is not None:
            self._client.put(
                f"/datasets/{self.uid}/metadata/default/license/",
                json={"value": license_name},
            )

        logger.info(
            "Updated license",
            uid=self.uid,
            license_id=license_id,
            license_name=license_name,
        )

        if publish:
            self.publish()

        return self

    def set_dcat_ap_ch_rights(self, rights: str, *, publish: bool = True) -> Self:
        """Set the DCAT-AP-CH rights statement.

        Args:
            rights: Rights statement string (e.g.
                ``"NonCommercialAllowed-CommercialAllowed-ReferenceRequired"``).
                See the documentation for a full list of valid values.
            publish: Whether to publish after updating.

        Returns:
            Self for method chaining.
        """
        return self._set_metadata_value("dcat_ap_ch", "rights", rights, publish=publish)

    def set_dcat_ap_ch_license(self, license_code: str, *, publish: bool = True) -> Self:
        """Set the DCAT-AP-CH license code.

        Args:
            license_code: License code (e.g. ``"terms_open"``, ``"terms_by"``).
                See the documentation for a full list of valid values.
            publish: Whether to publish after updating.

        Returns:
            Self for method chaining.
        """
        return self._set_metadata_value("dcat_ap_ch", "license", license_code, publish=publish)

    def set_created(self, created: str, *, publish: bool = True) -> Self:
        """Set the dataset creation date (``dcat.created``).

        Args:
            created: ISO datetime string (e.g. ``"2024-01-15T10:30:00Z"``).
            publish: Whether to publish after updating.

        Returns:
            Self for method chaining.
        """
        return self._set_metadata_value("dcat", "created", created, publish=publish)

    def set_issued(self, issued: str, *, publish: bool = True) -> Self:
        """Set the dataset publication date (``dcat.issued``).

        Args:
            issued: ISO datetime string (e.g. ``"2024-01-15"``).
            publish: Whether to publish after updating.

        Returns:
            Self for method chaining.
        """
        return self._set_metadata_value("dcat", "issued", issued, publish=publish)

    def set_creator(self, creator: str, *, publish: bool = True) -> Self:
        """Set the dataset creator.

        Args:
            creator: Creator name.
            publish: Whether to publish after updating.

        Returns:
            Self for method chaining.
        """
        return self._set_metadata_value("dcat", "creator", creator, publish=publish)

    def set_contributor(self, contributor: str, *, publish: bool = True) -> Self:
        """Set the dataset contributor.

        Args:
            contributor: Contributor name.
            publish: Whether to publish after updating.

        Returns:
            Self for method chaining.
        """
        return self._set_metadata_value("dcat", "contributor", contributor, publish=publish)

    def set_contact_name(self, name: str, *, publish: bool = True) -> Self:
        """Set the dataset contact name.

        Args:
            name: Contact name.
            publish: Whether to publish after updating.

        Returns:
            Self for method chaining.
        """
        return self._set_metadata_value("dcat", "contact_name", name, publish=publish)

    def set_contact_email(self, email: str, *, publish: bool = True) -> Self:
        """Set the dataset contact email.

        Args:
            email: Contact email address.
            publish: Whether to publish after updating.

        Returns:
            Self for method chaining.
        """
        return self._set_metadata_value("dcat", "contact_email", email, publish=publish)

    def set_accrualperiodicity(self, frequency: str, *, publish: bool = True) -> Self:
        """Set the dataset accrual periodicity.

        Args:
            frequency: EU frequency URI string (e.g.
                ``"http://publications.europa.eu/resource/authority/frequency/DAILY"``).
            publish: Whether to publish after updating.

        Returns:
            Self for method chaining.
        """
        return self._set_metadata_value("dcat", "accrualperiodicity", frequency, publish=publish)

    def set_relation(self, relation: str, *, publish: bool = True) -> Self:
        """Set the dataset relation URL.

        Args:
            relation: Relation URL string.
            publish: Whether to publish after updating.

        Returns:
            Self for method chaining.
        """
        return self._set_metadata_value("dcat", "relation", relation, publish=publish)

    def set_geographic_reference(self, references: list[str], *, publish: bool = True) -> Self:
        """Set the dataset geographic reference codes.

        Args:
            references: List of geographic reference codes (e.g.
                ``["ch_40_12"]``).  See the documentation for the code
                format: ``{country}_{admin_level}_{territory_id}``.
            publish: Whether to publish after updating.

        Returns:
            Self for method chaining.
        """
        return self._set_metadata_value("default", "geographic_reference", references, publish=publish)

    def set_modified(
        self,
        modified: str,
        *,
        updates_on_metadata_change: bool | None = None,
        updates_on_data_change: bool | None = None,
        publish: bool = True,
    ) -> Self:
        """Set the dataset last-modified date (``default.modified``).

        Uses per-field ``PUT`` endpoints so that each field is updated

        Args:
            modified: ISO datetime string (e.g. ``"2024-01-15T10:30:00Z"``).
            updates_on_metadata_change: If given, sets whether the modified
                date should auto-update when metadata changes.
            updates_on_data_change: If given, sets whether the modified
                date should auto-update when data changes.
            publish: Whether to publish after updating.

        Returns:
            Self for method chaining.
        """
        self._wait_for_idle()

        # Set the modified value
        self._client.put(
            f"/datasets/{self.uid}/metadata/default/modified/",
            json={"value": modified},
        )

        # Optionally set the companion boolean flags
        if updates_on_metadata_change is not None:
            self._client.put(
                f"/datasets/{self.uid}/metadata/default/modified_updates_on_metadata_change/",
                json={"value": updates_on_metadata_change},
            )

        if updates_on_data_change is not None:
            self._client.put(
                f"/datasets/{self.uid}/metadata/default/modified_updates_on_data_change/",
                json={"value": updates_on_data_change},
            )

        logger.info(
            "Updated modified date",
            uid=self.uid,
            modified=modified,
            updates_on_metadata_change=updates_on_metadata_change,
            updates_on_data_change=updates_on_data_change,
        )

        if publish:
            self.publish()

        return self

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
