"""Role-Based Access Control (RBAC) Matrix."""

from enum import Enum


class RoleEnum(str, Enum):
    ADMIN = "ADMIN"
    STAFF = "STAFF"
    LEADERSHIP = "LEADERSHIP"
    FACULTY = "FACULTY"
    REVIEWER = "REVIEWER"


class Permission(str, Enum):
    VIEW_DASHBOARD = "VIEW_DASHBOARD"
    MANAGE_USERS = "MANAGE_USERS"
    MANAGE_CATALOGS = "MANAGE_CATALOGS"
    MANAGE_PERIODS = "MANAGE_PERIODS"
    VIEW_PROPOSALS = "VIEW_PROPOSALS"
    SUBMIT_PROPOSAL = "SUBMIT_PROPOSAL"
    REVIEW_PROPOSAL = "REVIEW_PROPOSAL"
    APPROVE_PROPOSAL = "APPROVE_PROPOSAL"
    MANAGE_COUNCILS = "MANAGE_COUNCILS"
    SUBMIT_PROGRESS = "SUBMIT_PROGRESS"
    SUBMIT_ACCEPTANCE = "SUBMIT_ACCEPTANCE"


# RBAC Matrix: Maps Role to a set of allowed Permissions
RBAC_MATRIX = {
    RoleEnum.ADMIN: {
        Permission.VIEW_DASHBOARD,
        Permission.MANAGE_USERS,
        Permission.MANAGE_CATALOGS,
        Permission.MANAGE_PERIODS,
        Permission.VIEW_PROPOSALS,
    },
    RoleEnum.STAFF: {
        Permission.VIEW_DASHBOARD,
        Permission.MANAGE_CATALOGS,
        Permission.MANAGE_PERIODS,
        Permission.VIEW_PROPOSALS,
        Permission.APPROVE_PROPOSAL,
        Permission.MANAGE_COUNCILS,
    },
    RoleEnum.LEADERSHIP: {
        Permission.VIEW_DASHBOARD,
        Permission.VIEW_PROPOSALS,
        Permission.APPROVE_PROPOSAL,
    },
    RoleEnum.FACULTY: {
        Permission.VIEW_DASHBOARD,
        Permission.VIEW_PROPOSALS,
        Permission.SUBMIT_PROPOSAL,
        Permission.SUBMIT_PROGRESS,
        Permission.SUBMIT_ACCEPTANCE,
    },
    RoleEnum.REVIEWER: {
        Permission.VIEW_DASHBOARD,
        Permission.VIEW_PROPOSALS,
        Permission.REVIEW_PROPOSAL,
    },
}

def has_permission(role_code: str, permission: Permission) -> bool:
    """Check if a given role string has the specified permission."""
    try:
        role_enum = RoleEnum(role_code)
        return permission in RBAC_MATRIX.get(role_enum, set())
    except ValueError:
        return False
