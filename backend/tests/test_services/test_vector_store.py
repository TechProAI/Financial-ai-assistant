from unittest.mock import patch, MagicMock
import pytest
from app.core.exceptions import VectorStoreError


def _make_vs():
    """Build a VectorStore with Pinecone fully mocked."""
    with patch("app.services.vector_store.Pinecone") as mock_pc, \
         patch("app.services.vector_store.get_llm_service") as mock_llm:
        pc_instance = MagicMock()
        pc_instance.list_indexes.return_value = []
        mock_pc.return_value = pc_instance

        llm = MagicMock()
        llm.embed.return_value = [[0.1] * 1536]
        mock_llm.return_value = llm

        from app.services.vector_store import VectorStore
        vs = VectorStore()
        return vs, pc_instance, llm


def test_vector_store_creates_index_when_missing():
    vs, pc_instance, _ = _make_vs()
    pc_instance.create_index.assert_called_once()


def test_vector_store_upsert():
    vs, pc_instance, llm = _make_vs()
    llm.embed.return_value = [[0.1] * 1536, [0.2] * 1536]
    docs = [
        {"id": "1", "text": "a", "metadata": {"title": "A"}},
        {"id": "2", "text": "b", "metadata": {"title": "B"}},
    ]
    count = vs.upsert(docs)
    assert count == 2
    vs.index.upsert.assert_called()


def test_vector_store_upsert_raises():
    vs, _, llm = _make_vs()
    llm.embed.side_effect = RuntimeError("embed failed")
    with pytest.raises(VectorStoreError):
        vs.upsert([{"id": "1", "text": "a", "metadata": {}}])


def test_vector_store_query():
    vs, _, _ = _make_vs()
    match = MagicMock()
    match.score = 0.9
    match.metadata = {"text": "content", "title": "T", "source": "s"}
    results = MagicMock()
    results.matches = [match]
    vs.index.query.return_value = results

    chunks = vs.query("what is a stock?", top_k=3)
    assert len(chunks) == 1
    assert chunks[0].title == "T"
    assert chunks[0].score == 0.9


def test_vector_store_query_raises():
    vs, _, _ = _make_vs()
    vs.index.query.side_effect = RuntimeError("query failed")
    with pytest.raises(VectorStoreError):
        vs.query("q")