"""
Watson Discovery V2 API
    全てのトレーニングクエリの削除
"""

import logging
import pandas as pd
from requests import Response
import sys

from ibm_cloud_sdk_core.api_exception import ApiException
from ibm_watson import DiscoveryV2

from helper import authentication_v2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pd.set_option("display.max_columns", 50)
pd.set_option("display.width", 1000)


def delete_training_queries_v2(
        discovery: DiscoveryV2,
        project_id: str) -> Response:
    """
    指定されたプロジェクトの全てのトレーニングクエリを削除
    MEMO: https://cloud.ibm.com/apidocs/discovery-data?code=python#deletetrainingqueries  # noqa: E501
    """

    response = discovery.delete_training_queries(
        project_id=project_id
        ).get_result()
    return response


if __name__ == "__main__":
    # ご自身の環境に合わせて修正
    # IBM Cloud 画面: 管理 -> 資格情報 -> API 鍵 よりコピー
    api_key_v2 = "<your api key>"
    # IBM Cloud 画面: 自分のプロジェクト -> Integrate and deploy -> API Information で確認可能
    project_id = "<your project id>"
    # IBM Cloud 画面: 管理 -> 資格情報 -> URL よりコピー
    url = "<your url>"
    try:
        discovery = authentication_v2(api_key_v2, url)
        logger.info("authenticated.")
        # 3. 全てのトレーニングクエリの削除
        response = delete_training_queries_v2(
                discovery=discovery,
                project_id=project_id)
        logger.info(f"deleted all training queries. | project_id: {project_id}")  # noqa: E501
    except ApiException:
        logger.exception("Api exception.")
        sys.exit(1)
    except Exception:
        logger.exception("Unexpected exception.")
        sys.exit(1)
