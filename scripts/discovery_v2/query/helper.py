"""
Watson Discovery V2 API 関連のヘルパー
"""

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import DiscoveryV2


def authentication_v2(api_key: str, url: str) -> DiscoveryV2:
    """
    Watson Discovery の認証
    MEMO: https://cloud.ibm.com/apidocs/discovery-data?code=python#authentication-cloud  # noqa: E501
    """

    authenticator = IAMAuthenticator(api_key)
    discovery = DiscoveryV2(
        version="2020-08-30",
        authenticator=authenticator
        )
    discovery.set_service_url(url)
    return discovery
