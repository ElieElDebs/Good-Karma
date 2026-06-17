from unittest.mock import Mock

import App.Database.qdrant as qdrant


def test_add_embeddings_skips_existing_points_before_vectorizing(monkeypatch):
    client = Mock()
    client.retrieve.side_effect = [[{"id": "existing-id"}], []]
    monkeypatch.setattr(qdrant, "CLIENT", client)

    vectorize_text = Mock(return_value=[0.1, 0.2, 0.3])
    monkeypatch.setattr(qdrant, "vectorize_text", vectorize_text)

    inserted_count = qdrant.add_embeddings(
        collection_name="posts",
        texts=["already embedded", "new post"],
        ids=["existing-id", "new-id"],
        payloads=[{"title": "old"}, {"title": "new"}],
    )

    assert inserted_count == 1
    vectorize_text.assert_called_once_with("new post")
    client.upsert.assert_called_once()

    points = client.upsert.call_args.kwargs["points"]
    assert len(points) == 1
    assert points[0].id == "new-id"
    assert points[0].payload == {"title": "new"}


def test_add_embeddings_does_not_upsert_when_all_points_exist(monkeypatch):
    client = Mock()
    client.retrieve.return_value = [{"id": "existing-id"}]
    monkeypatch.setattr(qdrant, "CLIENT", client)

    vectorize_text = Mock(return_value=[0.1, 0.2, 0.3])
    monkeypatch.setattr(qdrant, "vectorize_text", vectorize_text)

    inserted_count = qdrant.add_embeddings(
        collection_name="posts",
        texts=["already embedded"],
        ids=["existing-id"],
        payloads=[{"title": "old"}],
    )

    assert inserted_count == 0
    vectorize_text.assert_not_called()
    client.upsert.assert_not_called()
