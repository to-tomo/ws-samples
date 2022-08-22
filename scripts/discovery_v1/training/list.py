"""
Watson Discovery V1 API
    01. トレーニングデータのリスト
    04. トレーニングデータクエリの詳細取得
    06. トレーニングデータクエリ例のリスト
    10. トレーニングデータ例の詳細取得
MEMO: 前提としてトレーニングクエリの追加が実施済みであること
"""

import logging
import pandas as pd
from requests import Response
import sys

from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.api_exception import ApiException

from helper import authentication_v1
from utils import json_dumps


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pd.set_option("display.max_columns", 50)
pd.set_option("display.width", 1000)


def list_training_data_v1(
        discovery: DiscoveryV1,
        environment_id: str,
        collection_id: str) -> Response:
    """
    指定されたコレクションのトレーニングクエリを一覧表示
    MEMO: https://cloud.ibm.com/apidocs/discovery?code=python#listtrainingdata  # noqa: E501
    """

    response = discovery.list_training_data(
        environment_id=environment_id,
        collection_id=collection_id
        ).get_result()
    return response


def get_training_data_v1(
        discovery: DiscoveryV１,
        environment_id: str,
        collection_id: str,
        query_id: str) -> Response:
    """
    クエリ文字列とすべての例を含む、特定のトレーニングクエリの詳細を取得
    MEMO: https://cloud.ibm.com/apidocs/discovery?code=python#gettrainingdata  # noqa: E501
    """

    response = discovery.get_training_data(
        environment_id=environment_id,
        collection_id=collection_id,
        query_id=query_id
        ).get_result()
    return response


def list_training_examples_v1(
        discovery: DiscoveryV１,
        environment_id: str,
        collection_id: str,
        query_id: str) -> Response:
    """
    トレーニングクエリ例を一覧表示
    MEMO: https://cloud.ibm.com/apidocs/discovery?code=python#listtrainingexamples  # noqa: E501
    """

    response = discovery.list_training_examples(
        environment_id=environment_id,
        collection_id=collection_id,
        query_id=query_id
        ).get_result()
    return response


def get_training_example_v1(
        discovery: DiscoveryV１,
        environment_id: str,
        collection_id: str,
        query_id: str,
        example_id: str) -> Response:
    """
    トレーニングクエリ例の詳細取得
    MEMO: https://cloud.ibm.com/apidocs/discovery?code=python#gettrainingexample  # noqa: E501
    """

    response = discovery.get_training_example(
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
    # IBM Cloud 画面: 管理 -> 資格情報 -> URL よりコピー
    url = "<your url>"
    try:
        discovery = authentication_v1(api_key_v1, url)
        logger.info("authenticated.")
        # 1. トレーニングデータのリスト
        list_data_response = list_training_data_v1(
                discovery=discovery,
                environment_id=environment_id,
                collection_id=collection_id)
        logger.info(f"********** respose of list_training_data_v1() ********** :\n{json_dumps(list_data_response)}")  # noqa: E501
        # 4. トレーニングデータクエリの詳細取得
        # NOTE: 代表的な1件目の query_id に対象に get_training_data_v1() / list_training_examples_v1() を実行  # noqa: E501
        query_id = list_data_response["queries"][0]["query_id"]
        get_data_response = get_training_data_v1(
            discovery=discovery,
            environment_id=environment_id,
            collection_id=collection_id,
            query_id=query_id)
        logger.info(f"********** respose of get_training_data_v1() ********** :\n{json_dumps(get_data_response)}")  # noqa: E501
        # 6. トレーニングデータクエリ例のリスト
        list_example_response = list_training_examples_v1(
            discovery=discovery,
            environment_id=environment_id,
            collection_id=collection_id,
            query_id=query_id)
        logger.info(f"********** respose of list_training_examples_v1() ********** :\n{json_dumps(list_example_response)}")  # noqa: E501
        # 10. トレーニングデータ例の詳細取得
        # NOTE: 代表的な1件目の example_id に対象に get_training_example_v1() を実行
        example_id = list_example_response["examples"][0]["document_id"]
        get_example_response = get_training_example_v1(
            discovery=discovery,
            environment_id=environment_id,
            collection_id=collection_id,
            query_id=query_id,
            example_id=example_id)
        logger.info(f"********** respose of get_training_example_v1() ********** :\n{json_dumps(get_example_response)}")  # noqa: E501
    except ApiException:
        logger.exception("Api exception.")
        sys.exit(1)
    except Exception:
        logger.exception("Unexpected exception.")
        sys.exit(1)
