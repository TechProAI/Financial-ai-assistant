"""Supabase JWT auth middleware for FastAPI."""
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client
from app.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

security = HTTPBearer(auto_error=False)


def get_supabase():
    """Create a Supabase client with service role (for server-side operations)."""
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """Extract and verify the user from the Supabase JWT token.
    
    Returns the user dict with 'id' and 'email'.
    If no token is provided, raises 401.
    """
    if not credentials:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = credentials.credentials
    try:
        supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
        user_response = supabase.auth.get_user(token)
        user = user_response.user

        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")

        return {"id": str(user.id), "email": user.email}

    except HTTPException:
        raise
    except Exception as e:
        logger.error("auth_failed", error=str(e))
        raise HTTPException(status_code=401, detail="Authentication failed")


async def get_optional_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict | None:
    """Same as get_current_user but returns None instead of raising 401."""
    if not credentials:
        return None
    try:
        return await get_current_user(credentials)
    except HTTPException:
        return None