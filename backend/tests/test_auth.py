import pytest
from app.core.security import create_access_token, create_refresh_token, decode_access_token, decode_refresh_token
from app.core.permissions import has_permission, Permission, RoleEnum

def test_token_creation():
    data = {"sub": "123", "role": "ADMIN"}
    
    access_token = create_access_token(data)
    assert access_token is not None
    
    refresh_token = create_refresh_token({"sub": "123"})
    assert refresh_token is not None
    
    # decode access token
    decoded = decode_access_token(access_token)
    assert decoded["sub"] == "123"
    assert decoded["role"] == "ADMIN"
    assert "exp" in decoded
    
    # decode refresh token
    decoded_refresh = decode_refresh_token(refresh_token)
    assert decoded_refresh["sub"] == "123"
    assert decoded_refresh["type"] == "refresh"
    assert "exp" in decoded_refresh

def test_decode_invalid_token():
    assert decode_access_token("invalid.token.string") is None
    assert decode_refresh_token("invalid.token.string") is None
    
def test_rbac_matrix():
    assert has_permission(RoleEnum.ADMIN, Permission.MANAGE_USERS) is True
    assert has_permission(RoleEnum.STAFF, Permission.MANAGE_USERS) is False
    
    assert has_permission(RoleEnum.FACULTY, Permission.SUBMIT_PROPOSAL) is True
    assert has_permission(RoleEnum.REVIEWER, Permission.SUBMIT_PROPOSAL) is False
    
    assert has_permission(RoleEnum.REVIEWER, Permission.REVIEW_PROPOSAL) is True
    
    # Invalid role test
    assert has_permission("UNKNOWN", Permission.VIEW_DASHBOARD) is False
