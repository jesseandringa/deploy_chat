import asyncio
import json

from crawl4ai import AsyncWebCrawler
from crawl4ai.chunking_strategy import RegexChunking
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from pydantic import BaseModel, Field


class PageSummary(BaseModel):
    title: str = Field(..., description="Title of the page.")
    summary: str = Field(..., description="Summary of the page.")
    brief_summary: str = Field(..., description="Brief summary of the page.")
    keywords: list = Field(..., description="Keywords assigned to the page.")


# Create a custom extraction strategy using Ollama
# class OllamaExtractionStrategy(LLMExtractionStrategy):
#     def __init__(self, model_name="ollama/llama3.2:1b"):
#         self.model_name = model_name

#     async def extract(self, text: str, instruction: str):
#         # Use the ollama.generate method to extract data
#         prompt = f"{instruction}\n\n{text}"
#         response = ollama.generate(model=self.model_name, prompt=prompt)

#         # Assuming the response contains generated text under 'text'
#         return response["text"]


# Define the extraction strategy using Ollama
# extraction_strategy = OllamaExtractionStrategy()
extraction_strategy = LLMExtractionStrategy(
    # provider="openai/gpt-4o",
    provider="ollama/llama3.1:latest",
    # api_token=os.getenv("OPENAI_API_KEY"),
    api_token="ollama",
    schema=PageSummary.model_json_schema(),
    extraction_type="schema",
    apply_chunking=False,
    instruction=(
        "From the crawled content, extract the following details: "
        "1. Title of the page "
        "2. Summary of the page, which is a detailed summary with all important data from the page. "
        "3. Brief summary of the page, which is a paragraph text "
        "4. Keywords assigned to the page, which is a list of keywords. "
        "The extracted JSON format should look like this: "
        '{ "title": "Page Title", "summary": "Detailed summary with all important data from the page.", '
        '"brief_summary": "Brief summary in a paragraph.", "keywords": ["keyword1", "keyword2", "keyword3"] }'
    ),
)


async def crawl_multiple_urls(urls):
    async with AsyncWebCrawler(verbose=True) as crawler:
        tasks = [
            crawler.arun(
                url=url,
                word_count_threshold=1,
                extraction_strategy=extraction_strategy,
                chunking_strategy=RegexChunking(),
                bypass_cache=True,
            )
            for url in urls
        ]
        results = await asyncio.gather(*tasks)
    return results


async def main():
    urls = [
        "https://sandy.utah.gov/306/City-Directory",
        "https://sandy.utah.gov/1414/Hiking-Club",
        "https://sandy.utah.gov/1403/Free-Fishing-Day",
    ]
    results = await crawl_multiple_urls(urls)

    for i, result in enumerate(results):
        if result.success:
            page_summary = json.loads(result.extracted_content)
            print(f"\nSummary for URL {i+1}:")
            print(json.dumps(page_summary, indent=2))
        else:
            print(f"\nFailed to summarize URL {i+1}. Error: {result.error_message}")


asyncio.run(main())
