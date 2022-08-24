"""
Watson Discovery V1 API
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
from ibm_watson import DiscoveryV1

import config
from helper import authentication_v1
from utils import json_dumps

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def query_v1(
        discovery: DiscoveryV1,
        environment_id: str,
        collection_id: str,
        filter: str = None,
        query: str = None,
        natural_language_query: str = None,
        passages: bool = None,
        aggregation: str = None,
        count: int = None,
        return_: List[str] = None,
        offset: int = None,
        sort: str = None,
        highlight: bool = None,
        passages_fields: str = None,
        passages_count: int = None,
        passages_characters: int = None,
        deduplicate: bool = None,
        deduplicate_field: str = None,
        similar: bool = None,
        similar_document_ids: str = None,
        similar_fields: str = None,
        bias: str = None,
        spelling_suggestions: bool = None,
        x_watson_logging_opt_out: bool = None) -> Response:
    """
    コレクションを照会
    MEMO: https://cloud.ibm.com/apidocs/discovery#queryusingget
    """

    response = discovery.query(
        environment_id=environment_id,
        collection_id=collection_id,
        filter=filter,
        query=query,
        natural_language_query=natural_language_query,
        passages=passages,
        aggregation=aggregation,
        count=count,
        return_=return_,
        offset=offset,
        sort=sort,
        highlight=highlight,
        passages_fields=passages_fields,
        passages_count=passages_count,
        passages_characters=passages_characters,
        deduplicate=deduplicate,
        deduplicate_field=deduplicate_field,
        similar=similar,
        similar_document_ids=similar_document_ids,
        similar_fields=similar_fields,
        bias=bias,
        spelling_suggestions=spelling_suggestions,
        x_watson_logging_opt_out=x_watson_logging_opt_out
        ).get_result()
    return response


def federated_query_v1(
        discovery: DiscoveryV1,
        environment_id: str,
        collection_ids: str,
        filter: str = None,
        query: str = None,
        natural_language_query: str = None,
        passages: bool = None,
        aggregation: str = None,
        count: int = None,
        return_: str = None,
        offset: int = None,
        sort: str = None,
        highlight: bool = None,
        passages_fields: str = None,
        passages_count: int = None,
        passages_characters: int = None,
        deduplicate: bool = None,
        deduplicate_field: str = None,
        similar: bool = None,
        similar_document_ids: str = None,
        similar_fields: str = None,
        bias: str = None,
        x_watson_logging_opt_out: bool = None) -> Response:
    """
    複数コレクションを照会
    MEMO: https://cloud.ibm.com/apidocs/discovery?code=python#federatedquery
    """

    response = discovery.federated_query(
        environment_id=environment_id,
        collection_ids=collection_ids,
        filter=filter,
        query=query,
        natural_language_query=natural_language_query,
        passages=passages,
        aggregation=aggregation,
        count=count,
        return_=return_,
        offset=offset,
        sort=sort,
        highlight=highlight,
        passages_fields=passages_fields,
        passages_count=passages_count,
        passages_characters=passages_characters,
        deduplicate=deduplicate,
        deduplicate_field=deduplicate_field,
        similar=similar,
        similar_document_ids=similar_document_ids,
        similar_fields=similar_fields,
        bias=bias,
        x_watson_logging_opt_out=x_watson_logging_opt_out
        ).get_result()
    return response


def query_notices_v1(
        discovery: DiscoveryV1,
        environment_id: str,
        collection_id: str,
        filter: str = None,
        query: str = None,
        natural_language_query: str = None,
        passages: bool = None,
        aggregation: str = None,
        count: int = None,
        return_: List[str] = None,
        offset: int = None,
        sort: List[str] = None,
        highlight: bool = None,
        passages_fields: List[str] = None,
        passages_count: int = None,
        passages_characters: int = None,
        deduplicate_field: str = None,
        similar: bool = None,
        similar_document_ids: List[str] = None,
        similar_fields: List[str] = None) -> Response:
    """
    コレクションのシステム通知を照会
    MEMO: https://cloud.ibm.com/apidocs/discovery?code=python#querynotices
    """

    response = discovery.query_notices(
        environment_id=environment_id,
        collection_id=collection_id,
        filter=filter,
        query=query,
        natural_language_query=natural_language_query,
        passages=passages,
        aggregation=aggregation,
        count=count,
        return_=return_,
        offset=offset,
        sort=sort,
        highlight=highlight,
        passages_fields=passages_fields,
        passages_count=passages_count,
        passages_characters=passages_characters,
        deduplicate_field=deduplicate_field,
        similar=similar,
        similar_document_ids=similar_document_ids,
        similar_fields=similar_fields
        ).get_result()
    return response


def federated_query_notices_v1(
        discovery: DiscoveryV1,
        environment_id: str,
        collection_ids: List[str],
        filter: str = None,
        query: str = None,
        natural_language_query: str = None,
        aggregation: str = None,
        count: int = None,
        return_: List[str] = None,
        offset: int = None,
        sort: List[str] = None,
        highlight: bool = None,
        deduplicate_field: str = None,
        similar: bool = None,
        similar_document_ids: List[str] = None,
        similar_fields: List[str] = None) -> Response:
    """
    複数コレクションのシステム通知を照会
    MEMO: https://cloud.ibm.com/apidocs/discovery?code=python#federatedquerynotices  # noqa: E501
    """

    response = discovery.federated_query_notices(
        environment_id=environment_id,
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
        deduplicate_field=deduplicate_field,
        similar=similar,
        similar_document_ids=similar_document_ids,
        similar_fields=similar_fields
        ).get_result()
    return response


def get_autocompletion_v1(
        discovery: DiscoveryV1,
        environment_id: str,
        collection_id: str,
        prefix: str,
        field: str = None,
        count: int = None) -> Response:
    """
    指定されたプリフィックスの補完クエリ候補を取得
    MEMO: https://cloud.ibm.com/apidocs/discovery?code=python#getautocompletion
    """

    response = discovery.get_autocompletion(
        environment_id=environment_id,
        collection_id=collection_id,
        prefix=prefix,
        field=field,
        count=count
        ).get_result()
    return response


if __name__ == "__main__":
    api_key_v1 = config.api_key_v1
    environment_id = config.environment_id
    collection_id = config.collection_id
    url = config.url
    try:
        discovery = authentication_v1(api_key_v1, url)
        logger.info("authenticated.")
        # 1. コレクションの照会
        query_response = query_v1(
            discovery=discovery,
            environment_id=environment_id,
            collection_id=collection_id,
            natural_language_query="スマートフォン",
            count=1,
            passages=True,
            passages_fields=None,
            passages_count=10,
            passages_characters=50)
        logger.info(f"********** respose of query_v1 ********** :\n{json_dumps(query_response)}")  # noqa: E50
        # 2. 複数のコレクションを照会
        federated_query_response = federated_query_v1(
            discovery=discovery,
            environment_id=environment_id,
            collection_ids=collection_id,
            natural_language_query="スマートフォン",
            count=1,
            passages=True,
            passages_fields=None,
            passages_count=10,
            passages_characters=50)
        logger.info(f"********** respose of federated_query_v1 ********** :\n{json_dumps(federated_query_response)}")  # noqa: E501
        # 3. システム通知の照会
        response = query_notices_v1(
            discovery=discovery,
            environment_id=environment_id,
            collection_id=collection_id,
            count=1)
        logger.info(f"********** respose of query_notices_v1 ********** :\n{json_dumps(response)}")  # noqa: E501
        # 4. 複数収集システム通知の照会
        response = federated_query_notices_v1(
            discovery=discovery,
            environment_id=environment_id,
            collection_ids=[collection_id],
            count=1)
        logger.info(f"********** respose of federated_query_notices_v1 ********** :\n{json_dumps(response)}")  # noqa: E501
    except ApiException:
        logger.exception("Api exception.")
        sys.exit(1)
    except Exception:
        logger.exception("Unexpected exception.")
        sys.exit(1)
