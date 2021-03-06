import os
import time
import boto3
import logging
from botocore.client import Config
from botocore.exceptions import ClientError
from src.config import Config as AppConfig

logger = logging.getLogger("GW:minio")


class MinioService:
    def __init__(self, url, access_key, secret_key):
        self.url = url
        self.s3 = boto3.resource(
            "s3",
            endpoint_url=url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            config=Config(signature_version="s3v4"),
        )

    def download_files(self, bucket_name, file_name, download_path):

        try:
            path = download_path + "/" + file_name
            self.s3.Bucket(bucket_name).download_file(file_name, path)
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                logger.info("The object does not exist.")
            else:
                logger.info(e)
                raise

    def upload(self, file_path, bucket_name, filename):
        try:
            if (self.s3.Bucket(bucket_name) in self.s3.buckets.all()) == False:
                self.s3.create_bucket(Bucket=bucket_name)
            logger.info(
                "Uploading file to bucket {} minio {}".format(bucket_name, self.url)
            )
            self.s3.Bucket(bucket_name).upload_file(file_path, filename)
            return bucket_name + "/" + filename
        except ClientError as e:
            logger.error(
                "Cannot connect to the minio {}. Please vefify the Credentials.".format(
                    self.url
                )
            )
        except Exception as e:
            logger.error("ex : {}".format(e))
