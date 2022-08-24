"""
Watson Discovery V2 API
    1. コレクションの照会
    2. 複数のコレクションを照会
    3. システム通知の照会
    4. 複数収集システム通知の照会
    5. オートコンプリート候補の取得 NOTE: Cloud Pak 版のみ有効であるため未確認
"""

import logging
from requests import Response
from typing import List
import sys

from ibm_cloud_sdk_core.api_exception import ApiException
from ibm_watson import DiscoveryV2
from ibm_watson.discovery_v2 import QueryLargeTableResults, QueryLargeSuggestedRefinements, QueryLargePassages  # noqa: E501


import config
from helper import authentication_v2
from utils import json_dumps


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def query_v2(
        discovery: DiscoveryV2,
        project_id: str,
        collection_ids: List[str] = None,
        filter: str = None,
        query: str = None,
        natural_language_query: str = None,
        aggregation: str = None,
        count: int = None,
        return_: List[str] = None,
        offset: int = None,
        sort: str = None,
        highlight: bool = None,
        spelling_suggestions: bool = None,
        table_results: QueryLargeTableResults = None,
        suggested_refinements: QueryLargeSuggestedRefinements = None,
        passages: QueryLargePassages = None) -> Response:
    """
    プロジェクトを照会
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
        spelling_suggestions=spelling_suggestions,
        table_results=table_results,
        suggested_refinements=suggested_refinements,
        passages=passages).get_result()
    return response


def query_collection_notices_v2(
        discovery: DiscoveryV2,
        project_id: str,
        collection_id: str,
        filter: str = None,
        query: str = None,
        natural_language_query: str = None,
        count: int = None,
        offset: int = None) -> Response:
    """
    コレクションのシステム通知を照会
    MEMO: https://cloud.ibm.com/apidocs/discovery-data?code=python#querycollectionnotices  # noqa: E50
    """

    response = discovery.query_collection_notices(
        project_id=project_id,
        collection_id=collection_id,
        filter=filter,
        query=query,
        natural_language_query=natural_language_query,
        count=count,
        offset=offset
        ).get_result()
    return response


def query_notices_v2(
        discovery: DiscoveryV2,
        project_id: str,
        filter: str = None,
        query: str = None,
        natural_language_query: str = None,
        count: int = None,
        offset: int = None) -> Response:
    """
    プロジェクトのシステム通知を照会
    MEMO: https://cloud.ibm.com/apidocs/discovery-data?code=python#querynotices
    """

    response = discovery.query_notices(
        project_id=project_id,
        filter=filter,
        query=query,
        natural_language_query=natural_language_query,
        count=count,
        offset=offset,
        ).get_result()
    return response


def get_autocompletion_v2(
        discovery: DiscoveryV2,
        project_id: str,
        prefix: str,
        collection_ids: List[str] = None,
        field: str = None,
        count: int = None) -> Response:
    """
    指定されたプリフィックスの補完クエリ候補を取得
    MEMO: https://cloud.ibm.com/apidocs/discovery-data?code=python#getautocompletion  # noqa: E50
    """

    response = discovery.get_autocompletion(
        project_id=project_id,
        prefix=prefix,
        collection_ids=collection_ids,
        field=field,
        count=count
        ).get_result()
    return response


if __name__ == "__main__":
    api_key_v2 = config.api_key_v2
    project_id = config.project_id
    collection_id = config.collection_id
    url = config.url
    passages = {
        # v1 API と同じ動作
        "v1": QueryLargePassages(
            enabled=True,
            fields=None,
            count=10,
            characters=50,
            per_document=False),
        # v2 API 追加機能: per_document が有効
        "v2_per_document": QueryLargePassages(
            enabled=True,
            fields=None,
            count=10,
            characters=50,
            per_document=True,
            max_per_document=1),
        # v2 API 追加機能: find_answers が有効
        "v2_find_answers": QueryLargePassages(
            enabled=True,
            fields=None,
            count=10,
            characters=50,
            per_document=True,
            max_per_document=1,
            find_answers=True,
            max_answers_per_passage=1)
    }
    try:
        discovery = authentication_v2(api_key_v2, url)
        logger.info("authenticated.")
        # 1. コレクションの照会
        query_response = query_v2(
            discovery=discovery,
            project_id=project_id,
            collection_ids=[collection_id],
            natural_language_query="スマートフォン",
            count=1,
            passages=passages["v1"])
        logger.info(f"********** respose of query_v2-1 ********** :\n{json_dumps(query_response)}")  # noqa: E501
        # 2. 複数のコレクションを照会
        query_response = query_v2(
            discovery=discovery,
            project_id=project_id,
            natural_language_query="スマートフォン",
            count=1,
            passages=passages["v1"])
        logger.info(f"********** respose of query_v2-2 ********** :\n{json_dumps(query_response)}")  # noqa: E501
        # 3. システム通知の照会
        query_response = query_collection_notices_v2(
            discovery=discovery,
            project_id=project_id,
            collection_id=collection_id)
        logger.info(f"********** respose of query_collection_notices_v2 ********** :\n{json_dumps(query_response)}")  # noqa: E501
        # 4. 複数収集システム通知の照会
        query_response = query_notices_v2(
            discovery=discovery,
            project_id=project_id)
        logger.info(f"********** respose of query_notices_v2 ********** :\n{json_dumps(query_response)}")  # noqa: E501
    except ApiException:
        logger.exception("Api exception.")
        sys.exit(1)
    except Exception:
        logger.exception("Unexpected exception.")
        sys.exit(1)
