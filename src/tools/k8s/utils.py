import base64

from boto3 import Session
from botocore.exceptions import ClientError


def get_headers() -> dict[str, str]:
    """
    Gets the headers using `kubernetes` package by loading the kube config.

    Returns:
        dict[str, str]: The headers for API requests.
    """
    from kubernetes import config  # pylint: disable=C0415 # type: ignore

    config.load_kube_config()  # type: ignore
    headers = config.kube_config.ApiClient().configuration.__dict__["api_key"]  # type: ignore
    return headers  # type: ignore


def get_certificates(cluster_name: str, session: Session) -> str:
    """
    Gets the certificates for the cluster.

    Args:
        cluster_name (str): The name of the cluster.
        session (Session): The boto3 session.

    Returns:
        str: The certificates for the cluster.
    """
    eks = session.client(service_name="eks")  # type: ignore
    try:
        cluster = eks.describe_cluster(name=cluster_name)  # type: ignore
        data = cluster["cluster"]["certificateAuthority"]["data"]  # type: ignore
        assert isinstance(data, str)
        return base64.b64decode(data).decode("utf-8")
    except ClientError as e:
        raise ClientError(
            error_response=e.response, operation_name=e.operation_name
        ) from e
