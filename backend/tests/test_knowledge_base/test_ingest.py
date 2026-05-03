from unittest.mock import patch, MagicMock
from app.knowledge_base.ingest import _chunk_text, ingest_all


def test_chunk_text_short():
    chunks = _chunk_text("hello world")
    assert chunks == ["hello world"]


def test_chunk_text_long():
    text = "a" * 1500
    chunks = _chunk_text(text, size=500, overlap=80)
    assert len(chunks) > 1
    assert all(len(c) <= 500 for c in chunks)


def test_ingest_all():
    with patch("app.knowledge_base.ingest.get_vector_store") as mock_vs:
        instance = MagicMock()
        instance.upsert.return_value = 60
        mock_vs.return_value = instance
        count = ingest_all()
        assert count == 60
        instance.upsert.assert_called_once()