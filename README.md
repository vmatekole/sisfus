# Web Scraper

## Problem statement
For web content to be available for NLP applications or for use in training LLMs it must be in a structured form so that it can be easily transformed and accessible for downstream applications.

## Solution
A suite of Python classes leveraging (scrapy)[https://scrapy.org/] to scrape content from the following sources:
- bbc.co.uk

Content is parsed and validated into a set of Pydantic models and then persisted to Bigquery.

All ETL tasks are orchestrated using Prefect.

Show example schema
