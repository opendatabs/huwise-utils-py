"""Setter functions for dataset metadata.

These functions provide a simple interface for updating dataset metadata.
They wrap the HuwiseDataset class internally.
"""

from typing import Any

from huwise_utils_py.config import HuwiseConfig
from huwise_utils_py.dataset import HuwiseDataset
from huwise_utils_py.http import HttpClient
from huwise_utils_py.utils.validators import validate_dataset_identifier


def set_dataset_public(
    dataset_id: str | None = None,
    dataset_uid: str | None = None,
    should_be_public: bool = True,
) -> None:
    """Publish or unpublish a dataset.

    Args:
        dataset_id: The numeric identifier of the dataset.
        dataset_uid: The unique string identifier (UID) of the dataset.
        should_be_public: True to publish, False to unpublish.

    Raises:
        ValueError: If both or neither identifiers are provided.
    """
    uid = validate_dataset_identifier(dataset_id, dataset_uid)
    dataset = HuwiseDataset(uid=uid)
    if should_be_public:
        dataset.publish()
    else:
        dataset.unpublish()


def set_dataset_title(
    title: str,
    dataset_id: str | None = None,
    dataset_uid: str | None = None,
    publish: bool = True,
) -> None:
    """Set the title of a dataset.

    Args:
        title: The new title for the dataset.
        dataset_id: The numeric identifier of the dataset.
        dataset_uid: The unique string identifier (UID) of the dataset.
        publish: Whether to publish after updating.
    """
    uid = validate_dataset_identifier(dataset_id, dataset_uid)
    dataset = HuwiseDataset(uid=uid)
    dataset.set_title(title, publish=publish)


def set_dataset_description(
    description: str,
    dataset_id: str | None = None,
    dataset_uid: str | None = None,
    publish: bool = True,
) -> None:
    """Set the description of a dataset.

    Args:
        description: The new description for the dataset.
        dataset_id: The numeric identifier of the dataset.
        dataset_uid: The unique string identifier (UID) of the dataset.
        publish: Whether to publish after updating.
    """
    uid = validate_dataset_identifier(dataset_id, dataset_uid)
    dataset = HuwiseDataset(uid=uid)
    dataset.set_description(description, publish=publish)


def set_dataset_keywords(
    keywords: list[str],
    dataset_id: str | None = None,
    dataset_uid: str | None = None,
    publish: bool = True,
) -> None:
    """Set the keywords of a dataset.

    Args:
        keywords: List of keywords for the dataset.
        dataset_id: The numeric identifier of the dataset.
        dataset_uid: The unique string identifier (UID) of the dataset.
        publish: Whether to publish after updating.
    """
    uid = validate_dataset_identifier(dataset_id, dataset_uid)
    dataset = HuwiseDataset(uid=uid)
    dataset.set_keywords(keywords, publish=publish)


def set_dataset_language(
    language: str,
    dataset_id: str | None = None,
    dataset_uid: str | None = None,
    publish: bool = True,
) -> None:
    """Set the language of a dataset.

    Args:
        language: Language code (e.g., "en", "de", "fr").
        dataset_id: The numeric identifier of the dataset.
        dataset_uid: The unique string identifier (UID) of the dataset.
        publish: Whether to publish after updating.
    """
    uid = validate_dataset_identifier(dataset_id, dataset_uid)
    dataset = HuwiseDataset(uid=uid)
    dataset.set_language(language, publish=publish)


def set_dataset_publisher(
    publisher: str,
    dataset_id: str | None = None,
    dataset_uid: str | None = None,
    publish: bool = True,
) -> None:
    """Set the publisher of a dataset.

    Args:
        publisher: Publisher name.
        dataset_id: The numeric identifier of the dataset.
        dataset_uid: The unique string identifier (UID) of the dataset.
        publish: Whether to publish after updating.
    """
    uid = validate_dataset_identifier(dataset_id, dataset_uid)
    dataset = HuwiseDataset(uid=uid)
    dataset.set_publisher(publisher, publish=publish)


def set_dataset_theme(
    theme_id: str,
    dataset_id: str | None = None,
    dataset_uid: str | None = None,
    publish: bool = True,
) -> None:
    """Set the theme of a dataset.

    Args:
        theme_id: Theme identifier.
        dataset_id: The numeric identifier of the dataset.
        dataset_uid: The unique string identifier (UID) of the dataset.
        publish: Whether to publish after updating.
    """
    uid = validate_dataset_identifier(dataset_id, dataset_uid)
    dataset = HuwiseDataset(uid=uid)
    dataset.set_theme(theme_id, publish=publish)


def set_dataset_license(
    license_id: str,
    dataset_id: str | None = None,
    dataset_uid: str | None = None,
    license_name: str | None = None,
    publish: bool = True,
) -> None:
    """Set the license of a dataset.

    Args:
        license_id: License identifier (e.g. ``"5sylls5"``).
        dataset_id: The numeric identifier of the dataset.
        dataset_uid: The unique string identifier (UID) of the dataset.
        license_name: Optional human-readable name (e.g. ``"CC BY 4.0"``).
            If provided, ``default.license`` is updated alongside
            ``default.license_id``.
        publish: Whether to publish after updating.
    """
    uid = validate_dataset_identifier(dataset_id, dataset_uid)
    dataset = HuwiseDataset(uid=uid)
    dataset.set_license(license_id, license_name=license_name, publish=publish)


def set_dataset_dcat_ap_ch_rights(
    rights: str,
    dataset_id: str | None = None,
    dataset_uid: str | None = None,
    publish: bool = True,
) -> None:
    """Set the DCAT-AP-CH rights statement of a dataset.

    Args:
        rights: Rights statement string (e.g.
            ``"NonCommercialAllowed-CommercialAllowed-ReferenceRequired"``).
        dataset_id: The numeric identifier of the dataset.
        dataset_uid: The unique string identifier (UID) of the dataset.
        publish: Whether to publish after updating.
    """
    uid = validate_dataset_identifier(dataset_id, dataset_uid)
    dataset = HuwiseDataset(uid=uid)
    dataset.set_dcat_ap_ch_rights(rights, publish=publish)


def set_dataset_dcat_ap_ch_license(
    license_code: str,
    dataset_id: str | None = None,
    dataset_uid: str | None = None,
    publish: bool = True,
) -> None:
    """Set the DCAT-AP-CH license code of a dataset.

    Args:
        license_code: License code (e.g. ``"terms_open"``).
        dataset_id: The numeric identifier of the dataset.
        dataset_uid: The unique string identifier (UID) of the dataset.
        publish: Whether to publish after updating.
    """
    uid = validate_dataset_identifier(dataset_id, dataset_uid)
    dataset = HuwiseDataset(uid=uid)
    dataset.set_dcat_ap_ch_license(license_code, publish=publish)


def set_dataset_created(
    created: str,
    dataset_id: str | None = None,
    dataset_uid: str | None = None,
    publish: bool = True,
) -> None:
    """Set the creation date of a dataset (``dcat.created``).

    Args:
        created: ISO datetime string.
        dataset_id: The numeric identifier of the dataset.
        dataset_uid: The unique string identifier (UID) of the dataset.
        publish: Whether to publish after updating.
    """
    uid = validate_dataset_identifier(dataset_id, dataset_uid)
    dataset = HuwiseDataset(uid=uid)
    dataset.set_created(created, publish=publish)


def set_dataset_issued(
    issued: str,
    dataset_id: str | None = None,
    dataset_uid: str | None = None,
    publish: bool = True,
) -> None:
    """Set the publication date of a dataset (``dcat.issued``).

    Args:
        issued: ISO datetime string.
        dataset_id: The numeric identifier of the dataset.
        dataset_uid: The unique string identifier (UID) of the dataset.
        publish: Whether to publish after updating.
    """
    uid = validate_dataset_identifier(dataset_id, dataset_uid)
    dataset = HuwiseDataset(uid=uid)
    dataset.set_issued(issued, publish=publish)


def set_dataset_creator(
    creator: str,
    dataset_id: str | None = None,
    dataset_uid: str | None = None,
    publish: bool = True,
) -> None:
    """Set the creator of a dataset.

    Args:
        creator: Creator name.
        dataset_id: The numeric identifier of the dataset.
        dataset_uid: The unique string identifier (UID) of the dataset.
        publish: Whether to publish after updating.
    """
    uid = validate_dataset_identifier(dataset_id, dataset_uid)
    dataset = HuwiseDataset(uid=uid)
    dataset.set_creator(creator, publish=publish)


def set_dataset_contributor(
    contributor: str,
    dataset_id: str | None = None,
    dataset_uid: str | None = None,
    publish: bool = True,
) -> None:
    """Set the contributor of a dataset.

    Args:
        contributor: Contributor name.
        dataset_id: The numeric identifier of the dataset.
        dataset_uid: The unique string identifier (UID) of the dataset.
        publish: Whether to publish after updating.
    """
    uid = validate_dataset_identifier(dataset_id, dataset_uid)
    dataset = HuwiseDataset(uid=uid)
    dataset.set_contributor(contributor, publish=publish)


def set_dataset_contact_name(
    name: str,
    dataset_id: str | None = None,
    dataset_uid: str | None = None,
    publish: bool = True,
) -> None:
    """Set the contact name of a dataset.

    Args:
        name: Contact name.
        dataset_id: The numeric identifier of the dataset.
        dataset_uid: The unique string identifier (UID) of the dataset.
        publish: Whether to publish after updating.
    """
    uid = validate_dataset_identifier(dataset_id, dataset_uid)
    dataset = HuwiseDataset(uid=uid)
    dataset.set_contact_name(name, publish=publish)


def set_dataset_contact_email(
    email: str,
    dataset_id: str | None = None,
    dataset_uid: str | None = None,
    publish: bool = True,
) -> None:
    """Set the contact email of a dataset.

    Args:
        email: Contact email address.
        dataset_id: The numeric identifier of the dataset.
        dataset_uid: The unique string identifier (UID) of the dataset.
        publish: Whether to publish after updating.
    """
    uid = validate_dataset_identifier(dataset_id, dataset_uid)
    dataset = HuwiseDataset(uid=uid)
    dataset.set_contact_email(email, publish=publish)


def set_dataset_accrualperiodicity(
    frequency: str,
    dataset_id: str | None = None,
    dataset_uid: str | None = None,
    publish: bool = True,
) -> None:
    """Set the accrual periodicity of a dataset.

    Args:
        frequency: EU frequency URI string.
        dataset_id: The numeric identifier of the dataset.
        dataset_uid: The unique string identifier (UID) of the dataset.
        publish: Whether to publish after updating.
    """
    uid = validate_dataset_identifier(dataset_id, dataset_uid)
    dataset = HuwiseDataset(uid=uid)
    dataset.set_accrualperiodicity(frequency, publish=publish)


def set_dataset_relation(
    relation: str,
    dataset_id: str | None = None,
    dataset_uid: str | None = None,
    publish: bool = True,
) -> None:
    """Set the relation URL of a dataset.

    Args:
        relation: Relation URL string.
        dataset_id: The numeric identifier of the dataset.
        dataset_uid: The unique string identifier (UID) of the dataset.
        publish: Whether to publish after updating.
    """
    uid = validate_dataset_identifier(dataset_id, dataset_uid)
    dataset = HuwiseDataset(uid=uid)
    dataset.set_relation(relation, publish=publish)


def set_dataset_geographic_reference(
    references: list[str],
    dataset_id: str | None = None,
    dataset_uid: str | None = None,
    publish: bool = True,
) -> None:
    """Set the geographic reference codes of a dataset.

    Args:
        references: List of geographic reference codes (e.g. ``["ch_40_12"]``).
        dataset_id: The numeric identifier of the dataset.
        dataset_uid: The unique string identifier (UID) of the dataset.
        publish: Whether to publish after updating.
    """
    uid = validate_dataset_identifier(dataset_id, dataset_uid)
    dataset = HuwiseDataset(uid=uid)
    dataset.set_geographic_reference(references, publish=publish)


def set_dataset_modified(
    modified: str,
    dataset_id: str | None = None,
    dataset_uid: str | None = None,
    updates_on_metadata_change: bool | None = None,
    updates_on_data_change: bool | None = None,
    publish: bool = True,
) -> None:
    """Set the last-modified date of a dataset (``default.modified``).

    Args:
        modified: ISO datetime string.
        dataset_id: The numeric identifier of the dataset.
        dataset_uid: The unique string identifier (UID) of the dataset.
        updates_on_metadata_change: If given, sets whether the modified
            date should auto-update when metadata changes.
        updates_on_data_change: If given, sets whether the modified
            date should auto-update when data changes.
        publish: Whether to publish after updating.
    """
    uid = validate_dataset_identifier(dataset_id, dataset_uid)
    dataset = HuwiseDataset(uid=uid)
    dataset.set_modified(
        modified,
        updates_on_metadata_change=updates_on_metadata_change,
        updates_on_data_change=updates_on_data_change,
        publish=publish,
    )


def set_dataset_metadata_temporal_coverage_start_date(
    start_date: str,
    dataset_id: str | None = None,
    dataset_uid: str | None = None,
    publish: bool = True,
) -> None:
    """Set the temporal coverage start date.

    Args:
        start_date: Start date in ISO format.
        dataset_id: The numeric identifier of the dataset.
        dataset_uid: The unique string identifier (UID) of the dataset.
        publish: Whether to publish after updating.
    """
    uid = validate_dataset_identifier(dataset_id, dataset_uid)
    config = HuwiseConfig.from_env()
    client = HttpClient(config)

    response = client.get(f"/datasets/{uid}/metadata/")
    metadata: dict[str, Any] = response.json()

    if "dcat" not in metadata:
        metadata["dcat"] = {}
    if "temporal_coverage_start_date" not in metadata["dcat"]:
        metadata["dcat"]["temporal_coverage_start_date"] = {}

    metadata["dcat"]["temporal_coverage_start_date"]["value"] = start_date

    client.put(f"/datasets/{uid}/metadata/", json=metadata)

    if publish:
        client.post(f"/datasets/{uid}/publish/")


def set_dataset_metadata_temporal_coverage_end_date(
    end_date: str,
    dataset_id: str | None = None,
    dataset_uid: str | None = None,
    publish: bool = True,
) -> None:
    """Set the temporal coverage end date.

    Args:
        end_date: End date in ISO format.
        dataset_id: The numeric identifier of the dataset.
        dataset_uid: The unique string identifier (UID) of the dataset.
        publish: Whether to publish after updating.
    """
    uid = validate_dataset_identifier(dataset_id, dataset_uid)
    config = HuwiseConfig.from_env()
    client = HttpClient(config)

    response = client.get(f"/datasets/{uid}/metadata/")
    metadata: dict[str, Any] = response.json()

    if "dcat" not in metadata:
        metadata["dcat"] = {}
    if "temporal_coverage_end_date" not in metadata["dcat"]:
        metadata["dcat"]["temporal_coverage_end_date"] = {}

    metadata["dcat"]["temporal_coverage_end_date"]["value"] = end_date

    client.put(f"/datasets/{uid}/metadata/", json=metadata)

    if publish:
        client.post(f"/datasets/{uid}/publish/")


def set_dataset_metadata_temporal_period(
    start_date: str,
    end_date: str,
    dataset_id: str | None = None,
    dataset_uid: str | None = None,
    publish: bool = True,
) -> None:
    """Set the temporal period (both start and end dates).

    Args:
        start_date: Start date in ISO format.
        end_date: End date in ISO format.
        dataset_id: The numeric identifier of the dataset.
        dataset_uid: The unique string identifier (UID) of the dataset.
        publish: Whether to publish after updating.
    """
    uid = validate_dataset_identifier(dataset_id, dataset_uid)
    config = HuwiseConfig.from_env()
    client = HttpClient(config)

    response = client.get(f"/datasets/{uid}/metadata/")
    metadata: dict[str, Any] = response.json()

    if "dcat" not in metadata:
        metadata["dcat"] = {}
    if "temporal_coverage_start_date" not in metadata["dcat"]:
        metadata["dcat"]["temporal_coverage_start_date"] = {}
    if "temporal_coverage_end_date" not in metadata["dcat"]:
        metadata["dcat"]["temporal_coverage_end_date"] = {}

    metadata["dcat"]["temporal_coverage_start_date"]["value"] = start_date
    metadata["dcat"]["temporal_coverage_end_date"]["value"] = end_date

    client.put(f"/datasets/{uid}/metadata/", json=metadata)

    if publish:
        client.post(f"/datasets/{uid}/publish/")


def set_template_metadata(
    template_name: str,
    field_name: str,
    value: Any,
    dataset_id: str | None = None,
    dataset_uid: str | None = None,
    publish: bool = True,
) -> None:
    """Set a metadata field in a specific template.

    Args:
        template_name: Name of the metadata template.
        field_name: Name of the field to set.
        value: Value to set.
        dataset_id: The numeric identifier of the dataset.
        dataset_uid: The unique string identifier (UID) of the dataset.
        publish: Whether to publish after updating.
    """
    uid = validate_dataset_identifier(dataset_id, dataset_uid)
    config = HuwiseConfig.from_env()
    client = HttpClient(config)

    response = client.get(f"/datasets/{uid}/metadata/")
    metadata: dict[str, Any] = response.json()

    if template_name not in metadata:
        metadata[template_name] = {}
    if field_name not in metadata[template_name]:
        metadata[template_name][field_name] = {}

    metadata[template_name][field_name]["value"] = value

    client.put(f"/datasets/{uid}/metadata/", json=metadata)

    if publish:
        client.post(f"/datasets/{uid}/publish/")
