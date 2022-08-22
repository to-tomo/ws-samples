"""
Watson Discovery V2 API
    01. トレーニングデータのリスト
    04. トレーニングデータクエリの詳細取得
    06. トレーニングデータクエリ例のリスト
    10. トレーニングデータ例の詳細取得
MEMO: 前提としてトレーニングデータへのクエリ追加処理を実施済みであること
"""

import logging
import pandas as pd
from requests import Response
import sys

from ibm_cloud_sdk_core.api_exception import ApiException
from ibm_watson import DiscoveryV2

from helper import authentication_v2
from utils import json_dumps


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pd.set_option("display.max_columns", 50)
pd.set_option("display.width", 1000)


def list_training_queries_v2(
        discovery: DiscoveryV2,
        project_id: str) -> Response:
    """
    指定されたプロジェクトのトレーニングクエリを一覧表示
    MEMO: https://cloud.ibm.com/apidocs/discovery-data?code=python#listtrainingqueries  # noqa: E501
    """

    response = discovery.list_training_queries(
        project_id=project_id
        ).get_result()
    return response


def get_training_query_v2(
        discovery: DiscoveryV2,
        project_id: str,
        query_id: str) -> Response:
    """
    クエリ文字列とすべての例を含む、特定のトレーニングクエリの詳細を取得
    MEMO: https://cloud.ibm.com/apidocs/discovery-data?code=python#gettrainingquery  # noqa: E501
    """

    response = discovery.get_training_query(
        project_id=project_id,
        query_id=query_id
        ).get_result()
    return response


if __name__ == "__main__":
    # ご自身の環境に合わせて修正
    # IBM Cloud 画面: 管理 -> 資格情報 -> API 鍵 よりコピー
    # api_key_v2 = "<your api key>"
    api_key_v2 = "FBGigKC8wDQ2O-fN-AID-zrJeMaaLSnMY6rq5bvZsUX4"
    # IBM Cloud 画面: 自分のプロジェクト -> Integrate and deploy -> API Information で確認可能
    # project_id = "<your project id>"
    project_id = "7e3ae262-db94-42bc-9942-1cb9ec59fd7a"
    # IBM Cloud 画面: 管理 -> 資格情報 -> URL よりコピー
    # url = "<your url>"
    url = "https://api.jp-tok.discovery.watson.cloud.ibm.com/instances/ae6d7a25-0647-42b2-8993-257539ef4b38"  # noqa: E501
    try:
        discovery = authentication_v2(api_key_v2, url)
        logger.info("authenticated.")
        # 1. トレーニングデータのリスト
        list_response = list_training_queries_v2(
                discovery=discovery,
                project_id=project_id)
        logger.info(f"********** respose of list_training_queries_v2() ********** :\n{json_dumps(list_response)}")  # noqa: E501
        # 4. トレーニングデータクエリの詳細取得 / 6. トレーニングデータクエリ例のリスト / 10. トレーニングデータ例の詳細取得
        # NOTE: 代表的な1件目の query_id に対象に get_training_query_queries_v2() を実行
        query_id = list_response["queries"][0]["query_id"]
        get_response = get_training_query_v2(
            discovery=discovery,
            project_id=project_id,
            query_id=query_id)
        logger.info(f"********** respose of get_training_query_v2() ********** :\n{json_dumps(get_response)}")  # noqa: E501
    except ApiException:
        logger.exception("Api exception.")
        sys.exit(1)
    except Exception:
        logger.exception("Unexpected exception.")
        sys.exit(1)
