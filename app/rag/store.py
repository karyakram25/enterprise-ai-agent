import json

from app.rag.database import get_connection


def store_chunks(chunks, embeddings, source):

    connection = get_connection()

    try:

        with connection.cursor() as cursor:

            for chunk, embedding in zip(chunks, embeddings):

                metadata = {
                    "document": source
                }

                cursor.execute(
                    """
                    INSERT INTO knowledge_chunks
                    (content, embedding, source, metadata)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        chunk,
                        embedding.tolist(),
                        source,
                        json.dumps(metadata)
                    )
                )

        connection.commit()

    finally:
        
        connection.close()