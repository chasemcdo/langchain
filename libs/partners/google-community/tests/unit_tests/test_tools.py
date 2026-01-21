from unittest.mock import patch

from pydantic import SecretStr

from langchain_google_community.tools import GoogleSearchResults, GoogleSearchRun
from langchain_google_community.utilities import GoogleSearchAPIWrapper


def test_google_search_run() -> None:
    api_wrapper = GoogleSearchAPIWrapper(
        google_api_key=SecretStr("dummy"), search_engine_id="dummy"
    )
    with patch(
        "langchain_google_community.utilities.GoogleSearchAPIWrapper.run",
        return_value="test results",
    ):
        tool = GoogleSearchRun(api_wrapper=api_wrapper)
        res = tool.run("test query")
        assert res == "test results"


def test_google_search_results() -> None:
    api_wrapper = GoogleSearchAPIWrapper(
        google_api_key=SecretStr("dummy"), search_engine_id="dummy"
    )
    with patch(
        "langchain_google_community.utilities.GoogleSearchAPIWrapper.results",
        return_value=[{"snippet": "test snippet"}],
    ):
        tool = GoogleSearchResults(api_wrapper=api_wrapper)
        res = tool.run("test query")
        assert res == [{"snippet": "test snippet"}]


def test_google_search_results_with_artifact() -> None:
    api_wrapper = GoogleSearchAPIWrapper(
        google_api_key=SecretStr("dummy"), search_engine_id="dummy"
    )
    results = [{"snippet": "test snippet", "title": "test title", "link": "test link"}]
    with patch(
        "langchain_google_community.utilities.GoogleSearchAPIWrapper.results",
        return_value=results,
    ):
        tool = GoogleSearchResults(
            api_wrapper=api_wrapper, response_format="content_and_artifact"
        )
        res = tool.run("test query", tool_call_id="123")
        assert res.artifact == results
        assert res.content == [
            {
                "type": "search_result",
                "title": "test title",
                "url": "test link",
                "content": [{"type": "text", "text": "test snippet"}],
            }
        ]
