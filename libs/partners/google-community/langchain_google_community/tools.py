from typing import Any, Optional, Type

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from langchain_google_community.utilities import GoogleSearchAPIWrapper


class GoogleSearchSchema(BaseModel):
    """Input for GoogleSearchTool."""

    query: str = Field(description="search query to look up")


class GoogleSearchRun(BaseTool):
    """Tool that queries the Google Custom Search API."""

    name: str = "google_search"
    description: str = (
        "A wrapper around Google Search. "
        "Useful for when you need to answer questions about current events. "
        "Input should be a search query."
    )
    api_wrapper: GoogleSearchAPIWrapper = Field(default_factory=GoogleSearchAPIWrapper)
    args_schema: Type[BaseModel] = GoogleSearchSchema

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        return self.api_wrapper.run(query)


class GoogleSearchResults(BaseTool):
    """Tool that queries the Google Custom Search API and gets back json."""

    name: str = "google_search_results_json"
    description: str = (
        "A wrapper around Google Search. "
        "Useful for when you need to answer questions about current events. "
        "Input should be a search query. "
        "Output is a JSON array of the query results"
    )
    api_wrapper: GoogleSearchAPIWrapper = Field(default_factory=GoogleSearchAPIWrapper)
    args_schema: Type[BaseModel] = GoogleSearchSchema
    num_results: int = 10

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Any:
        """Use the tool."""
        results = self.api_wrapper.results(query, self.num_results)

        if self.response_format == "content_and_artifact":
            # If the user requested content_and_artifact, we can return the results
            # in the search_result format for models that support it.
            content = []
            for res in results:
                if "Result" in res:
                    content.append({"type": "text", "text": res["Result"]})
                    continue

                content.append(
                    {
                        "type": "search_result",
                        "title": res.get("title", ""),
                        "url": res.get("link", ""),
                        "content": [{"type": "text", "text": res.get("snippet", "")}],
                    }
                )
            return content, results

        return results
