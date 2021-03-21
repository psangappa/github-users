"""
The response model of the users
"""


from pydantic import BaseModel
from pydantic import Field
from datetime import datetime
from typing import List


class LatestCommit(BaseModel):
    """
    Included in the user's public repository only when an additional
    `include=commit_latest` query parameter is provided.
    """

    commit_hash: str = Field(description="The commit hash.")
    author: str = Field(description="Author name of this commit.")
    committer_email: str = Field(description="The email of the committer.")
    commit_date: datetime = Field(description="The commit date.")
    resource_uri: str = Field(description="The API url of this commit.")


class PublicRepository(BaseModel):
    """
    Public repositories of the user.
    """

    def dict(self, **kwargs):
        """
        fields which are equal to None should be excluded.
        In our case `latest_commit`.
        """
        kwargs["exclude_none"] = True
        return super().dict(**kwargs)

    repository_name: str = Field(description="The name of the repository.")
    repository_id: str = Field(description="The ID of the repository.")
    created_at: datetime = Field(
        description="Repository created time. ISO 8601 format"
    )
    updated_at: datetime = Field(
        description="Repository updated time. ISO 8601 format"
    )
    resource_uri: str = Field(description="The API url of the repository.")
    latest_commit: LatestCommit = Field(
        default=None,
        description="Latest commit information to this repository.",
    )


class User(BaseModel):
    """
    Information about a single user.
    """

    login_name: str = Field(description="The username.")
    user_id: str = Field(description="The user ID.")
    resource_uri: str = Field(description="The API url of the user.")
    public_repositories: List[PublicRepository] = Field(
        description="List of public repositories."
    )


class Users(BaseModel):
    """
    List of users that was requested for.
    """

    size: int = Field(description="Total number of users.")
    missing: int = Field(description="Total number of missing users.")
    users: List[User] = Field(
        description="List of users requested for.", default=[]
    )
