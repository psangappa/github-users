import logging

from enum import Enum
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from fastapi import Query
from github_users.models.users import Users
from github_users.api.async_http_client import AuthorizationError


logger = logging.getLogger(__name__)
user_router = APIRouter()


class IncludeEnum(str, Enum):
    """Choices"""

    commit_latest = "commit_latest"


@user_router.get("/users", response_model=Users)
async def get_users(
    request: Request,
    usernames: str = Query(..., description="Comma separated usernames"),
    include: IncludeEnum = Query(
        None, description="Show users latest commit in the user's public "
                          "repository"
    ),
) -> Users:
    """
    ```
    GET /api/v1/users?usernames=comma,separated,usernames&include=commit_latest

    - statuscode 200: in case of success
    - statuscode 401: in case of access errors
    - statuscode 422: in case of invalid input model
    - statuscode 500: in case of an internal error
    ```
    """
    state = request.app.state
    try:
        usernames = [user.strip() for user in usernames.split(",")]
        users = await state.user_manager.get_users(usernames, include)
    except AuthorizationError:
        logger.error("Authentication error")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication error: you might want to set the "
            "GITHUB_TOKEN with a Personal access token",
        )
    except Exception as e:
        logger.error(e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    return users
