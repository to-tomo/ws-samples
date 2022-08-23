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

import config
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
    api_key_v2 = config.api_key_v2
    project_id = config.project_id
    url = config.url
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
