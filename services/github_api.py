import requests
from config import GITHUB_TOKEN, GITHUB_USERNAME

BASE = "https://api.github.com"
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}


def _get(path, params=None):
    r = requests.get(f"{BASE}{path}", headers=HEADERS, params=params)
    r.raise_for_status()
    return r.json()


def _post(path, json_body):
    r = requests.post(f"{BASE}{path}", headers=HEADERS, json=json_body)
    r.raise_for_status()
    return r.json()


# ── Repos ────────────────────────────────────────────────────────────────────

def get_repos(per_page=15):
    return _get("/user/repos", params={"sort": "updated", "per_page": per_page})


def get_repo_info(repo):
    return _get(f"/repos/{GITHUB_USERNAME}/{repo}")


# ── Branches ─────────────────────────────────────────────────────────────────

def get_branches(repo):
    return _get(f"/repos/{GITHUB_USERNAME}/{repo}/branches")


def create_branch(repo, new_branch, from_branch="main"):
    ref_data = _get(f"/repos/{GITHUB_USERNAME}/{repo}/git/ref/heads/{from_branch}")
    sha = ref_data["object"]["sha"]
    return _post(
        f"/repos/{GITHUB_USERNAME}/{repo}/git/refs",
        {"ref": f"refs/heads/{new_branch}", "sha": sha},
    )


# ── Files ─────────────────────────────────────────────────────────────────────

def get_files(repo, path="", branch="main"):
    return _get(
        f"/repos/{GITHUB_USERNAME}/{repo}/contents/{path}",
        params={"ref": branch},
    )


# ── Issues ────────────────────────────────────────────────────────────────────

def get_issues(repo):
    return _get(
        f"/repos/{GITHUB_USERNAME}/{repo}/issues",
        params={"state": "open", "per_page": 10},
    )


def create_issue(repo, title, body=""):
    return _post(
        f"/repos/{GITHUB_USERNAME}/{repo}/issues",
        {"title": title, "body": body},
    )


# ── Pull Requests ─────────────────────────────────────────────────────────────

def get_pull_requests(repo):
    return _get(
        f"/repos/{GITHUB_USERNAME}/{repo}/pulls",
        params={"state": "open", "per_page": 10},
    )


# ── Commits ───────────────────────────────────────────────────────────────────

def get_latest_commits(repo, branch="main", per_page=5):
    return _get(
        f"/repos/{GITHUB_USERNAME}/{repo}/commits",
        params={"sha": branch, "per_page": per_page},
    )
