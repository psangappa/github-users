import logging

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request
from fastapi import status

from github_users.models.users import Users
from fastapi import Query
from enum import Enum

logger = logging.getLogger(__name__)
user_router = APIRouter()


class IncludeEnum(str, Enum):
    """Choices"""

    commit_latest = "commit_latest"


@user_router.get("/users", response_model=list)
async def users(
    request: Request,
    usernames: str = Query(..., description="Comma separated usernames"),
    include: IncludeEnum = Query(
        None, description="Show users latest commit in the user's public "
                          "repository"
    ),
) -> list:
    """
    ```
    GET /api/v1/users?usernames=comma,separated,usernames&include=commit_latest

    - statuscode 200: in case of success
    - statuscode 422: in case of invalid input model
    - statuscode 500: in case of an internal error
    ```
    """

    try:
        usernames = [user.strip() for user in usernames.split(",")]
    except Exception as e:
        logger.error(e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    return usernames
