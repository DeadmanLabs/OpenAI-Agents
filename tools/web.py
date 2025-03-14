import os, re, fnmatch, json, shutil, glob, subprocess, requests
from typing import List, Dict, Any, Optional, Literal, Union, Tuple
from langchain_core.tools import BaseTool, tool
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from agents import Agent, FunctionTool, RunContextWrapper, function_tool

@function_tool
def web_search(query: str, num_results: int = 5) -> List[Dict[str, str]]:
    """
    Search the web for information on a specific query using SerpAPI.

    Args:
        query: The search query.
        num_results: Number of results to return (default: 5).

    Returns:
        A list of dictionaries containing search results with title, snippet, and url.
    """
    if not os.environ.get("SERPAPI_API_KEY"):
        return [{"error": "SERPAPI_API_KEY environment variable not set. Please set your SerpAPI key."}]

    # Construct the SerpAPI request
    params = {
            "engine": "google",
            "q": query,
            "api_key": os.environ.get("SERPAPI_API_KEY"),
            "num": num_results
    }

    # Make the API request
    response = requests.get("https://serpapi.com/search", params=params)
    response.raise_for_status()  # Raise an exception for bad status codes

    data = response.json()

    # Extract and format the search results
    results = []

    # Check if we have organic results
    if "organic_results" in data:
        for result in data["organic_results"][:num_results]:
            results.append({
                "title": result.get("title", "No title"),
                "snippet": result.get("snippet", "No snippet available"),
                "url": result.get("link", "No URL available")
            })

    # If we don't have enough results from organic search, check knowledge graph
    if len(results) < num_results and "knowledge_graph" in data:
        kg = data["knowledge_graph"]
        results.append({
            "title": kg.get("title", "Knowledge Graph Result"),
            "snippet": kg.get("description", "No description available"),
            "url": kg.get("website", "No website available")
        })

    # Add results from related questions if we still need more
    if len(results) < num_results and "related_questions" in data:
        for question in data["related_questions"][:num_results - len(results)]:
            results.append({
                "title": question.get("question", "Related Question"),
                "snippet": question.get("snippet", "No answer available"),
                "url": question.get("link", "No URL available")
            })

    return results

@function_tool
def fetch_webpage_content(url: str) -> str:
    """
    Fetch and extract the text content from a webpage.

    Args:
        url: The URL of the webpage to fetch.

    Returns:
        The extracted text content of the webpage.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for bad status codes

    soup = BeautifulSoup(response.text, 'html.parser')

    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.extract()

    # Get text
    text = soup.get_text(separator='\n')

    # Break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # Break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # Remove blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    # Check if content might be too large (assuming 8k token context window)
    if len(text) > os.environ.get("MAX_FILE_TOKENS"):  # Rough approximation
        raise Exception("Webpage content too large for context window")

    return text