from functools import cached_property  # type: ignore
from typing import Any

from boto3 import client  # type: ignore
from glob_utils import async_io, robust  # type: ignore
from glob_utils.apiClient import LazyProxy  # type: ignore


class StorageBucket(LazyProxy[Any]):
    """
    Represents a storage bucket for storing and retrieving objects.
    """

    def __load__(self):
        """
        Loads the S3 client.
        """
        return client("s3")

    @cached_property
    def client(self):
        """
        Returns the S3 client.
        """
        return self.__load__()

    @robust
    @async_io
    def upload(self, *, body: bytes, key: str, content_type: str):
        """
        Uploads an object to the storage bucket.

        Args:
                body (bytes): The content of the object to upload.
                key (str): The key or name of the object.

        Returns:
                str: The URL of the uploaded object.
        """
        self.client.put_object(
            Bucket="aws-call-4-speakers", Body=body, Key=key, ContentType=content_type
        )
        return self.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": "aws-call-4-speakers", "Key": key},
            ExpiresIn=86400,
        )

    @robust
    @async_io
    def get(self, *, key: str):
        """
        Retrieves the URL of an object in the storage bucket.

        Args:
                key (str): The key or name of the object.

        Returns:
                str: The URL of the object.
        """
        return self.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": "aws-call-4-speakers", "Key": key},
            ExpiresIn=86400,
        )

    @robust
    @async_io
    def delete(self, *, key: str):
        """
        Deletes an object from the storage bucket.

        Args:
                key (str): The key or name of the object.

        Returns:
                bool: True if the object was successfully deleted, False otherwise.
        """
        self.client.delete_object(Bucket="aws-call-4-speakers", Key=key)
        return True

    @robust
    @async_io
    def list(self, *, prefix: str):
        """
        Lists objects in the storage bucket with the specified prefix.

        Args:
                prefix (str): The prefix to filter the object keys.

        Returns:
                List[Dict[str, Any]]: A list of objects in the bucket matching the prefix.
        """
        return self.client.list_objects(Bucket="aws-call-4-speakers", Prefix=prefix)[
            "Contents"
        ]
