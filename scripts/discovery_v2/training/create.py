"""
Watson Discovery V2 API
    02. トレーニングクエリの追加
    07. トレーニングクエリ例の追加
"""

import logging
import pandas as pd
from requests import Response
import sys
from typing import List

from ibm_cloud_sdk_core.api_exception import ApiException
from ibm_watson import DiscoveryV2
from ibm_watson.discovery_v2 import TrainingExample

from helper import authentication_v2, conver_df_to_training_exaples
from list import get_training_query_v2
from utils import json_dumps


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pd.set_option("display.max_columns", 50)
pd.set_option("display.width", 1000)


def create_training_query_v2(
        discovery: DiscoveryV2,
        project_id: str,
        natural_language_query: str,
        examples: List['TrainingExample'],
        filter: str = None) -> Response:
    """
    プロジェクトのトレーニングクエリを追加
    クエリにはフィルターと自然言語クエリを含めることが出来る
    MEMO: https://cloud.ibm.com/apidocs/discovery-data#createtrainingquery  # noqa: E501
    """

    response = discovery.create_training_query(
        project_id=project_id,
        natural_language_query=natural_language_query,
        examples=examples,
        filter=filter
        ).get_result()
    return response


if __name__ == "__main__":
    # ご自身の環境に合わせて修正
    # IBM Cloud 画面: 管理 -> 資格情報 -> API 鍵 よりコピー
    api_key_v2 = "<your api key>"
    # IBM Cloud 画面: 自分のプロジェクト -> Integrate and deploy -> API Information で確認可能
    project_id = "<your project id>"
    # IBM Cloud 画面 URLの https://jp-tok.discovery.watson.cloud.ibm.com/v2/instances/(省略)/collections/<your collection id>/activity  # noqa: E501
    collection_id = "<your collection id>"
    # IBM Cloud 画面: 管理 -> 資格情報 -> URL よりコピー
    url = "<your url>"
    training_file = "v2_training_data.csv"
    num_queries_len = 2  # training_file 内の num_queries の最大数に変更
    try:
        discovery = authentication_v2(api_key_v2, url)
        logger.info("authenticated.")
        # トレーニング用 CSV ファイルの読み込み
        df = pd.read_csv(training_file)
        logger.info(f"read [{training_file}].")
        # num_queries のループ処理
        for i in range(num_queries_len):
            df_per_num_queries = df.query(f"num_queries =={i}")
            natural_language_query, examples = conver_df_to_training_exaples(collection_id, df_per_num_queries)  # noqa: E501
            logger.info(f"prepared data. | natural_language_query: {natural_language_query}, examples:\n {examples}")  # noqa: E501
            # 2. トレーニングクエリの追加 / 7. トレーニングクエリ例の追加
            create_response = create_training_query_v2(
                discovery=discovery,
                project_id=project_id,
                natural_language_query=natural_language_query,
                examples=examples)
            logger.info(f"********** respose of create_training_query_v2() {i} ********** :\n{json_dumps(create_response)}")  # noqa: E501
            query_id = create_response["query_id"]
            get_response = get_training_query_v2(
                    discovery=discovery,
                    project_id=project_id,
                    query_id=query_id)
            logger.info(f"********** respose of get_training_query_v2() {i} ********** :\n{json_dumps(get_response)}")  # noqa: E501
    except ApiException:
        logger.exception("Api exception.")
        sys.exit(1)
    except Exception:
        logger.exception("Unexpected exception.")
        sys.exit(1)
