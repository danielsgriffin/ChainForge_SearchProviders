"""This chain is adapted from metaphor's example code, see also metaphor_provider.py."""
import requests
import os
import textwrap
from datetime import datetime, timedelta

from readability import Document
import openai
from chainforge.providers import provider
from langchain.document_loaders import BraveSearchLoader


# Set up environment variables for API keys
BRAVE_SEARCH_API_KEY = os.getenv("BRAVE_SEARCH_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize APIs
openai.api_key = OPENAI_API_KEY


def get_openai_response(system_message, content):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": content},
        ],
    )
    return completion.choices[0].message.content


def generate_search_query(question: str) -> str:
    """Generates a search query based on the user's question."""
    system_message = "You are a helpful assistant that generates search queries based on user questions. Only generate one search query."
    return get_openai_response(system_message, question)


def fetch_search_results(search_query: str, result_limit: int) -> list:
    """Fetches search results from BraveSearch via LangChain."""
    loader = BraveSearchLoader(
        query=search_query, api_key=BRAVE_SEARCH_API_KEY, search_kwargs={"count": result_limit}
    )
    docs = loader.load()
    return docs

def summarize_content(content: str, url: str, title: str, query: str) -> str:
    """Summarizes the content of a webpage."""
    system_message = "You are a helpful assistant that briefly summarizes the content of a webpage. Summarize the content with respect to the user query."
    content = f"# Query\n{query}\n\n# Content\n{content}"
    summary = get_openai_response(system_message, content)
    summary_formatted = textwrap.fill(summary, 80)
    return f"Summary for {url}:\n{title}\n{summary_formatted}"


def generate_response(question: str, query: str, summaries: list):
    """Generates a response for the user based on the question, previously generated query, and summaries."""
    system_message = "You are a helpful assistant that generates a response based on the user question, an computer-generated query, and summaries of top search results. Generate a response."
    content = f"Question: {question}\nQuery: {query}\nSummaries: {summaries}"
    return get_openai_response(system_message, content)


def get_genwebsearch_response(question: str) -> str:
    search_query = generate_search_query(question)
    print(f"Generated search query: {search_query}")

    limit = 5
    
    results = fetch_search_results(search_query, result_limit=limit)
    print(f"Length of results: {len(results)}")

    # Process the summaries of the top results
    summaries = []

    for n, result in enumerate(results[:limit]):
        print(f"Processing result {n}...")
        result_content_extract = result.page_content[:1000]          
        summary = summarize_content(
            result_content_extract, result.metadata["link"], result.metadata["title"], search_query
        )
        summaries.append(summary)

    # Generate a response for the user
    print(f"Length of summaries: {len(summaries)}")
    print(f"Summaries: {summaries}")
    print("Generating response...")
    response = generate_response(question, search_query, summaries)
    return f"searched: {search_query}\n\nsummary of results: {response}"


@provider(
    name="BraveSearch (gpt-3.5-turbo)",
    emoji="🛡",
    rate_limit="sequential",
    settings_schema={},
)
def BraveSearchProvider(prompt: str, **kwargs) -> str:
    """ChainForge custom provider that uses BraveSearch for search results & Open AI for generating responses."""
    return get_genwebsearch_response(prompt)

# Test the functioning (outside of ChainForge's provider)
if __name__ == "__main__":
    test_prompt = "Explain the latest news this week in generative web search."
    result = get_genwebsearch_response(test_prompt)
    print("Test Prompt:", test_prompt)
    print("Provider Response:", result)