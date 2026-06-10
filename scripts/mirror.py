#!/usr/bin/env python3
"""Re-mirror openapi.yaml and the Postman collection from the production spec.

Usage:
    python3 scripts/mirror.py

Steps:
  1. Fetch https://www.wearewarp.com/api/v1/openapi.json and rewrite openapi.yaml
     using the exact serialization the committed file was written with (PyYAML,
     key order preserved, 120-column wrap), so re-mirroring an unchanged
     production spec produces an empty git diff.
  2. Regenerate postman/warp-freight-api.postman_collection.json from
     openapi.yaml with openapi-to-postmanv2, restore the stable _postman_id so
     Postman re-imports update the collection in place, and re-serialize with
     4-space indent and no trailing newline to match the committed formatting.

openapi-to-postmanv2 samples fresh item ids and example values on every run,
so expect the collection diff to be larger than the underlying spec change.
Only commit the regenerated collection alongside a real production spec change.

Requires Python 3 with PyYAML, plus Node (npx) for openapi-to-postmanv2.
"""

import json
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: python3 -m pip install pyyaml")

SPEC_URL = "https://www.wearewarp.com/api/v1/openapi.json"
POSTMAN_ID = "4492fb92-852b-4b19-8567-073830d2e124"

REPO_ROOT = Path(__file__).resolve().parent.parent
OPENAPI_YAML = REPO_ROOT / "openapi.yaml"
POSTMAN_COLLECTION = REPO_ROOT / "postman" / "warp-freight-api.postman_collection.json"


def mirror_openapi():
    with urllib.request.urlopen(SPEC_URL) as response:
        spec = json.load(response)
    text = yaml.safe_dump(
        spec,
        sort_keys=False,
        default_flow_style=False,
        allow_unicode=True,
        width=120,
    )
    OPENAPI_YAML.write_text(text, encoding="utf-8")
    print(f"wrote {OPENAPI_YAML.relative_to(REPO_ROOT)}")


def regenerate_postman():
    if shutil.which("npx") is None:
        sys.exit("Node (npx) is required for openapi-to-postmanv2")
    subprocess.run(
        [
            "npx",
            "-y",
            "openapi-to-postmanv2",
            "-s",
            "openapi.yaml",
            "-o",
            str(POSTMAN_COLLECTION.relative_to(REPO_ROOT)),
            "-p",
        ],
        cwd=REPO_ROOT,
        check=True,
    )
    collection = json.loads(POSTMAN_COLLECTION.read_text(encoding="utf-8"))
    collection["info"]["_postman_id"] = POSTMAN_ID
    POSTMAN_COLLECTION.write_text(
        json.dumps(collection, indent=4, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"wrote {POSTMAN_COLLECTION.relative_to(REPO_ROOT)}")


def main():
    mirror_openapi()
    regenerate_postman()


if __name__ == "__main__":
    main()
