import base64
import os
from dataclasses import dataclass, field
from functools import cached_property
from typing import Optional

from boto3 import Session
from boto3.exceptions import Boto3Error
from botocore.exceptions import BotoCoreError
from fastapi import HTTPException
from glob_utils._proxy import LazyProxy  # type: ignore

from kubernetes import config  # type: ignore

AWS_EXCEPTIONS = {
    "Boto3Error": 500,
    "BotoCoreError": 500,
    "ClientError": 400,
    "NoCredentialsError": 401,
    "NoRegionError": 400,
    "ParamValidationError": 400,
    "PartialCredentialsError": 401,
    "ProfileNotFound": 400,
    "UnknownSignatureVersionError": 400,
    "UnsupportedSignatureVersionError": 400,
}


@dataclass
class AWSClient(LazyProxy[Session]):
    """
    AWS client.

    Attributes:
            region_name (str): The AWS region name.
            endpoint_url (Optional[str]): The AWS endpoint URL.
    """

    region_name: str = field(default=os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
    endpoint_url: Optional[str] = field(default=os.getenv("AWS_ENDPOINT_URL", None))

    def __load__(self) -> Session:
        """
        Load the AWS session.

        Returns:
                Session: The AWS session.
        """
        return Session(region_name=self.region_name)

    @cached_property
    def eks(self):
        """
        Get the Amazon Elastic Kubernetes Service (EKS) client.

        Returns:
                botocore.client.EKS: The EKS client.
        """
        return self.__load__().client(service_name="eks", endpoint_url=self.endpoint_url)  # type: ignore

    @cached_property
    def s3(self):
        """
        Get the Amazon Simple Storage Service (S3) client.

        Returns:
                botocore.client.S3: The S3 client.
        """
        return self.__load__().client(service_name="s3", endpoint_url=self.endpoint_url)  # type: ignore

    @cached_property
    def iam(self):
        """
        Get the AWS Identity and Access Management (IAM) client.

        Returns:
                botocore.client.IAM: The IAM client.
        """
        return self.__load__().client(service_name="iam", endpoint_url=self.endpoint_url)  # type: ignore

    @cached_property
    def ec2(self):
        """
        Get the Amazon Elastic Compute Cloud (EC2) client.

        Returns:
                botocore.client.EC2: The EC2 client.
        """
        return self.__load__().client(service_name="ec2", endpoint_url=self.endpoint_url)  # type: ignore

    @cached_property
    def ddb(self):
        """
        Get the Amazon DynamoDB client.

        Returns:
                botocore.client.DynamoDB: The DynamoDB client.
        """
        return self.__load__().client(service_name="dynamodb", endpoint_url=self.endpoint_url)  # type: ignore

    @cached_property
    def acm(self):
        """
        Get the AWS Certificate Manager (ACM) client.

        Returns:
                botocore.client.ACM: The ACM client.
        """
        return self.__load__().client(service_name="acm", endpoint_url=self.endpoint_url)  # type: ignore

    @cached_property
    def route53(self):
        """
        Get the Amazon Route 53 client.

        Returns:
                botocore.client.Route53: The Route 53 client.
        """
        return self.__load__().client(service_name="route53", endpoint_url=self.endpoint_url)  # type: ignore

    def get_k8s_credentials(self) -> dict[str, str]:
        """
        Gets the headers using `kubernetes` package by loading the kube config.

        Returns:
                dict[str, str]: The headers for API requests.
        """
        config.load_kube_config()  # type: ignore
        headers = config.kube_config.ApiClient().configuration.__dict__["api_key"]  # type: ignore
        return headers  # type: ignore

    def get_k8s_certificates(self, cluster_name: str) -> str:
        """
        Gets the certificates for the cluster.

        Args:
                cluster_name (str): The name of the cluster.

        Returns:
                str: The certificates for the cluster.
        """
        try:
            cluster = self.eks.describe_cluster(name=cluster_name)  # type: ignore
            data = cluster["cluster"]["certificateAuthority"]["data"]  # type: ignore
            assert isinstance(data, str)
            return base64.b64decode(data).decode("utf-8")
        except (BotoCoreError, Boto3Error) as exc:
            raise HTTPException(
                status_code=AWS_EXCEPTIONS.get(exc.__class__.__name__, 500),
                detail=str(exc.fmt) if hasattr(exc, "fmt") else str(exc),  # type: ignore
            ) from exc
