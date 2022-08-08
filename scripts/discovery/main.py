"""
Watson Discovery V2 API を使用して検索実行
"""

import json
import logging
import sys
from ibm_watson import DiscoveryV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def authentication_v2(api_key: str, version: str) -> DiscoveryV2:
    """
    Watson Discovery の認証
    MEMO: https://cloud.ibm.com/apidocs/discovery-data?code=python#disabling-ssl  # noqa: E501
    """
    # URL の構造明示のため分解
    region = "<your region>"
    instance_id = "<your instance_id>"
    url = f"https://api.{region}.discovery.watson.cloud.ibm.com/instances/{instance_id}"  # noqa: E501
    authenticator = IAMAuthenticator(api_key)
    discovery = DiscoveryV2(
        version=version,
        authenticator=authenticator
        )
    discovery.set_service_url(url)
    return discovery


def query_v2(
    discovery: DiscoveryV2,
    project_id: str,
    query: str = None,
    natural_language_query: str = None
        ) -> str:
    """
    query 検索 or 自然言語 query の実行
    MEMO: https://cloud.ibm.com/apidocs/discovery-data?code=python#query
    """
    response = discovery.query(
        project_id=project_id,
        query=query,
        natural_language_query=natural_language_query
        ).get_result()
    return json.dumps(response, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    api_key_v2 = "your api key"
    version_v2 = "2020-08-30"
    # https://<region>.discovery.watson.cloud.ibm.com/v2/instances/(省略)/projects/<your project id>/workspace から抜粋  # noqa: E501
    project_id = "<your project id>"
    try:
        discovery = authentication_v2(api_key_v2, version_v2)
        logger.info("authenticated")
        query = "日本"
        jsonized_response = query_v2(
            discovery,
            project_id,
            query=query
        )
        logger.info(f"********** respose of query ********** :\n{jsonized_response}")  # noqa: E501
        natural_language_query = "日本"
        jsonized_response = query_v2(
            discovery,
            project_id,
            natural_language_query=natural_language_query
        )
        logger.info(f"********** respose of natural_language_query  ********** :\n{jsonized_response}")  # noqa: E501
    except Exception:
        logger.exception("Unexpected exception.")
        sys.exit(1)
