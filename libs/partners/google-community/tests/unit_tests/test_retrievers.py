from unittest.mock import patch

from pydantic import SecretStr

from langchain_google_community.retrievers import GoogleSearchRetriever
from langchain_google_community.utilities import GoogleSearchAPIWrapper


def test_google_search_retriever() -> None:
    api_wrapper = GoogleSearchAPIWrapper(
        google_api_key=SecretStr("dummy"), search_engine_id="dummy"
    )
    results = [{"snippet": "test snippet", "title": "test title", "link": "test link"}]
    with patch(
        "langchain_google_community.utilities.GoogleSearchAPIWrapper.results",
        return_value=results,
    ):
        api_wrapper.k = 1
        retriever = GoogleSearchRetriever(api_wrapper=api_wrapper)
        docs = retriever.invoke("test query")
        assert len(docs) == 1
        assert docs[0].page_content == "test snippet"
        assert docs[0].metadata["title"] == "test title"
        assert docs[0].metadata["link"] == "test link"
