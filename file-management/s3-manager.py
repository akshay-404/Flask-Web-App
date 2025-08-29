import boto3
import argparse
import os

s3 = boto3.client("s3")

def upload_file(bucket_name, local_file_path, s3_key):
    try:
        s3.upload_file(local_file_path, bucket_name, s3_key)
        print(f"✅ Uploaded {local_file_path} to s3://{bucket_name}/{s3_key}")
    except Exception as e:
        print(f"❌ Upload failed: {e}")

def download_file(bucket_name, s3_key, local_file_path=None):
    try:
        # If no local path provided, use the same filename as s3_key
        if local_file_path is None:
            local_file_path = os.path.basename(s3_key)

        s3.download_file(bucket_name, s3_key, local_file_path)
        print(f"✅ Downloaded s3://{bucket_name}/{s3_key} to {local_file_path}")
    except Exception as e:
        print(f"❌ Download failed: {e}")

def main():
    parser = argparse.ArgumentParser(description="Upload/Download files to/from AWS S3")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Upload command
    upload_parser = subparsers.add_parser("upload", help="Upload file to S3")
    upload_parser.add_argument("bucket_name", help="S3 bucket name")
    upload_parser.add_argument("local_file_path", help="Local file path")
    upload_parser.add_argument("s3_key", help="S3 object key (filename in bucket)")

    # Download command
    download_parser = subparsers.add_parser("download", help="Download file from S3")
    download_parser.add_argument("bucket_name", help="S3 bucket name")
    download_parser.add_argument("s3_key", help="S3 object key (filename in bucket)")
    download_parser.add_argument("local_file_path", nargs="?", help="Local file path (optional)")

    args = parser.parse_args()

    if args.command == "upload":
        upload_file(args.bucket_name, args.local_file_path, args.s3_key)
    elif args.command == "download":
        download_file(args.bucket_name, args.s3_key, args.local_file_path)

if __name__ == "__main__":
    main()

