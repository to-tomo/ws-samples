"""
Watson Discovery V1 API を使用してドキュメント削除
"""

import json
import logging
import sys
from typing import Any, List
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import DiscoveryV1


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def authentication_v1(api_key: str, url: str) -> DiscoveryV1:
    """
    Watson Discovery の認証
    MEMO: https://cloud.ibm.com/apidocs/discovery?code=python#authentication-cloud  # noqa: E501
    """

    authenticator = IAMAuthenticator(api_key)
    discovery = DiscoveryV1(
        version="2019-04-30",
        authenticator=authenticator
        )
    discovery.set_service_url(url)
    return discovery


def query_results_v1(
    discovery: DiscoveryV1,
    environment_id: str,
    collection_id: str,
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
    MEMO: https://cloud.ibm.com/apidocs/discovery?code=python#query
    """
    response = discovery.query(
        environment_id=environment_id,
        collection_id=collection_id,
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


def delete_document_v1(
        discovery: DiscoveryV1,
        environment_id: str,
        collection_id: str,
        document_id: str) -> Any:

    delete_doc = discovery.delete_document(
        environment_id=environment_id,
        collection_id=collection_id,
        document_id=document_id,

    ).get_result()
    return json.dumps(delete_doc, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    api_key_v1 = "<api key>"
    # IBM Cloud 画面 URLの https://jp-tok.discovery.watson.cloud.ibm.com/v2/instances/(省略)/projects/<your project id>/workspace から抜粋  # noqa: E501
    environment_id = "<environment id>"
    # IBM Cloud 画面 URLの https://jp-tok.discovery.watson.cloud.ibm.com/v2/instances/(省略)/collections/<your collection id>/activity  # noqa: E501
    collection_id = "<collection id>"
    url = "https://<host>/instances/<instance id>"
    try:
        discovery = authentication_v1(api_key_v1, url)
        logger.info("authenticated.")
        results = query_results_v1(
            discovery=discovery,
            environment_id=environment_id,
            collection_id=collection_id,
            count=250
        )
        for i in range(len(results)):
            document_id = results[i]["id"]
            file_name = results[i]["file_name"]
            logger.info(f"input data. | document_id: {document_id}, file: {file_name}")  # noqa: E501
            jsonized_response = delete_document_v1(
                discovery=discovery,
                environment_id=environment_id,
                collection_id=collection_id,
                document_id=document_id,
            )
            logger.info(f"********** respose of [document_id: {document_id}] ********** :\n{jsonized_response}")  # noqa: E501
    except Exception:
        logger.exception("Unexpected exception.")
        sys.exit(1)
