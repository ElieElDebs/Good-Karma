from typing import Any, Dict, List

from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, PointStruct
from qdrant_client.models import VectorParams
from sentence_transformers import SentenceTransformer

# Initialize Qdrant client and embedding model
CLIENT = None  # = QdrantClient(host="localhost", port=6333)
MODEL = None  # = SentenceTransformer('all-MiniLM-L6-v2')


def initialize_qdrant(host: str = "localhost", port: int = 6333) -> None:
    """
    Initialize the Qdrant client.

    Args:
        host (str): The host address of the Qdrant server.
        port (int): The port number of the Qdrant server.

    Returns:
        None
    """
    global CLIENT

    if CLIENT is None:
        CLIENT = QdrantClient(host=host, port=port)


def create_collection(
    collection_name: str, vector_size: int = 384, distance: str = "Cosine"
) -> None:
    """
    Create a Qdrant collection if it does not exist.

    Args:
        collection_name (str): The name of the Qdrant collection.
        vector_size (int): The size of the embedding vectors.
        distance (str): The distance metric to use ("Cosine", "Euclidean", etc.).

    Returns:
        None
    """

    global CLIENT
    try:
        CLIENT.get_collection(collection_name)
    except Exception as e:
        if "Not found" in str(e):
            CLIENT.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_size, distance=distance),
            )
        else:
            raise e


def initialize_model(model_name: str = "all-mpnet-base-v2") -> None:
    """
    Initialize the sentence transformer model.

    Args:
        model_name (str): The name of the sentence transformer model to load.

    Returns:
        None
    """
    global MODEL

    if MODEL is None:
        MODEL = SentenceTransformer(model_name)


def vectorize_text(text: str) -> List[float]:
    """
    Vectorize a given text using a sentence transformer model.

    Args:
        text (str): The input text to vectorize.

    Returns:
        List[float]: The embedding vector of the input text.
    """
    return MODEL.encode(text).tolist()


def add_embeddings(
    collection_name: str,
    texts: List[str],
    ids: List[str],
    payloads: List[Dict[str, Any]],
) -> None:
    """
    Add embeddings to the Qdrant database.

    Args:
        collection_name (str): The name of the Qdrant collection.
        texts (List[str]): List of texts to vectorize and add.
        ids (List[str]): List of unique IDs for each text.
        payloads (List[Dict[str, Any]]): List of payloads associated with each text.

    Returns:
        None
    """
    vectors = [vectorize_text(text) for text in texts]
    points = []

    for id_value, vector, payload in zip(ids, vectors, payloads):
        # Check if the point ID already exists
        existing = CLIENT.retrieve(collection_name=collection_name, ids=[id_value])

        if existing:  # If the list is not empty, the ID exists
            print(f"ID {id_value} already exists in the collection. Skipping.")
            return None

        point = PointStruct(id=id_value, vector=vector, payload=payload)
        points.append(point)

    if points:
        CLIENT.upsert(collection_name=collection_name, points=points)


def delete_entries(collection_name: str, ids: List[int]) -> None:
    """
    Delete entries from the Qdrant database by their IDs.

    Args:
        collection_name (str): The name of the Qdrant collection.
        ids (List[int]): List of IDs to delete.

    Returns:
        None
    """
    CLIENT.delete(collection_name=collection_name, points_selector={"points": ids})


def search_embeddings(
    collection_name: str, query: str, top_k: int = 5, filter: Filter = None
) -> List[Dict[str, Any]]:
    """
    Search for similar embeddings in the Qdrant database.

    Args:
        collection_name (str): The name of the Qdrant collection.
        query (str): The query text to vectorize and search.
        top_k (int, optional): Number of top results to return. Defaults to 5.
        filter (Filter, optional): Optional Qdrant filter for search.

    Returns:
        List[Dict[str, Any]]: List of search results with payloads and scores.
    """
    query_vector = vectorize_text(query)
    results = CLIENT.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=top_k,
        query_filter=filter,
    )
    
    return [{"payload": r.payload, "score": r.score} for r in results]
