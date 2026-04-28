"""HuwiseDataset class for dataset operations.

This module provides a dataclass-based interface for interacting with
Huwise datasets, supporting method chaining and dependency injection.
"""

import time
from dataclasses import dataclass, field
from typing import Any, NotRequired, Self, TypedDict
from urllib.parse import urlparse

from huwise_utils_py.config import HuwiseConfig
from huwise_utils_py.http import HttpClient
from huwise_utils_py.logger import get_logger
from huwise_utils_py.utils.metadata import assert_non_empty_dataset_id, build_create_dataset_metadata

logger = get_logger(__name__)


class DatasetSecurityQuota(TypedDict):
    """Typed representation of API calls quota configuration."""

    unit: str
    limit: int


class DatasetSecurity(TypedDict):
    """Typed representation of dataset security configuration."""

    is_data_visible: NotRequired[bool]
    visible_fields: NotRequired[list[str]]
    filter_query: NotRequired[str]
    api_calls_quota: NotRequired[DatasetSecurityQuota]


class DatasetCreatePayload(TypedDict):
    """Typed payload for POST /datasets/."""

    metadata: dict[str, Any]
    dataset_id: NotRequired[str]
    is_restricted: NotRequired[bool]
    default_security: NotRequired[DatasetSecurity]


class DatasetUpdatePayload(TypedDict):
    """Typed payload for PUT /datasets/{uid}/."""

    dataset_id: NotRequired[str]
    is_restricted: NotRequired[bool]
    default_security: NotRequired[DatasetSecurity]


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

    @classmethod
    def create(
        cls,
        metadata: dict[str, Any] | None = None,
        *,
        title: str | None = None,
        dataset_id: str | None = None,
        is_restricted: bool | None = None,
        default_security: DatasetSecurity | None = None,
        resource_source_url: str | None = None,
        resource_title: str | None = None,
        resource_extractor_type: str | None = None,
        resource_headers: list[dict[str, str]] | None = None,
        config: HuwiseConfig | None = None,
    ) -> Self:
        """Create a new dataset and return it as a ``HuwiseDataset`` instance.

        Args:
            metadata: Optional dataset metadata payload. If omitted, a minimal
                metadata object is auto-built with ``default.title``.
            title: Optional title used when ``metadata`` is omitted.
            dataset_id: Optional human-readable identifier.
            is_restricted: Optional restriction flag.
            default_security: Optional default security ruleset.
            resource_source_url: Optional HTTP(S) source URL to upsert as a
                resource right after dataset creation.
            resource_title: Optional title used for the created/updated resource.
            resource_extractor_type: Optional extractor type for the resource.
            resource_headers: Optional connection headers for the resource.
            config: Optional HuwiseConfig instance.

        Returns:
            A ``HuwiseDataset`` instance for the created dataset.

        Raises:
            TypeError: If metadata is provided but is not a dictionary.
            ValueError: If response does not contain a UID.
        """
        config = config or HuwiseConfig.from_env()
        client = HttpClient(config)
        payload: DatasetCreatePayload = {
            "metadata": build_create_dataset_metadata(metadata, title=title, dataset_id=dataset_id)
        }

        if dataset_id is not None:
            assert_non_empty_dataset_id(dataset_id)
            payload["dataset_id"] = dataset_id
        if is_restricted is not None:
            payload["is_restricted"] = is_restricted
        if default_security is not None:
            payload["default_security"] = default_security

        response = client.post("/datasets/", json=payload)
        response_data: dict[str, Any] = response.json()
        uid = response_data.get("uid")

        if not isinstance(uid, str) or not uid:
            raise ValueError("Create dataset response does not contain a valid uid")

        logger.info(
            "Created dataset",
            uid=uid,
            dataset_id=dataset_id,
            is_restricted=is_restricted,
        )
        instance = cls(uid=uid, config=config)
        instance._wait_for_idle()
        if resource_source_url is not None:
            instance.upsert_http_resource(
                source_url=resource_source_url,
                title=resource_title,
                extractor_type=resource_extractor_type,
                headers=resource_headers,
            )
        return instance

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

    def delete(self) -> None:
        """Delete the dataset.

        After successful deletion, this instance should no longer be used for
        API operations that require the dataset to exist.
        """
        self._wait_for_idle()
        self._client.delete(f"/datasets/{self.uid}/")
        logger.info("Deleted dataset", uid=self.uid)

    def update_configuration(
        self,
        *,
        dataset_id: str | None = None,
        is_restricted: bool | None = None,
        default_security: DatasetSecurity | None = None,
    ) -> Self:
        """Update dataset-level configuration properties.

        Args:
            dataset_id: Optional new dataset ID.
            is_restricted: Optional restriction flag.
            default_security: Optional default security ruleset.

        Returns:
            Self for method chaining.

        Raises:
            ValueError: If no configuration field is provided.
        """
        payload: DatasetUpdatePayload = {}
        if dataset_id is not None:
            payload["dataset_id"] = dataset_id
        if is_restricted is not None:
            payload["is_restricted"] = is_restricted
        if default_security is not None:
            payload["default_security"] = default_security

        if not payload:
            raise ValueError("At least one configuration field must be provided")

        self._client.put(f"/datasets/{self.uid}/", json=payload)
        logger.info(
            "Updated dataset configuration",
            uid=self.uid,
            dataset_id=dataset_id,
            is_restricted=is_restricted,
            has_default_security=default_security is not None,
        )
        return self

    def list_field_configurations(self, *, limit: int | None = None, offset: int | None = None) -> dict[str, Any]:
        """List field configurations for the dataset.

        Args:
            limit: Optional pagination limit.
            offset: Optional pagination offset.

        Returns:
            Paginated response dictionary with field configurations.
        """
        params: dict[str, int] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        response = self._client.get(f"/datasets/{self.uid}/fields/", params=params or None)
        return response.json()

    def retrieve_field_configuration(self, field_uid: str) -> dict[str, Any]:
        """Retrieve one field configuration by UID.

        Args:
            field_uid: Field configuration UID.

        Returns:
            Field configuration dictionary.
        """
        response = self._client.get(f"/datasets/{self.uid}/fields/{field_uid}/")
        return response.json()

    def append_field_configuration(self, field_configuration: dict[str, Any]) -> dict[str, Any]:
        """Append a new field configuration processor.

        Args:
            field_configuration: Payload for field configuration creation.

        Returns:
            Created field configuration response.
        """
        self._wait_for_idle()
        response = self._client.post(f"/datasets/{self.uid}/fields/", json=field_configuration)
        logger.info("Appended dataset field configuration", uid=self.uid, field_type=field_configuration.get("type"))
        return response.json()

    def update_field_configuration(self, field_uid: str, field_configuration: dict[str, Any]) -> dict[str, Any]:
        """Update an existing field configuration processor.

        Args:
            field_uid: Field configuration UID.
            field_configuration: Updated field configuration payload.

        Returns:
            Updated field configuration response.
        """
        self._wait_for_idle()
        response = self._client.put(f"/datasets/{self.uid}/fields/{field_uid}/", json=field_configuration)
        logger.info(
            "Updated dataset field configuration",
            uid=self.uid,
            field_uid=field_uid,
            field_type=field_configuration.get("type"),
        )
        return response.json()

    def delete_field_configuration(self, field_uid: str) -> Self:
        """Delete a field configuration processor.

        Args:
            field_uid: Field configuration UID.

        Returns:
            Self for method chaining.
        """
        self._wait_for_idle()
        self._client.delete(f"/datasets/{self.uid}/fields/{field_uid}/")
        logger.info("Deleted dataset field configuration", uid=self.uid, field_uid=field_uid)
        return self

    @staticmethod
    def _normalize_http_source_url(source_url: str) -> tuple[str, str]:
        """Split and normalize source URL into base and relative URL.

        Args:
            source_url: Full URL to the remote source.

        Returns:
            Tuple of (connection_url, relative_url).

        Raises:
            ValueError: If source_url is empty or not an absolute HTTP(S) URL.
        """
        normalized_source = source_url.strip()
        if not normalized_source:
            raise ValueError("source_url must not be empty")

        parsed = urlparse(normalized_source)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("source_url must be an absolute HTTP(S) URL")

        connection_url = f"{parsed.scheme.lower()}://{parsed.netloc.lower()}"
        relative_path = parsed.path if parsed.path else "/"
        if not relative_path.startswith("/"):
            relative_path = f"/{relative_path}"
        if relative_path != "/" and relative_path.endswith("/"):
            relative_path = relative_path.rstrip("/")

        relative_url = relative_path
        if parsed.query:
            relative_url = f"{relative_url}?{parsed.query}"

        return connection_url, relative_url

    @staticmethod
    def _extract_resource_url_parts(resource: dict[str, Any]) -> tuple[str | None, str | None]:
        """Extract normalized connection and relative URL from a resource."""
        connection = resource.get("connection")
        if not isinstance(connection, dict):
            return None, None

        connection_url = connection.get("url")
        if not isinstance(connection_url, str):
            return None, None

        relative_url = resource.get("relative_url")
        if not isinstance(relative_url, str):
            return None, None

        return connection_url, relative_url

    def list_resources(self, *, limit: int | None = None, offset: int | None = None) -> dict[str, Any]:
        """List resources for the dataset.

        Args:
            limit: Optional pagination limit.
            offset: Optional pagination offset.

        Returns:
            Paginated response dictionary with resources.
        """
        params: dict[str, int] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        response = self._client.get(f"/datasets/{self.uid}/resources/", params=params or None)
        return response.json()

    def upsert_http_resource(
        self,
        *,
        source_url: str,
        title: str | None = None,
        extractor_type: str | None = None,
        headers: list[dict[str, str]] | None = None,
    ) -> dict[str, Any]:
        """Create or update a dataset HTTP resource idempotently.

        Args:
            source_url: Absolute HTTP(S) source URL.
            title: Optional resource title.
            extractor_type: Optional extractor type. Not auto-guessed.
            headers: Optional connection headers list.

        Returns:
            Created or updated resource payload.
        """
        connection_url, relative_url = self._normalize_http_source_url(source_url)

        payload: dict[str, Any] = {
            "type": "http",
            "connection": {"url": connection_url},
            "relative_url": relative_url,
        }
        if title is not None:
            payload["title"] = title
        if extractor_type is not None:
            payload["extractor_type"] = extractor_type
        if headers is not None:
            payload["connection"]["headers"] = headers

        existing_resources = self.list_resources(limit=200).get("results", [])
        if not isinstance(existing_resources, list):
            existing_resources = []

        matching_resource: dict[str, Any] | None = None
        for resource in existing_resources:
            if not isinstance(resource, dict):
                continue

            resource_uid = resource.get("uid")
            if not isinstance(resource_uid, str):
                continue

            existing_connection_url, existing_relative_url = self._extract_resource_url_parts(resource)
            url_match = existing_connection_url == connection_url and existing_relative_url == relative_url
            title_match = title is not None and resource.get("title") == title

            if url_match or title_match:
                matching_resource = resource
                break

        self._wait_for_idle()

        if matching_resource is not None:
            resource_uid = matching_resource["uid"]
            response = self._client.put(f"/datasets/{self.uid}/resources/{resource_uid}/", json=payload)
            logger.info(
                "Updated dataset resource",
                uid=self.uid,
                resource_uid=resource_uid,
                connection_url=connection_url,
                relative_url=relative_url,
            )
            return response.json()

        response = self._client.post(f"/datasets/{self.uid}/resources/", json=payload)
        logger.info(
            "Created dataset resource",
            uid=self.uid,
            connection_url=connection_url,
            relative_url=relative_url,
        )
        return response.json()

    def delete_resource(self, resource_uid: str) -> Self:
        """Delete a resource by UID.

        Args:
            resource_uid: Resource UID.

        Returns:
            Self for method chaining.
        """
        self._wait_for_idle()
        self._client.delete(f"/datasets/{self.uid}/resources/{resource_uid}/")
        logger.info("Deleted dataset resource", uid=self.uid, resource_uid=resource_uid)
        return self
