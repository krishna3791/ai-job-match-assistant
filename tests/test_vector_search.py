from app.vector_search import build_embedding, cosine_similarity


def test_similar_text_has_higher_similarity_than_unrelated_text() -> None:
    query = build_embedding("Python SQL Spark Airflow RAG embeddings")
    similar = build_embedding("Python Spark pipelines with RAG and embeddings")
    unrelated = build_embedding("Retail sales associate customer service")

    assert cosine_similarity(query, similar) > cosine_similarity(query, unrelated)
