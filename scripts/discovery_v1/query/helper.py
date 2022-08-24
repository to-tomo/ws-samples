"""
Watson Discovery V1 API 関連のヘルパー
"""

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import DiscoveryV1


def authentication_v1(api_key: str, url: str) -> DiscoveryV1:
    """
    Watson Discovery の認証
    MEMO: https://cloud.ibm.com/apidocs/discovery-data?code=python#authentication-cloud  # noqa: E501
    """

    authenticator = IAMAuthenticator(api_key)
    discovery = DiscoveryV1(
        version="2019-04-30",
        authenticator=authenticator
        )
    discovery.set_service_url(url)
    return discovery
