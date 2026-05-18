from unittest.mock import MagicMock
import pytest
from fastapi import HTTPException
from dependencies.services import get_current_admin_user

pytestmark = pytest.mark.unit


def test_get_current_admin_user_as_admin():
    mock_user = MagicMock()
    mock_role = MagicMock()
    mock_role.name = "admin"
    mock_user.roles = [mock_role]

    result = get_current_admin_user(current_user=mock_user)
    assert result == mock_user


def test_get_current_admin_user_as_regular_user():
    mock_user = MagicMock()
    mock_user.roles = []

    with pytest.raises(HTTPException) as exc_info:
        get_current_admin_user(current_user=mock_user)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Not enough privileges"
