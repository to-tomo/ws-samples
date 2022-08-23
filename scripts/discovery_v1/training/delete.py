"""
Watson Discovery V1 API
    05. トレーニングクエリの削除
    08. トレーニングクエリ例の削除
"""

import logging
import pandas as pd
from requests import Response
import sys

from ibm_cloud_sdk_core.api_exception import ApiException
from ibm_watson import DiscoveryV1

import config
from helper import authentication_v1
from list import list_training_data_v1


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pd.set_option("display.max_columns", 50)
pd.set_option("display.width", 1000)


def delete_training_data_v1(
        discovery: DiscoveryV1,
        environment_id: str,
        collection_id: str,
        query_id: str) -> Response:
    """
    指定されたトレーニングクエリを削除
    MEMO: https://cloud.ibm.com/apidocs/discovery?code=python#deletetrainingdata  # noqa: E501
    """

    response = discovery.delete_training_data(
        environment_id=environment_id,
        collection_id=collection_id,
        query_id=query_id
        ).get_result()
    return response


def delete_training_example_v1(
        discovery: DiscoveryV1,
        environment_id: str,
        collection_id: str,
        query_id: str,
        example_id: str) -> Response:
    """
    指定されたトレーニングクエリ例を削除
    MEMO: https://cloud.ibm.com/apidocs/discovery?code=python#deletetrainingexample  # noqa: E501
    """

    response = discovery.delete_training_example(
        environment_id=environment_id,
        collection_id=collection_id,
        query_id=query_id,
        example_id=example_id
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
        list_response = list_training_data_v1(
            discovery=discovery,
            environment_id=environment_id,
            collection_id=collection_id)
        # 08. トレーニングクエリ例の削除
        # NOTE: 代表的な1件目の query_id に対象に delete_training_example_v1() を実行
        #       代表的な1件目の document_id に対象に delete_training_example_v1() を実行
        query_id = list_response["queries"][0]["query_id"]
        example_id = list_response["queries"][0]["examples"][0]["document_id"]
        delete_training_example_v1(
            discovery=discovery,
            environment_id=environment_id,
            collection_id=collection_id,
            query_id=query_id,
            example_id=example_id)
        logger.info(f"deleted training example. | query_id: {query_id}, example_id: {example_id}")  # noqa: E501
        # 05. トレーニングクエリの削除
        query_id = list_response["queries"][0]["query_id"]
        delete_training_data_v1(
            discovery=discovery,
            environment_id=environment_id,
            collection_id=collection_id,
            query_id=query_id)
        logger.info(f"deleted training data. | query_id: {query_id}")
    except ApiException:
        logger.exception("Api exception.")
        sys.exit(1)
    except Exception:
        logger.exception("Unexpected exception.")
        sys.exit(1)
