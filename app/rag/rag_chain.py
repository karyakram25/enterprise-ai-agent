from langchain_ollama import ChatOllama
from app.rag.retriever import search_similar_chunks


rag_llm = ChatOllama(
    model="qwen3:4b",
    temperature=0
)


def answer_question(question: str):

    results = search_similar_chunks(
        question,
        top_k=3
    )
    if not results:
        return "I don't have enough information in the knowledge base to answer that."

    context = "\n\n".join(
        result[1]
        for result in results
    )

    prompt = f"""
Context:
{context}

Question:
{question}

Answer the question using the Context.

If the Context contains the answer, give the answer directly.
If the Context does not contain the answer, say:
I don't have enough information in the knowledge base to answer that.

Answer:
"""

    response = rag_llm.invoke(prompt)

    return response.content 