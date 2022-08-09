"""
Watson Discovery V2 API を使用して検索実行
"""

import json
import logging
from typing import Any, List
import sys
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import DiscoveryV2


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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


def query_v2(
    discovery: DiscoveryV2,
    project_id: str,
    collection_ids: List[str] = None,
    filter: str = None,
    query: str = None,
    natural_language_query: str = None,
    aggregation: str = None,
    count: int = 1,  # 暫定でデフォルト1件
    return_: List[str] = None,
    offset: int = None,
    sort: str = "+",  # 暫定でデフォルト昇順
    highlight: bool = None,
    spelling_suggestions: bool = None
        ) -> Any:
    """
    query 検索 or 自然言語 query の実行
    MEMO: https://cloud.ibm.com/apidocs/discovery-data?code=python#query
    """
    response = discovery.query(
        project_id=project_id,
        collection_ids=collection_ids,
        filter=filter,
        query=query,
        natural_language_query=natural_language_query,
        aggregation=aggregation,
        count=count,
        return_=return_,
        offset=offset,
        sort=sort,
        highlight=highlight,
        spelling_suggestions=spelling_suggestions
        ).get_result()
    return json.dumps(response, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    api_key_v2 = "<your api key>"
    # IBM Cloud 画面 URLの https://jp-tok.discovery.watson.cloud.ibm.com/v2/instances/(省略)/projects/<your project id>/workspace から抜粋  # noqa: E501
    project_id = "<your project id>"
    # URL の構造明示のため分解
    host = "api.jp-tok.discovery.watson.cloud.ibm.com"
    instance_id = "<your instance id>"
    url = f"https://{host}/instances/{instance_id}"
    try:
        discovery = authentication_v2(api_key_v2, url)
        logger.info("authenticated.")
        query = "日本"
        jsonized_response = query_v2(
            discovery=discovery,
            project_id=project_id,
            query=query
        )
        logger.info(f"********** respose of query ********** :\n{jsonized_response}")  # noqa: E501
        natural_language_query = "日本"
        jsonized_response = query_v2(
            discovery=discovery,
            project_id=project_id,
            natural_language_query=natural_language_query
        )
        logger.info(f"********** respose of natural_language_query ********** :\n{jsonized_response}")  # noqa: E501
    except Exception:
        logger.exception("Unexpected exception.")
        sys.exit(1)
