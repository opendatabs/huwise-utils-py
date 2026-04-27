"""Helpers for Automation API dataset metadata payloads."""

from __future__ import annotations

from typing import Any


def assert_non_empty_dataset_id(dataset_id: str) -> None:
    """Raise ``ValueError`` if ``dataset_id`` is missing or blank.

    The create-dataset API requires a non-empty human-readable identifier when
    ``dataset_id`` is supplied on the request.
    """
    if not isinstance(dataset_id, str) or not dataset_id.strip():
        raise ValueError("dataset_id must be a non-empty string")


def strip_empty_metadata_values(metadata: dict[str, Any]) -> dict[str, Any]:
    """Return a copy of ``metadata`` without fields whose ``value`` is empty.

    Walks template dicts shaped like ``{ template: { field: { "value": ... }}}``
    and drops entries where ``value`` is ``None``, ``""``, or ``[]``. Templates
    that become empty are omitted.

    Use before :func:`create_dataset` to avoid sending empty cells that some
    domains reject with HTTP 400 validation errors.

    Args:
        metadata: Nested metadata mapping as accepted by the Automation API.

    Returns:
        New metadata dict; the input is not modified.
    """
    result: dict[str, Any] = {}
    for template_name, fields in metadata.items():
        if not isinstance(fields, dict):
            result[template_name] = fields
            continue
        new_fields: dict[str, Any] = {}
        for field_name, spec in fields.items():
            if not isinstance(spec, dict):
                new_fields[field_name] = spec
                continue
            if "value" not in spec:
                new_fields[field_name] = spec
                continue
            val = spec.get("value")
            if val is None or val == "" or val == []:
                continue
            new_fields[field_name] = spec
        if new_fields:
            result[template_name] = new_fields
    return result
