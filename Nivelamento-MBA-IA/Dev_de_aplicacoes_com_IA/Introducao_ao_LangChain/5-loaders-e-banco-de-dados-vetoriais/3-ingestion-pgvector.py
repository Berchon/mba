import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector

load_dotenv()

for k in ["GOOGLE_API_KEY", "PGVECTOR_URL", "PGVECTOR_COLLECTION"]:
    if k not in os.environ:
        raise RuntimeError(f"Missing required environment variable: {k}")

BASE_DIR = Path(__file__).resolve().parent

pdf_path = BASE_DIR / "gpt5.pdf"

loader = PyPDFLoader(str(pdf_path))
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=150,
    add_start_index=False,
)
splits = splitter.split_documents(docs)

if not splits:
    raise SystemExit(0)

enriched = [
    Document(
        page_content=doc.page_content,
        metadata={k: v for k, v in doc.metadata.items() if v not in ("", None)},
    )
    for doc in splits
]

ids = [f"doc-{i}" for i in range(len(enriched))]

embeddings = GoogleGenerativeAIEmbeddings(
    model=os.getenv("EMBEDDING_MODEL", "text-embedding-004"),
)

store = PGVector(
    embeddings=embeddings,
    collection_name=os.environ["PGVECTOR_COLLECTION"],
    connection=os.environ["PGVECTOR_URL"],
    use_jsonb=True,
)

store.add_documents(documents=enriched, ids=ids)