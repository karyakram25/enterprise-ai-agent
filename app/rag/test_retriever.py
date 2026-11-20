from app.rag.retriever import search_similar_chunks


question = "question = How long does a password reset normally take?"

results = search_similar_chunks(question, top_k=3)

print("QUESTION:")
print(question)

print("\nRETRIEVED CHUNKS:")

for result in results:

    chunk_id, content, source, similarity = result

    print(f"\n--- Chunk ID: {chunk_id} ---")
    print(f"Source: {source}")
    print(f"Similarity: {similarity:.4f}")
    print(f"Content:\n{content}")