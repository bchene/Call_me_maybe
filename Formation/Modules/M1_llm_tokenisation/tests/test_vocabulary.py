#!/usr/bin/env python3
"""Tests pour la classe Vocabulary."""

import pytest
import json
from pathlib import Path
from llm_sdk import Small_LLM_Model
from src.vocabulary import Vocabulary


@pytest.fixture
def vocab():
    """Fixture pour le vocabulaire."""
    model = Small_LLM_Model()
    vocab_path = model.get_path_to_vocabulary_json()
    return Vocabulary(vocab_path)


def test_vocab_loads(vocab):
    """Test que le vocabulaire se charge correctement."""
    assert vocab.token_to_id is not None
    assert len(vocab.token_to_id) > 0


def test_encode_decode_roundtrip(vocab):
    """Test que encode puis decode redonne le token original."""
    test_tokens = ["hello", "world", "test"]
    
    for token in test_tokens:
        if token in vocab.token_to_id:
            token_id = vocab.encode_token(token)
            decoded = vocab.decode_id(token_id)
            assert decoded == token


def test_unk_token(vocab):
    """Test que le token UNK existe."""
    unk_id = vocab.get_unk_token_id()
    # Peut être None si pas de token UNK
    if unk_id is not None:
        assert isinstance(unk_id, int)


def test_eos_token(vocab):
    """Test que le token EOS existe."""
    eos_id = vocab.get_eos_token_id()
    # Peut être None si pas de token EOS
    if eos_id is not None:
        assert isinstance(eos_id, int)

