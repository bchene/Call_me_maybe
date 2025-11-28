#!/usr/bin/env python3
"""Tests pour le pipeline."""

import pytest
from unittest.mock import Mock
from src.pipeline import FunctionCallingPipeline


class MockLLM:
    """Mock du LLM pour les tests."""
    
    def get_logits_from_input_ids(self, input_ids):
        """Retourne des logits déterministes."""
        vocab_size = 1000
        logits = np.zeros((len(input_ids), vocab_size))
        if len(input_ids) > 0:
            next_id = (input_ids[-1] + 1) % vocab_size
            logits[-1, next_id] = 10.0
        return logits
    
    def get_path_to_vocabulary_json(self):
        """Retourne le chemin du vocabulaire."""
        return "path/to/vocab.json"


def test_pipeline_initialization():
    """Test l'initialisation du pipeline."""
    mock_llm = MockLLM()
    pipeline = FunctionCallingPipeline(
        function_definitions_path='Dev/input/function_definitions.json',
        vocab_path='path/to/vocab.json',
        model=mock_llm
    )
    assert pipeline is not None


def test_pipeline_run():
    """Test l'exécution du pipeline."""
    # TODO: Implémenter avec mock complet
    pass

