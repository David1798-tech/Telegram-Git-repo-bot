"""
Simple in-memory session manager.
Stores active repo and branch per Telegram user.
Resets on bot restart — fine for personal use.
"""


class SessionManager:
    def __init__(self):
        self._data = {}

    def get(self, user_id: int, key: str, default=None):
        return self._data.get(str(user_id), {}).get(key, default)

    def set(self, user_id: int, key: str, value):
        uid = str(user_id)
        if uid not in self._data:
            self._data[uid] = {}
        self._data[uid][key] = value

    def get_repo(self, user_id: int) -> str | None:
        return self.get(user_id, "repo")

    def set_repo(self, user_id: int, repo: str):
        self.set(user_id, "repo", repo)
        self.set(user_id, "branch", "main")  # reset branch when repo changes

    def get_branch(self, user_id: int) -> str:
        return self.get(user_id, "branch", "main")

    def set_branch(self, user_id: int, branch: str):
        self.set(user_id, "branch", branch)


# Single global instance imported by handlers
session = SessionManager()
