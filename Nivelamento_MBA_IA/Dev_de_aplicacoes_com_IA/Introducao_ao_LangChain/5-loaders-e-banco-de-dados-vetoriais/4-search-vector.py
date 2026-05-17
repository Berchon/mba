import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

for k in ["GOOGLE_API_KEY", "PGVECTOR_URL", "PGVECTOR_COLLECTION"]:
    if k not in os.environ:
        raise RuntimeError(f"Missing required environment variable: {k}")

query = "Tell me more about the gpt-5 thinking evaluation and performance results comparing to gpt-4"

embeddings = GoogleGenerativeAIEmbeddings(
    model=os.getenv("EMBEDDING_MODEL", "text-embedding-004"),
)

store = PGVector(
    embeddings=embeddings,
    collection_name=os.environ["PGVECTOR_COLLECTION"],
    connection=os.environ["PGVECTOR_URL"],
    use_jsonb=True,
)

results = store.similarity_search_with_score(query, k=3)

for i, (doc, score) in enumerate(results, start=1):
    print("="*50)
    print(f"Resultado {i} (score: {score:.2f}):")
    print("="*50)

    print("\nTexto:\n")
    print(doc.page_content.strip())

    print("\nMetadados:\n")
    for k, v in doc.metadata.items():
        print(f"{k}: {v}")