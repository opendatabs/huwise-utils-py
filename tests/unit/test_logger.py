"""Unit tests for logger utilities."""

import logging

from huwise_utils_py.logger import get_logger


class TestLogger:
    """Tests for structured logger adapter behavior."""

    def test_get_logger_allows_structured_keyword_fields(self, caplog) -> None:
        """Test that keyword fields are serialized into the log message."""
        logger = get_logger("huwise_utils_py.test_logger")

        with caplog.at_level(logging.INFO):
            logger.info("Operation completed", dataset_uid="da_123", field_count=5)

        assert "Operation completed" in caplog.text
        assert "dataset_uid='da_123'" in caplog.text
        assert "field_count=5" in caplog.text
