#!/usr/bin/env python3
"""Tests pour la validation."""

import pytest
from pydantic import ValidationError
from src.validation import FunctionCallResult, FunctionCallValidator, FunctionDefinition


def test_function_call_result_valid():
    """Test création d'un FunctionCallResult valide."""
    result = FunctionCallResult(
        prompt="Test",
        fn_name="fn_add_numbers",
        args={"a": 2.0, "b": 3.0}
    )
    assert result.fn_name == "fn_add_numbers"
    assert result.args["a"] == 2.0


def test_function_call_result_missing_field():
    """Test que les champs requis sont obligatoires."""
    with pytest.raises(ValidationError):
        FunctionCallResult(
            fn_name="test",
            args={}
            # prompt manquant
        )


def test_validator_valid_call():
    """Test validation d'un appel valide."""
    functions = {
        "fn_add_numbers": FunctionDefinition(
            name="fn_add_numbers",
            args={"a": "float", "b": "float"},
            return_type="float"
        )
    }
    
    validator = FunctionCallValidator(functions)
    result = FunctionCallResult(
        prompt="Test",
        fn_name="fn_add_numbers",
        args={"a": 2.0, "b": 3.0}
    )
    
    is_valid, error = validator.validate(result)
    assert is_valid
    assert error is None


def test_validator_missing_arg():
    """Test validation avec argument manquant."""
    functions = {
        "fn_add_numbers": FunctionDefinition(
            name="fn_add_numbers",
            args={"a": "float", "b": "float"},
            return_type="float"
        )
    }
    
    validator = FunctionCallValidator(functions)
    result = FunctionCallResult(
        prompt="Test",
        fn_name="fn_add_numbers",
        args={"a": 2.0}  # b manquant
    )
    
    is_valid, error = validator.validate(result)
    assert not is_valid
    assert "b" in error.lower()

