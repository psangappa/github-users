"""
The user manager.
"""

from github_users.api.handlers.users import IncludeEnum
import asyncio
from github_users.api.async_http_client import SingletonAiohttp as aiohttp
from typing import Iterable


class UserManager:
    def __init__(self, url: str) -> None:
        self.api_base = url.rstrip("/")

    async def get_users(self, usernames: list, include: str) -> dict:
        """
        Gets the users and their repo data, transforms them to `Users` model.
        """
        if include == IncludeEnum.commit_latest:
            print("include is included!!!")

        user_repo_tasks = self._create_tasks(usernames)
        users_and_repos = await asyncio.gather(*user_repo_tasks)
        users = self._transform_result(users_and_repos)
        return {"users": users}

    def _create_tasks(self, usernames: list) -> list:
        """Creates tasks to get the users and repos asynchronously."""
        user_repo_tasks = []
        for username in usernames:
            user_repo_tasks.append(
                asyncio.create_task(
                    aiohttp.get(f"{self.api_base}/users/{username}")
                )
            )
            user_repo_tasks.append(
                asyncio.create_task(
                    aiohttp.get(
                        f"{self.api_base}/users/{username}/repos?sort=updated"
                    )
                )
            )
        return user_repo_tasks

    @staticmethod
    def _transform_result(users_and_repos: Iterable) -> list:
        """Transform the result to `Users` model."""
        users = []
        for user_info, repos in zip(*[iter(users_and_repos)] * 2):
            user = {
                "login_name": user_info["login"],
                "user_id": user_info["id"],
                "resource_uri": user_info["url"],
            }
            public_repositories = []
            for repo in repos:
                public_repositories.append(
                    {
                        "repository_name": repo["name"],
                        "repository_id": repo["id"],
                        "created_at": repo["created_at"],
                        "updated_at": repo["updated_at"],
                        "resource_uri": repo["url"],
                    }
                )
            user["public_repositories"] = public_repositories
            users.append(user)
        return users
