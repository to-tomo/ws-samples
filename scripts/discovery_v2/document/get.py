"""
Watson Discovery V2 API を使用してドキュメントの状態を取得
"""

import glob
import json
import logging
import sys
from typing import Any, List
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import DiscoveryV2


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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


def query_results_v2(
    discovery: DiscoveryV2,
    project_id: str,
    collection_ids: List[str] = None,
    filter: str = None,
    query: str = None,
    natural_language_query: str = None,
    aggregation: str = None,
    count: int = None,
    return_: List[str] = None,
    offset: int = None,
    sort: str = None,
    highlight: bool = None,
    spelling_suggestions: bool = None
        ) -> List:
    """
    results の取得
    MEMO: https://cloud.ibm.com/apidocs/discovery-data?code=python#query
    """
    response = discovery.query(
        project_id=project_id,
        collection_ids=collection_ids,
        filter=filter,
        query=query,
        natural_language_query=natural_language_query,
        aggregation=aggregation,
        count=count,
        return_=return_,
        offset=offset,
        sort=sort,
        highlight=highlight,
        spelling_suggestions=spelling_suggestions
        ).get_result()
    return response["results"]


def get_document_v2(
        discovery: DiscoveryV2,
        project_id: str,
        collection_id: str,
        document_id: str) -> Any:

    doc_info = discovery.get_document(
        project_id=project_id,
        collection_id=collection_id,
        document_id=document_id
    ).get_result()
    return json.dumps(doc_info, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    api_key_v2 = "<api key>"
    # IBM Cloud 画面 URLの https://jp-tok.discovery.watson.cloud.ibm.com/v2/instances/(省略)/projects/<your project id>/workspace から抜粋  # noqa: E501
    project_id = "<project id"
    # IBM Cloud 画面 URLの https://jp-tok.discovery.watson.cloud.ibm.com/v2/instances/(省略)/collections/<your collection id>/activity  # noqa: E501
    collection_id = "<collection id>"
    url = "https://<host>/instances/<instance id>"
    # ファイルを取得
    data_files = glob.glob("data/*.json")
    try:
        discovery = authentication_v2(api_key_v2, url)
        logger.info("authenticated.")

        results = query_results_v2(
            discovery=discovery,
            project_id=project_id,
            collection_ids=[collection_id],
            count=250
        )
        for i in range(len(data_files)):
            data_file = data_files[i]
            document_id = results[i]["document_id"]
            logger.info(f"input data. | document_id: {document_id}, file: {data_file}")  # noqa: E501
            jsonized_response = get_document_v2(
                discovery=discovery,
                project_id=project_id,
                collection_id=collection_id,
                document_id=document_id
            )
            logger.info(f"********** respose of [document_id: {document_id}] ********** :\n{jsonized_response}")  # noqa: E501
    except Exception:
        logger.exception("Unexpected exception.")
        sys.exit(1)
