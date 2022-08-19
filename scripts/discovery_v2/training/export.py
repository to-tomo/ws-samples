"""
Watson Discovery V2 API を使用して training 用 CSV ファイルの出力
"""

import logging
import pandas as pd
import sys
from typing import List

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core.api_exception import ApiException
from ibm_watson import DiscoveryV2


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


def list_training_queries_v2(
    discovery: DiscoveryV2,
    project_id: str
        ) -> List:
    """
    training query 一覧表示処理の実行し queries を返す
    MEMO: https://cloud.ibm.com/apidocs/discovery-data?cm_sp=ibmdev-_-developer-articles-_-cloudreg&code=python#listtrainingqueries  # noqa: E501
    """

    response = discovery.list_training_queries(
        project_id=project_id
        ).get_result()
    return response["queries"]


def convert_to_csv(file_name: str, queries: List) -> None:
    """
    DetailedResponse を csv ファイルに変換
    """

    columns = ["num_queries", "natural_language_query", "num_examples", "examples_document_id", "examples_relevance"]  # noqa: E501
    df_csv = pd.DataFrame(columns=columns)
    # queries のループ処理
    for i in range(len(queries)):
        nl_query = queries[i]["natural_language_query"]
        # examples のループ処理
        examples = queries[i]["examples"]
        for j in range(len(examples)):
            df_data = pd.DataFrame(
                data=[[i, nl_query, j, examples[j]["document_id"], examples[j]["relevance"]]],  # noqa: E501
                columns=columns)
            df_csv = pd.concat([df_csv, df_data], ignore_index=True, axis=0)
    df_csv.to_csv(file_name, encoding='utf-8-sig', index=True)


if __name__ == "__main__":
    # ご自身の環境に合わせて修正
    api_key_v2 = "<your api key>"
    # IBM Cloud 画面 URLの https://jp-tok.discovery.watson.cloud.ibm.com/v2/instances/(省略)/projects/<your project id>/workspace から抜粋  # noqa: E501
    project_id = "<your project id>"
    # URL の構造明示のため分解
    host = "api.jp-tok.discovery.watson.cloud.ibm.com"
    instance_id = "<your instance id>"
    url = f"https://{host}/instances/{instance_id}"
    training_file = "v2_training_data.csv"  # 0-499 の 500 レコード

    try:
        discovery = authentication_v2(api_key_v2, url)
        logger.info("authenticated.")
        queries = list_training_queries_v2(
            discovery=discovery,
            project_id=project_id
        )
        logger.info("listed training queries.")
        convert_to_csv(training_file, queries)
        logger.info("converted response to csv.")
    except ApiException:
        logger.exception("Api exception.")
        sys.exit(1)
    except Exception:
        logger.exception("Unexpected exception.")
        sys.exit(1)
