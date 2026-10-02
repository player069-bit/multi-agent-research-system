# Multi-Agent Research System

A multi-agent research system that searches the web, scrapes relevant sources, generates a research report, and reviews the report using multiple AI agents.

## Features

- Web search using Tavily
- Webpage scraping using BeautifulSoup
- Search Agent
- Reader Agent
- AI-generated research report
- Critic Agent for report review
- LangChain agents and LCEL pipelines
- OpenAI API integration

## Tech Stack

- Python
- LangChain
- LangGraph
- OpenAI
- Tavily
- BeautifulSoup
- Requests

## Project Structure

```text
Multi Agent System/
│
├── agents.py
├── pipeline.py
├── tools.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env
