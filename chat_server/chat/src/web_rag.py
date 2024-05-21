from llama_index.core import VectorStoreIndex
from llama_index.readers.web import BeautifulSoupWebReader

from src.website_scraper import read_urls_from_json

loader = BeautifulSoupWebReader()
url_list = read_urls_from_json("sandy_visited_urls.json")

documents = loader.load_data(urls=["https://google.com"])
index = VectorStoreIndex.from_documents(documents)
