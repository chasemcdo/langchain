from typing import Any, Dict, List, Optional

import requests
from langchain_core.utils import get_from_dict_or_env
from pydantic import BaseModel, ConfigDict, Field, SecretStr, model_validator


class GoogleSearchAPIWrapper(BaseModel):
    """Wrapper for Google Custom Search API."""

    search_engine_id: Optional[str] = Field(default=None)
    google_api_key: Optional[SecretStr] = Field(default=None)
    k: int = 10
    siterestrict: bool = False

    model_config = ConfigDict(
        extra="forbid",
        arbitrary_types_allowed=True,
    )

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Any:
        """Validate that api key and python package exists in environment."""
        google_api_key = get_from_dict_or_env(
            values, "google_api_key", "GOOGLE_API_KEY"
        )
        values["google_api_key"] = (
            SecretStr(google_api_key)
            if isinstance(google_api_key, str)
            else google_api_key
        )

        search_engine_id = get_from_dict_or_env(
            values, "search_engine_id", "GOOGLE_CSE_ID"
        )
        values["search_engine_id"] = search_engine_id

        return values

    def _google_search_results(self, search_term: str, **kwargs: Any) -> List[Dict]:
        if self.siterestrict:
            url = "https://www.googleapis.com/customsearch/v1/siterestrict"
        else:
            url = "https://www.googleapis.com/customsearch/v1"

        params = {
            "q": search_term,
            "key": self.google_api_key.get_secret_value()
            if self.google_api_key
            else None,
            "cx": self.search_engine_id,
            "num": self.k,
            **kwargs,
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        search_results = response.json().get("items", [])
        return search_results

    def run(self, query: str, **kwargs: Any) -> str:
        """Run query through GoogleSearch and parse result."""
        results = self._google_search_results(query, **kwargs)
        if not results:
            return "No good Google Search Result was found"

        def f(res: Dict) -> str:
            return f"Snippet: {res.get('snippet', '')}\nLink: {res.get('link', '')}"

        return "\n\n".join([f(res) for res in results])

    def results(self, query: str, num_results: int, **kwargs: Any) -> List[Dict]:
        """Run query through GoogleSearch and return metadata."""
        results = self._google_search_results(query, num=num_results, **kwargs)
        if not results:
            return [{"Result": "No good Google Search Result was found"}]

        return [
            {
                "snippet": res.get("snippet", ""),
                "title": res.get("title", ""),
                "link": res.get("link", ""),
            }
            for res in results
        ]
