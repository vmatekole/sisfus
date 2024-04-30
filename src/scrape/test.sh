#!/bin/bash
curl https://api-production.authory.com/content/ZariaGorvett?take\=300\&collection\=c5d1d6fb3283d4c4ba80a721ce88bcb26 | jq '.articles | length'
