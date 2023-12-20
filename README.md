This is a repository for search API's ported or wrapped into a form usable in [ChainForge](https://chainforge.ai/).

See: [ChainForge Documentation > Add a Custom Provider](https://chainforge.ai/docs/custom_providers/)

See the larger objective is here:
https://danielsgriffin.com/2023/12/14/building-a-generative-web-search-arena/

# Cost

These all have a cost (or eat into monthly or one-time free quotas).

# TODO

- Add settings within the scripts to increase flexibility and reliability within ChainForge.
- Modify providers to have the final answer purely generated response rather than providing the query in the final response.
- Demonstrate on a subset of different benchmarks?
- Find third-party tutorials to replicate

# Search Providers

## Brave Search

`bravesearch_provider.py`

Uses LangChain's implementation: [Components > Document loaders > Brave Search](https://python.langchain.com/docs/integrations/document_loaders/brave_search)

## Metaphor Systems

`metaphor_provider.py`

This was initially based off the example code here: [Metaphor > Metaphor Search API > Recent News Summarizer](https://docs.metaphor.systems/reference/recent-news-summarizer)

## Perplexity AI

`perplexity_provider.py`

- model: `pplx-70b-online`

See: [Perplexity AI API > Chat Completions](https://docs.perplexity.ai/reference/post_chat_completions)

See also: [Perplexity AI Blog: "Introducing PPLX Online LLMs"](https://blog.perplexity.ai/blog/introducing-pplx-online-llms) (2023-11-29)

## SerpAPI

`serpapi_provider.py`

See: [SerpAPI > Google Search Engine Results API](https://serpapi.com/search-api)

## Tavily

`tavily_provider.py`

This is simply using a `qna_search`, not their search results fully.

There is plenty of room to explore possible improvements. Their website discusses a [GPT Researcher](https://docs.tavily.com/docs/gpt-researcher/introduction) ("GPT Researcher is an autonomous agent designed for comprehensive online research on a variety of tasks."), which seems something like a the offerings from academic search LLMs or the demo from Metaphor Systems, a local version of Perplexity AI's Copilot or Bing's Deep Search (or You.com's new ["Smart mode"](https://twitter.com/RichardSocher/status/1736883367919194485) (in beta)).

See: [Tavily API > Python SDK](https://docs.tavily.com/docs/tavily-api/python-sdk)

## You.com

`you_provider.py`

2023-12-19 23:09:56: I just realized that this has a different OpenAI model than the others: `gpt-3.5-turbo-16k` (which I think was the default in their example).

This is only using their search API and snippets, not their [News](https://documentation.you.com/api-reference/news) or [RAG](https://documentation.you.com/api-reference/rag) (elsewhere called [Web LLM](https://api.you.com/api-key)).

From their [api FAQ](https://api.you.com/faq):

> The YOU API has three dedicated endpoints, each best in class:
> 
> - Web LLM - Our end-to-end solution that pairs our Web Search results with an LLM to generate a response.
> - Web Search - This endpoint provides search results similar to Google or Bing, except that instead of short snippets designed for enticing humans to click the links, we deliver many long snippets designed to provide an LLM the most relevant information needed to generate the best response.
> - News — Similar to Web Search, but exclusively news results for applications that primarily rely on current events.

The code was initially based on this: [Using the Search API with an LLM > OpenAI LLM Integration](https://documentation.you.com/openai-language-model-integration)

- [You.com API Documentation](https://documentation.you.com/quickstart)
- [You.com API Dashboard](https://api.you.com/dashboard)

See also: [You.com: Introducing the YOU API: Web-scale search for LLMs](https://about.you.com/introducing-the-you-api-web-scale-search-for-llms/)

> **Future work**
>
> We will continue to work on enhancing the API’s functionality and user experience. Efforts are being made to make the APIs more intuitively conversational, allowing users to handle context effortlessly. Moreover, intermediate modules like query rewriting will be exposed as new endpoints, enabling developers to customize their usage of the YOU API according to their specific needs. Additionally, the API team aims to incorporate agent-like capabilities, similar to those of You.com’s Agent and Deep Research modes, making all the functionality of You.com accessible through the API.

# Misc

## API keys

The API keys are all stored in the local environment, not in the scripts.
Ex: `TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")`

## Requests v. SDKs v. LangChain

There are multiple ways to access several of these, this is what I used so far:

- Brave Search: LangChain
- Metaphor Systems: [`pip install metaphor_python`](https://github.com/metaphorsystems/metaphor-python)
- Perplexity AI: requests
- SerpAPI: [`pip install google-search-results`](https://serpapi.com/integrations/python)
- Tavily: [`pip install tavily-python`](https://docs.tavily.com/docs/tavily-api/python-sdk)
- You.com: LangChain

## query rewriting

I have a simple `generate_search_query` function in `bravesearch_provider.py`, `metaphor_provider.py`, and `serpapi_provider.py`.

## results

Search results are obtained with the Brave Search, Metaphor Systems, SerpAPI, and You.com providers. While Tavily can return search results, I only retrieve a short answer. Perplexity AI's model is "online", which seems to suggest it is not reliant on search results?

I'd like to write some providers that simply return a set of search results and snippets (or summaries).

There are many more providers of search results. Including [Kagi](https://kagi.com/settings?p=api) (which has question-answering ([FastGPT](https://help.kagi.com/kagi/api/fastgpt.html)) as well as summarizers and indices), Bing Web Search API, Google's Programmable Search Engine, 

## scraping and parsing

I use `readability` in the SerpAPI provider.

## generation

Brave Search, Metaphor Systems, SerpAPI, and You.com providers all rely on my orchestration (or a controllable LangChain setup) of OpenAI's API.

