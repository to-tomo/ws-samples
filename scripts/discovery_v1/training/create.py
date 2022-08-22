"""
Watson Discovery V1 API
    02. トレーニングクエリの追加
    07. トレーニングクエリ例の追加
"""

import logging
import pandas as pd
from requests import Response
import sys
from typing import List

from ibm_cloud_sdk_core.api_exception import ApiException
from ibm_watson import DiscoveryV1
from ibm_watson.discovery_v1 import TrainingExample

from helper import authentication_v1, conver_df_to_training_exaples
from utils import json_dumps


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pd.set_option("display.max_columns", 50)
pd.set_option("display.width", 1000)


def add_training_data_v1(
        discovery: DiscoveryV1,
        environment_id: str,
        collection_id: str,
        natural_language_query: str,
        filter: str = None,
        examples: List[TrainingExample] = None) -> Response:
    """
    トレーニングクエリを作成
    MEMO: https://cloud.ibm.com/apidocs/discovery#addtrainingdata  # noqa: E501
    """

    response = discovery.add_training_data(
        environment_id=environment_id,
        collection_id=collection_id,
        natural_language_query=natural_language_query,
        filter=filter,
        examples=examples
        ).get_result()
    return response


def create_training_example_v1(
        discovery: DiscoveryV1,
        environment_id: str,
        collection_id: str,
        query_id: str,
        document_id: str,
        cross_reference: str,
        relevance: int) -> Response:
    """
    トレーニングクエリ例を追加
    MEMO: https://cloud.ibm.com/apidocs/discovery?code=python#createtrainingexample  # noqa: E501
    """

    response = discovery.create_training_example(
        environment_id=environment_id,
        collection_id=collection_id,
        query_id=query_id,
        document_id=document_id,
        cross_reference=cross_reference,
        relevance=relevance
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
    training_file = "v1_training_data.csv"
    num_queries_len = 1  # training_file 内の num_queries の最大数に変更
    try:
        discovery = authentication_v1(api_key_v1, url)
        logger.info("authenticated.")
        # MEMO: training_file からトレーニングクエリを追加する場合
        # トレーニング用 CSV ファイルの読み込み
        df = pd.read_csv(training_file)
        logger.info(f"read [{training_file}].")
        # num_queries のループ処理
        for i in range(num_queries_len):
            df_per_num_queries = df.query(f"num_queries =={i}")
            natural_language_query, examples = conver_df_to_training_exaples(df_per_num_queries)  # noqa: E501
            logger.info(f"prepared data. | natural_language_query: {natural_language_query}, examples:\n {examples}")  # noqa: E501
            # 2. トレーニングクエリの追加
            add_response = add_training_data_v1(
                discovery=discovery,
                environment_id=environment_id,
                collection_id=collection_id,
                natural_language_query=natural_language_query,
                examples=examples)
            logger.info(f"********** respose of add_training_data_v1() {i} ********** :\n{json_dumps(add_response)}")  # noqa: E501
        # MEMO: 手作業でトレーニングクエリを追加する場合
        """
        # 2. トレーニングクエリの追加
        # document_id を IBM Watson Discovery 画面 より転記
        # natural_language_query, cross_reference, relevance に任意の値を設定  # noqa: E501
        natural_language_query = "ハローキティ"
        examples = [TrainingExample(
            document_id="73bacbd1c545057035827ddaa32fac24",
            cross_reference="スマートフォン",
            relevance=10)]
        add_response = add_training_data_v1(
            discovery=discovery,
            environment_id=environment_id,
            collection_id=collection_id,
            natural_language_query=natural_language_query,
            examples=examples)
        logger.info(f"********** respose of add_training_data_v1() ********** :\n{json_dumps(add_response)}")  # noqa: E501
        """
        # 7. トレーニングクエリ例の追加
        # document_id を IBM Watson Discovery 画面 より転記
        # cross_reference, relevance に任意の値を設定
        query_id = add_response["query_id"]
        document_id = "73bacbd1c545057035827ddaa32fac24"
        cross_reference = "スマートフォン"
        relevance = 10
        create_example_response = create_training_example_v1(
            discovery=discovery,
            environment_id=environment_id,
            collection_id=collection_id,
            query_id=query_id,
            document_id=document_id,
            cross_reference=cross_reference,
            relevance=relevance)
        logger.info(f"********** respose of create_training_example_v1() ********** :\n{json_dumps(create_example_response)}")  # noqa: E501
    except ApiException:
        logger.exception("Api exception.")
        sys.exit(1)
    except Exception:
        logger.exception("Unexpected exception.")
        sys.exit(1)
