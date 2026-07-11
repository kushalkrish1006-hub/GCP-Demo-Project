"""Upload bronze-layer CSV files to Google Cloud Storage.

Example:
    python src/data_ingestion/batch/upload_to_gcs.py \
        --bucket my-gcs-bucket \
        --source-dir data/bronze \
        --prefix raw/ecommerce
"""

from __future__ import annotations

import argparse
from pathlib import Path


DEFAULT_SOURCE_DIR = Path("data/bronze")
DEFAULT_PATTERN = "*.csv"


def build_blob_name(source_dir: Path, file_path: Path, prefix: str) -> str:
    relative_path = file_path.relative_to(source_dir).as_posix()
    clean_prefix = prefix.strip("/")
    if not clean_prefix:
        return relative_path
    return f"{clean_prefix}/{relative_path}"


def discover_files(source_dir: Path, pattern: str) -> list[Path]:
    if not source_dir.exists():
        raise FileNotFoundError(f"Source directory does not exist: {source_dir}")
    if not source_dir.is_dir():
        raise NotADirectoryError(f"Source path is not a directory: {source_dir}")

    return sorted(path for path in source_dir.rglob(pattern) if path.is_file())


def get_storage_client(project: str | None):
    try:
        from google.cloud import storage
    except ImportError as exc:  # pragma: no cover - depends on local environment
        raise SystemExit(
            "Missing dependency: google-cloud-storage. "
            "Install it with `pip install google-cloud-storage`."
        ) from exc

    return storage.Client(project=project)


def upload_file(bucket, file_path: Path, blob_name: str) -> None:
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(str(file_path))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Upload generated bronze CSV files to a GCS bucket."
    )
    parser.add_argument("--bucket", required=True, help="Target GCS bucket name.")
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=DEFAULT_SOURCE_DIR,
        help="Local directory containing files to upload.",
    )
    parser.add_argument(
        "--prefix",
        default="",
        help="Optional GCS object prefix, for example raw/ecommerce.",
    )
    parser.add_argument(
        "--pattern",
        default=DEFAULT_PATTERN,
        help="File glob pattern to upload from source-dir.",
    )
    parser.add_argument(
        "--project",
        default=None,
        help="Optional GCP project ID for the storage client.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned uploads without sending files to GCS.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    files = discover_files(args.source_dir, args.pattern)

    if not files:
        print(f"No files matched {args.pattern!r} in {args.source_dir}")
        return

    upload_plan = [
        (file_path, build_blob_name(args.source_dir, file_path, args.prefix))
        for file_path in files
    ]

    if args.dry_run:
        print(f"Dry run: {len(upload_plan)} file(s) would be uploaded")
        for file_path, blob_name in upload_plan:
            print(f"{file_path} -> gs://{args.bucket}/{blob_name}")
        return

    client = get_storage_client(args.project)
    bucket = client.bucket(args.bucket)

    for file_path, blob_name in upload_plan:
        upload_file(bucket, file_path, blob_name)
        print(f"Uploaded {file_path} -> gs://{args.bucket}/{blob_name}")

    print(f"Uploaded {len(upload_plan)} file(s) to gs://{args.bucket}")


if __name__ == "__main__":
    main()
