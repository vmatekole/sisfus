# Web Scraper

## Problem statement
For web content to be available for NLP applications or for use in training LLMs it must be in a structured form so that it can be easily transformed and accessible for downstream applications.

## Solution
A suite of Python classes leveraging (scrapy)[https://scrapy.org/] to scrape content from the following sources:
- bbc.co.uk

Content is then persisted to Bigquery. Articles from various sources are scraped and imported into the articles table.

All ETL tasks are orchestrated using Prefect.

Show example schema
