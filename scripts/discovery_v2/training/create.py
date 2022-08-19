"""
Watson Discovery V2 API を使用して training query 作成
"""

import json
import logging
import pandas as pd
import sys
from typing import Any, List

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core.api_exception import ApiException
from ibm_watson import DiscoveryV2
from ibm_watson.discovery_v2 import TrainingExample


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pd.set_option("display.max_columns", 50)
pd.set_option("display.width", 1000)


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


def prepare_data(collection_id: str, df: pd.DataFrame) -> Any:
    """
    training data の準備
    """

    natural_language_query: str = None  # トレーニング クエリとして使用される自然テキストクエリ
    examples: List[TrainingExample] = []  # トレーニング例の配列
    for data in df.itertuples():
        training_example = TrainingExample(
            document_id=data.examples_document_id,
            collection_id=collection_id,
            relevance=data.examples_relevance
            )
        examples.append(training_example)
        # num_queries 毎に同一の natural_language_query になるため、そのまま上書き
        natural_language_query = data.natural_language_query
    return natural_language_query, examples


def create_training_query_v2(
    discovery: DiscoveryV2,
    project_id: str,
    natural_language_query: str,
    examples: List['TrainingExample'],
    filter: str = None
        ) -> Any:
    """
    training query 作成処理の実行
    MEMO: https://cloud.ibm.com/apidocs/discovery-data?cm_sp=ibmdev-_-developer-articles-_-cloudreg&code=python#createtrainingquery  # noqa: E501
    """

    response = discovery.create_training_query(
        project_id=project_id,
        natural_language_query=natural_language_query,
        examples=examples,
        filter=filter
        ).get_result()
    return json.dumps(response, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    # ご自身の環境に合わせて修正
    api_key_v2 = "<your api key>"
    # IBM Cloud 画面 URLの https://jp-tok.discovery.watson.cloud.ibm.com/v2/instances/(省略)/projects/<your project id>/workspace から抜粋  # noqa: E501
    project_id = "<your project id>"
    # IBM Cloud 画面 URLの https://jp-tok.discovery.watson.cloud.ibm.com/v2/instances/(省略)/collections/<your collection id>/activity  # noqa: E501
    collection_id = "<your collection id>"
    # URL の構造明示のため分解
    host = "api.jp-tok.discovery.watson.cloud.ibm.com"
    instance_id = "<your instance id>"
    url = f"https://{host}/instances/{instance_id}"

    training_file = "v2_training_data.csv"
    with open(training_file) as file:
        total_lines = sum(1 for _ in file)
    num_queries_len = total_lines - 2

    try:
        discovery = authentication_v2(api_key_v2, url)
        logger.info("authenticated.")
        # training 用 CSV ファイルの読み込み
        df = pd.read_csv(training_file)
        logger.info(f"read [{training_file}].")
        # num_queries のループ処理
        for i in range(num_queries_len):
            df_per_num_queries = df.query('num_queries =='+str(i))
            natural_language_query, examples = prepare_data(collection_id, df_per_num_queries)  # noqa: E501
            logger.info(f"prepared data. | natural_language_query: {natural_language_query}, examples:\n {examples}")  # noqa: E501
            jsonized_response = create_training_query_v2(
                discovery=discovery,
                project_id=project_id,
                natural_language_query=natural_language_query,
                examples=examples
            )
            logger.info(f"********** respose {i} ********** :\n{jsonized_response}")  # noqa: E501
    except ApiException:
        logger.exception("Api exception.")
        sys.exit(1)
    except Exception:
        logger.exception("Unexpected exception.")
        sys.exit(1)
