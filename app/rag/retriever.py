from app.rag.database import get_connection
from app.rag.embedder import model


def search_similar_chunks(
    question: str,
    top_k: int = 3,
    similarity_threshold: float = 0.30
):

    question_embedding = model.encode(question).tolist()

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    id,
                    content,
                    source,
                    1 - (embedding <=> %s::vector) AS similarity
                FROM knowledge_chunks
                WHERE 1 - (embedding <=> %s::vector) >= %s
                ORDER BY embedding <=> %s::vector
                LIMIT %s
                """,
                (
                    question_embedding,
                    question_embedding,
                    similarity_threshold,
                    question_embedding,
                    top_k
                )
            )

            return cursor.fetchall()

    finally:
        connection.close()