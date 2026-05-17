# o langchain tem servicos para fazer web crawling e scraping, mas existem
# varias outras bibliotecas especializadas nisso, como a scrapy, beautifulsoup, 
# requests-html, firecrawl,etc.
# Entao, para casos mais complexos, vale a pena usar essas bibliotecas especializadas

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = WebBaseLoader("https://www.langchain.com/")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = splitter.split_documents(docs)

for chunk in chunks:
    print(chunk)
    print("-"*30)

