from typing import List

from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from pydantic import Field

from langchain_google_community.utilities import GoogleSearchAPIWrapper


class GoogleSearchRetriever(BaseRetriever):
    """Google Search retriever."""

    api_wrapper: GoogleSearchAPIWrapper = Field(default_factory=GoogleSearchAPIWrapper)

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        results = self.api_wrapper.results(query, self.api_wrapper.k)
        if not results:
            return []

        return [
            Document(
                page_content=res.get("snippet", ""),
                metadata={
                    "title": res.get("title", ""),
                    "link": res.get("link", ""),
                },
            )
            for res in results
            if "Result" not in res
        ]
