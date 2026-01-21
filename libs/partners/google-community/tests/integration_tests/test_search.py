import pytest

from langchain_google_community.retrievers import GoogleSearchRetriever
from langchain_google_community.tools import GoogleSearchResults, GoogleSearchRun
from langchain_google_community.utilities import GoogleSearchAPIWrapper


@pytest.mark.integration
def test_google_search_api_wrapper_real() -> None:
    """This test requires GOOGLE_API_KEY and GOOGLE_CSE_ID."""
    search = GoogleSearchAPIWrapper()
    output = search.run("LangChain")
    assert isinstance(output, str)
    assert len(output) > 0


@pytest.mark.integration
def test_google_search_tool_real() -> None:
    """This test requires GOOGLE_API_KEY and GOOGLE_CSE_ID."""
    tool = GoogleSearchRun()
    output = tool.run("What is LangChain?")
    assert isinstance(output, str)
    assert len(output) > 0


@pytest.mark.integration
def test_google_search_results_tool_real() -> None:
    """This test requires GOOGLE_API_KEY and GOOGLE_CSE_ID."""
    tool = GoogleSearchResults(num_results=2)
    output = tool.run("LangChain news")
    assert isinstance(output, list)
    assert len(output) <= 2


@pytest.mark.integration
def test_google_search_retriever_real() -> None:
    """This test requires GOOGLE_API_KEY and GOOGLE_CSE_ID."""
    retriever = GoogleSearchRetriever()
    docs = retriever.invoke("LangChain documentation")
    assert isinstance(docs, list)
    assert len(docs) > 0
