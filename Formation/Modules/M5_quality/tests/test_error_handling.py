#!/usr/bin/env python3
"""Tests pour la gestion d'erreurs."""

import pytest
import logging
from src.error_handler import log_exceptions, safe_parse_json


def test_log_exceptions_decorator(caplog):
    """Test que le décorateur loggue les exceptions."""
    @log_exceptions
    def failing_function():
        raise ValueError("Test error")
    
    with pytest.raises(ValueError):
        failing_function()
    
    assert "failing_function" in caplog.text
    assert "Test error" in caplog.text


def test_safe_parse_json_valid():
    """Test parsing d'un JSON valide."""
    result = safe_parse_json('{"test": 42}')
    assert result == {"test": 42}


def test_safe_parse_json_invalid(caplog):
    """Test parsing d'un JSON invalide."""
    result = safe_parse_json('{"test": 42')  # Incomplet
    assert result == {}
    assert "JSON invalide" in caplog.text

