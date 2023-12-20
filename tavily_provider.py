import os

from chainforge.providers import provider
from tavily import TavilyClient

# Set up environment variables for API keys
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Initialize Tavily
tavily = TavilyClient(api_key=TAVILY_API_KEY)


def get_genwebsearch_response(prompt: str) -> str:
    return tavily.qna_search(query=prompt)


@provider(name="Tavily", emoji="✦", rate_limit="sequential", settings_schema={})
def TavilyProvider(prompt: str, **kwargs) -> str:
    """ChainForge custom provider that uses Tavily for generating responses."""
    return tavily.qna_search(query=prompt)


# Test the functioning (outside of ChainForge's provider)
if __name__ == "__main__":
    test_prompt = "Explain the latest news this week in generative web search."
    result = get_genwebsearch_response(test_prompt)
    print("Test Prompt:", test_prompt)
    print("Provider Response:", result)
