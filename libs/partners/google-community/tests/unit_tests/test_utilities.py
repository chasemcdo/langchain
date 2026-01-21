from unittest.mock import MagicMock, patch

from pydantic import SecretStr

from langchain_google_community.utilities import GoogleSearchAPIWrapper


@patch("requests.get")
def test_google_search_api_wrapper_run(mock_get: MagicMock) -> None:
    mock_get.return_value.json.return_value = {
        "items": [
            {"snippet": "snippet 1", "link": "link 1"},
            {"snippet": "snippet 2", "link": "link 2"},
        ]
    }
    wrapper = GoogleSearchAPIWrapper(
        google_api_key=SecretStr("test_key"), search_engine_id="test_id"
    )
    res = wrapper.run("test query")
    assert "snippet 1" in res
    assert "link 1" in res
    assert "snippet 2" in res
    assert "link 2" in res


@patch("requests.get")
def test_google_search_api_wrapper_results(mock_get: MagicMock) -> None:
    mock_get.return_value.json.return_value = {
        "items": [
            {"snippet": "snippet 1", "title": "title 1", "link": "link 1"},
        ]
    }
    wrapper = GoogleSearchAPIWrapper(
        google_api_key=SecretStr("test_key"), search_engine_id="test_id"
    )
    res = wrapper.results("test query", 1)
    assert len(res) == 1
    assert res[0]["snippet"] == "snippet 1"
    assert res[0]["title"] == "title 1"
    assert res[0]["link"] == "link 1"
