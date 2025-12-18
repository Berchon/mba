from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from pathlib import Path

# caminho absoluto do arquivo atual
BASE_DIR = Path(__file__).resolve().parent

# caminho para o PDF (na mesma pasta do script)
pdf_path = BASE_DIR / "gpt5.pdf"

loader = PyPDFLoader(str(pdf_path))
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = splitter.split_documents(docs)

print(len(chunks))