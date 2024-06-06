# Sisfus
(Under Development)

Sisfus is a command-line tool for web scraping and embedding generation, designed to make web content available for NLP and LLM applications.

A suite of Python classes leveraging (scrapy)[https://scrapy.org/] to scrape content from the following sources:
- bbc.co.uk

Embedding models supported:
- text-embedding-3-small (OpenAI)
- text-embedding-3-large (OpenAI)

Content is parsed and validated into a set of Pydantic models and then persisted to Bigquery.
