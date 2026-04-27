"""Integration test for full dataset lifecycle on a temporary restricted dataset."""

import os
import time
from contextlib import suppress
from uuid import uuid4

import pytest

from huwise_utils_py import HttpClient, HuwiseAutomationError, HuwiseConfig, HuwiseDataset

pytestmark = pytest.mark.skipif(
    not os.getenv("HUWISE_API_KEY"),
    reason="HUWISE_API_KEY not set - skipping tests",
)


def _build_temp_dataset_id() -> str:
    return f"it-secret-{int(time.time())}-{uuid4().hex[:6]}"


class TestDatasetLifecycleIntegration:
    """Create, mutate metadata/schema, and delete temporary datasets."""

    def test_restricted_dataset_full_lifecycle(self) -> None:
        """Create restricted dataset, verify metadata+schema flow, then delete."""
        dataset_id = _build_temp_dataset_id()
        title_v1 = f"Integration lifecycle title v1 {int(time.time())}"
        title_v2 = f"Integration lifecycle title v2 {int(time.time())}"

        dataset = HuwiseDataset.create(
            metadata={"default": {"title": {"value": title_v1}}},
            dataset_id=dataset_id,
            is_restricted=True,
        )
        field_uid: str | None = None

        try:
            # Assert the dataset is restricted (secret)
            config = HuwiseConfig.from_env()
            client = HttpClient(config)
            details = client.get(f"/datasets/{dataset.uid}/").json()
            assert details["is_restricted"] is True
            assert details["dataset_id"] == dataset_id

            # Initial metadata read
            assert dataset.get_title() == title_v1

            # Set metadata and read again
            dataset.set_title(title_v2, publish=False)
            dataset.set_description("Lifecycle test description", publish=False)
            dataset.set_keywords(["integration", "lifecycle", "secret"], publish=True)
            assert dataset.get_title() == title_v2
            assert "Lifecycle test description" in (dataset.get_description() or "")
            assert set(dataset.get_keywords() or []) == {"integration", "lifecycle", "secret"}

            # Change schema and read it back
            field_payload = {
                "name": "lifecycle_test_field",
                "label": "Lifecycle Test Field",
                "description": "Created by integration lifecycle test",
                "type": "text",
            }
            created_field = dataset.append_field_configuration(field_payload)
            field_uid = created_field["uid"]
            listed_fields = dataset.list_field_configurations(limit=200).get("results", [])
            assert any(field.get("uid") == field_uid for field in listed_fields)

            updated_payload = {
                "name": "lifecycle_test_field",
                "label": "Lifecycle Test Field Updated",
                "description": "Updated by integration lifecycle test",
                "type": "text",
            }
            dataset.update_field_configuration(field_uid, updated_payload)
            retrieved_field = dataset.retrieve_field_configuration(field_uid)
            assert retrieved_field["label"] == "Lifecycle Test Field Updated"

        finally:
            # Cleanup field first (if still present), then dataset itself.
            if field_uid is not None:
                with suppress(Exception):
                    dataset.delete_field_configuration(field_uid)
            dataset.delete()

        # Confirm deletion
        with pytest.raises(HuwiseAutomationError) as exc_info:
            client = HttpClient(HuwiseConfig.from_env())
            client.get(f"/datasets/{dataset.uid}/")
        assert exc_info.value.response.status_code == 404
