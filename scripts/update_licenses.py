"""Replace CC BY / CC BY 3.0 CH licenses with CC BY 4.0 across all datasets.

Matches on both metadata fields:
    - internal.license_id  (platform IDs like "cc_by")
    - default.license      (human-readable strings like "CC BY")

Usage:
    uv run python scripts/update_licenses.py              # dry run (preview only)
    uv run python scripts/update_licenses.py --apply      # actually update licenses
"""

import argparse
import asyncio

from dotenv import load_dotenv

from huwise_utils_py import LICENSE_MAP, HuwiseDataset
from huwise_utils_py.bulk import bulk_get_metadata_async
from huwise_utils_py.config import HuwiseConfig
from huwise_utils_py.http import HttpClient

parser = argparse.ArgumentParser(description="Update dataset licenses to CC BY 4.0")
parser.add_argument(
    "--apply",
    action="store_true",
    help="Actually apply the changes. Without this flag, runs in dry-run mode.",
)
args = parser.parse_args()
dry_run = not args.apply

load_dotenv()
config = HuwiseConfig.from_env()
client = HttpClient(config)

# Values to match (covers both license fields)
TARGET_LICENSE_IDS = {"cc_by"}  # internal.license_id
TARGET_LICENSE_STRINGS = {"CC BY", "CC BY 3.0 CH"}  # default.license

# Replacement values
NEW_LICENSE_ID = "5sylls5"
NEW_LICENSE_NAME = "CC BY 4.0"

if dry_run:
    print("=== DRY RUN (pass --apply to make changes) ===\n")

print(f"Target license IDs:     {TARGET_LICENSE_IDS}")
print(f"Target license strings: {TARGET_LICENSE_STRINGS}")
print(f"New license:            {NEW_LICENSE_ID} / {NEW_LICENSE_NAME} ({LICENSE_MAP[NEW_LICENSE_ID]})\n")

# Step 1: Paginate through all datasets, collecting both uid and dataset_id
datasets: list[dict[str, str]] = []  # [{"uid": "da_xxx", "dataset_id": "100011"}, ...]
batch_size = 100
offset = 0

while True:
    response = client.get(f"/datasets/?limit={batch_size}&offset={offset}")
    data = response.json()
    results = data.get("results", [])

    if not results:
        break

    datasets.extend({"uid": item["uid"], "dataset_id": item["dataset_id"]} for item in results)

    if not data.get("next"):
        break
    offset += batch_size

uid_to_id = {d["uid"]: d["dataset_id"] for d in datasets}
dataset_uids = [d["uid"] for d in datasets]

print(f"Found {len(datasets)} datasets total\n")

# Step 2: Fetch all metadata concurrently
all_metadata = asyncio.run(bulk_get_metadata_async(dataset_uids, config=config))

# Step 3: Filter datasets with matching licenses and update them
updated = 0
for uid, metadata in all_metadata.items():
    dataset_id = uid_to_id.get(uid, uid)

    if "error" in metadata:
        print(f"  SKIP {dataset_id}: error fetching metadata")
        continue

    internal = metadata.get("internal", {})
    default = metadata.get("default", {})
    license_id = internal.get("license_id", {}).get("value")
    license_str = default.get("license", {}).get("value")

    if license_id in TARGET_LICENSE_IDS or license_str in TARGET_LICENSE_STRINGS:
        current = f"internal.license_id={license_id!r}, default.license={license_str!r}"
        if dry_run:
            print(f"  WOULD UPDATE {dataset_id}: {current}")
        else:
            print(f"  UPDATE {dataset_id}: {current}")
            dataset = HuwiseDataset(uid=uid, config=config)
            dataset.set_license(NEW_LICENSE_ID, license_name=NEW_LICENSE_NAME)
        updated += 1

action = "Would update" if dry_run else "Updated"
print(f"\nDone. {action} {updated}/{len(datasets)} datasets.")
