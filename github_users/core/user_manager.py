"""
The user manager. Contains core logic.
"""

import asyncio
from github_users.api.handlers.users import IncludeEnum
from github_users.api.async_http_client import SingletonAiohttp as aiohttp
from typing import Dict
from typing import List
from typing import Iterable
from typing import Tuple
from itertools import cycle


class UserManager:
    def __init__(self, url: str) -> None:
        self.api_base = url.rstrip("/")

    async def get_users(self, usernames: List, include: str) -> Dict:
        """
        Gets the users and their repo data, transforms them to `Users` model.
        """
        user_repo_tasks = self._create_tasks(usernames)
        users_and_repos = await asyncio.gather(*user_repo_tasks)
        users, missing = self._transform_result(users_and_repos)
        if include == IncludeEnum.commit_latest:
            await self._add_latest_commit(users)
        return {"size": len(users), "missing": missing, "users": users}

    def _create_tasks(self, usernames: List) -> List:
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
    def _transform_result(users_and_repos: Iterable) -> Tuple[List, int]:
        """Transform the result to `Users` model."""
        users = []
        missing = 0
        for user_info, repos in zip(*[iter(users_and_repos)] * 2):
            if not user_info:
                missing += 1
                continue
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
        return users, missing

    async def _add_latest_commit(self, users: List) -> None:
        """
        Add the latest commit info to the user's repo when
        `include=commit_latest`.
        """
        commit_tasks = []
        for user in users:
            owner = user["login_name"]
            for repository in user["public_repositories"]:
                repo = repository["repository_name"]
                commit_tasks.append(
                    asyncio.create_task(
                        aiohttp.get(
                            f"{self.api_base}/repos/{owner}/{repo}/commits?per_page=1"
                        )
                    )
                )
        repo_commits = await asyncio.gather(*commit_tasks)
        repo_commits = cycle(repo_commits)
        for user in users:
            for repo in user["public_repositories"]:
                commit: List[Dict] = next(repo_commits)
                if commit:
                    commit: Dict = commit[0]
                    repo["latest_commit"] = {
                        "commit_hash": commit["sha"],
                        "author": commit["commit"]["author"]["name"],
                        "committer_email": commit["commit"]["committer"][
                            "email"
                        ],
                        "commit_date": commit["commit"]["committer"]["date"],
                        "resource_uri": commit["url"],
                    }
