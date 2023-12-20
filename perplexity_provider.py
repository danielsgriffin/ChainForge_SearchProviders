import os

import requests
from chainforge.providers import provider

# Set up environment variables for API keys
PPLX_API_KEY = os.getenv("PPLX_API_KEY")


def get_genwebsearch_response(prompt: str) -> str:
    """
    Sends a prompt to the Perplexity AI API and returns the model's response.
    """
    url = "https://api.perplexity.ai/chat/completions"

    # Define the payload with the prompt
    payload = {
        "model": "pplx-70b-online",
        "messages": [
            {"role": "system", "content": "Be precise and concise."},
            {"role": "user", "content": prompt},
        ],
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {PPLX_API_KEY}",
    }

    # Make the request
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Error in PPLX API call: {response.text}")


@provider(
    name="Perplexity AI (pplx-70b-online)", emoji="🔮", rate_limit="sequential", settings_schema={}
)
def PerplexityProvider(prompt: str, **kwargs) -> str:
    """
    ChainForge custom provider that uses Perplexity AI for generating responses.
    """
    return get_genwebsearch_response(prompt)


# Test the functioning (outside of ChainForge's provider)
if __name__ == "__main__":
    test_prompt = "Explain the latest news this week in generative web search."
    result = get_genwebsearch_response(test_prompt)
    print("Test Prompt:", test_prompt)
    print("Provider Response:", result)
