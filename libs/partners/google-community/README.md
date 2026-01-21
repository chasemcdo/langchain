# langchain-google-community

This package contains the Google Community integrations for LangChain.

## Installation

```bash
pip install -U langchain-google-community
```

## Google Search

To use Google Search, you need to set up a Google Custom Search Engine and get an API key.

1. Create a Google Custom Search Engine at https://cse.google.com/cse/all
2. Get your Search Engine ID (CX)
3. Get a Google Cloud API Key at https://console.cloud.google.com/apis/credentials

Set the following environment variables:
- `GOOGLE_API_KEY`
- `GOOGLE_CSE_ID`

### Usage

```python
from langchain_google_community import GoogleSearchRun, GoogleSearchAPIWrapper

search = GoogleSearchRun(api_wrapper=GoogleSearchAPIWrapper())
search.run("What is LangChain?")
```
