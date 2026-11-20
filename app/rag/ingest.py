
from pathlib import Path

from app.rag.loader import load_document
from app.rag.chunker import split_into_chunks
from app.rag.embedder import generate_embeddings
from app.rag.store import store_chunks


def ingest_document():

    # Locate the knowledge document
    document_path = (
        Path(__file__).parent / "knowledge" / "it_support_policy.txt"
    )

    # 1. Load document
    text = load_document(str(document_path))

    # 2. Split document into chunks
    chunks = split_into_chunks(text)

    if not chunks:
        print("No chunks generated.")
        return

    # 3. Generate embeddings
    embeddings = generate_embeddings(chunks)

    # 4. Store chunks and embeddings in PostgreSQL
    store_chunks(
        chunks=chunks,
        embeddings=embeddings,
        source=document_path.name
    )

    print(f"Document ingestion successful!")
    print(f"Document: {document_path.name}")
    print(f"Chunks stored: {len(chunks)}")


if __name__ == "__main__":
    ingest_document()
