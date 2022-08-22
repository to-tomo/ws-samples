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
    # ご自身の環境に合わせて修正
    # IBM Cloud 画面: 管理 -> 資格情報 -> API 鍵 よりコピー
    api_key_v1 = "<your api key>"
    # IBM Watson Discovery 画面 の右上の API アイコン -> Environment ID
    environment_id = "<your environment id>"
    # IBM Watson Discovery 画面 の右上の API アイコン -> Collection ID よりコピー
    collection_id = "<your collection id>"
    collection_id = "1425ab9a-126d-45cd-ac6c-4d3a0a561452"
    # IBM Cloud 画面: 管理 -> 資格情報 -> URL よりコピー
    url = "<your url>"
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
