#!/usr/bin/env python3
"""Tests pour PromptEngineer."""

import pytest
import json
from src.prompt_engineering import PromptEngineer


@pytest.fixture
def functions():
    """Charge les définitions de fonctions."""
    with open('Dev/input/function_definitions.json', 'r') as f:
        return json.load(f)


@pytest.fixture
def engineer(functions):
    """Crée un PromptEngineer."""
    return PromptEngineer(functions)


def test_prompt_contains_role(engineer):
    """Test que le prompt contient le rôle."""
    prompt = engineer.build_prompt("Test")
    assert "assistant" in prompt.lower() or "convertit" in prompt.lower()


def test_prompt_contains_format(engineer):
    """Test que le prompt contient le format JSON."""
    prompt = engineer.build_prompt("Test")
    assert "json" in prompt.lower() or "fn_name" in prompt


def test_prompt_contains_examples(engineer):
    """Test que le prompt contient des exemples."""
    prompt = engineer.build_prompt("Test")
    assert "exemple" in prompt.lower() or "question" in prompt.lower()


def test_prompt_contains_question(engineer):
    """Test que le prompt contient la question."""
    question = "Quelle est la somme de 2 et 3 ?"
    prompt = engineer.build_prompt(question)
    assert question in prompt

