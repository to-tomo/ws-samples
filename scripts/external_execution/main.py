"""
外部から Watson Studio Cloud の Jupyter Notebook ジョブを実行
"""

import logging
import requests
import sys
import time


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_bearer_token(api_key: str) -> str:
    """
    ベアラートークン生成
    MEMO: https://cloud.ibm.com/docs/account?topic=account-iamtoken_from_apikey&interface=api  # noqa: E501
    """

    url = "https://iam.cloud.ibm.com/oidc/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "apikey": api_key,
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
        }
    # IAM トークン取得
    response = requests.post(
        url,
        headers=headers,
        data=payload,
    ).json()
    iam_token = response["access_token"]
    return f"Bearer {iam_token}"


def get_job_id(bearer_token: str, project_id: str, job_name: str) -> str:
    """
    Job ID 取得
    MEMO: https://cloud.ibm.com/apidocs/watson-data-api-cpd#jobs-list
    """

    url = f"https://api.dataplatform.cloud.ibm.com/v2/jobs?project_id={project_id}"  # noqa: E501
    headers = {
        "Authorization": bearer_token,
        "Content-Type": "application/json"
        }
    # Job list 取得
    response = requests.get(
        url,
        headers=headers
    ).json()
    # Job ID(=asset_id) 取得
    return next(
        v["metadata"]["asset_id"]for v in response["results"] if v["metadata"]["name"] == job_name  # noqa: E501
    )


def run_job(bearer_token: str, job_id: str, project_id: str) -> str:
    """
    Job 実行
    MEMO: https://cloud.ibm.com/apidocs/watson-data-api#job-runs-create
    """

    url = f"https://api.dataplatform.cloud.ibm.com/v2/jobs/{job_id}/runs?project_id={project_id}"  # noqa: E501
    headers = {
        "Authorization": bearer_token,
        "Content-Type": "application/json"
        }
    # Job 実行
    response = requests.post(
        url,
        headers=headers
    ).json()
    # Run ID(=asset_id) 取得
    return response["metadata"]["asset_id"]


def check_job_status(
        bearer_token: str, job_id: str, run_id: str, project_id: str
        ) -> str:
    """
    Job ステータス確認
    MEMO: https://cloud.ibm.com/apidocs/watson-data-api#job-runs-get
    """

    url = f"https://api.dataplatform.cloud.ibm.com/v2/jobs/{job_id}/runs/{run_id}?project_id={project_id}"  # noqa: E501
    heders = {
        "Authorization": bearer_token,
        "Content-Type": "application/json"
        }
    # Job ステータス取得
    response = requests.get(
        url,
        headers=heders
    ).json()
    return response["entity"]["job_run"]["state"]


if __name__ == "__main__":
    # 自身の環境に合わせて修正
    api_key = "<your api key>"
    job_name = "<your job name>"
    project_id = "<your project id>"

    bearer_token = generate_bearer_token(api_key)
    logger.info(f"Bearer token is [{bearer_token}].")
    job_id = get_job_id(bearer_token, project_id, job_name)
    logger.info(f"Job id is [{job_id}].")
    run_id = run_job(bearer_token, job_id, project_id)
    logger.info(f"Run id is [{run_id}].")
    retury_times = 12  # JOB ステータス確認リトライ回数
    retry_sleep = 6    # JOB ステータス確認 sleep 期間(秒)
    try:
        for i in range(retury_times):
            job_status = check_job_status(
                bearer_token, job_id, run_id, project_id
                )
            logger.info(f"Job status is [{job_status}].")
            # Job 完了確認
            if job_status == "Completed":
                logger.info("Completed.")
                sys.exit(0)
            time.sleep(retry_sleep)
            # タイムアウト確認
            if i == retury_times-1:
                raise TimeoutError()
    except TimeoutError:
        logger.exception("Timeout error.")
        sys.exit(1)
    except Exception:
        logger.exception("Unexpected exception.")
        sys.exit(1)
