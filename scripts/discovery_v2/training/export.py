"""
Watson Discovery V2 API のトレーニング用 CSV ファイル出力
"""

import logging
import pandas as pd
import sys
from typing import List

from ibm_cloud_sdk_core.api_exception import ApiException

from helper import authentication_v2
from list import list_training_queries_v2


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pd.set_option("display.max_columns", 50)
pd.set_option("display.width", 1000)


def convert_to_csv(file_name: str, queries: List) -> None:
    """
    クエリのリストを csv ファイルに出力
    """

    columns = ["num_queries", "natural_language_query", "num_examples", "examples_document_id", "examples_relevance"]  # noqa: E501
    df_csv = pd.DataFrame(columns=columns)
    for i in range(len(queries)):
        nl_query = queries[i]["natural_language_query"]
        examples = queries[i]["examples"]
        for j in range(len(examples)):
            df_data = pd.DataFrame(
                data=[[i, nl_query, j, examples[j]["document_id"], examples[j]["relevance"]]],  # noqa: E501
                columns=columns)
            df_csv = pd.concat([df_csv, df_data], ignore_index=True, axis=0)
    df_csv.to_csv(file_name, encoding='utf-8-sig', index=True)


if __name__ == "__main__":
    # ご自身の環境に合わせて修正
    # IBM Cloud 画面: 管理 -> 資格情報 -> API 鍵 よりコピー
    api_key_v2 = "<your api key>"
    # IBM Cloud 画面: 自分のプロジェクト -> Integrate and deploy -> API Information で確認可能
    project_id = "<your project id>"
    # IBM Cloud 画面: 管理 -> 資格情報 -> URL よりコピー
    url = "<your url>"
    training_file = "v2_training_data.csv"

    try:
        discovery = authentication_v2(api_key_v2, url)
        logger.info("authenticated.")
        list_response = list_training_queries_v2(
            discovery=discovery,
            project_id=project_id)
        logger.info("listed training queries.")
        convert_to_csv(training_file, list_response["queries"])
        logger.info("converted response to csv.")
    except ApiException:
        logger.exception("Api exception.")
        sys.exit(1)
    except Exception:
        logger.exception("Unexpected exception.")
        sys.exit(1)
