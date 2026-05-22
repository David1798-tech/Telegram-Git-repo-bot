from telegram import Update
from telegram.ext import ContextTypes
from auth import restricted
from session import session
from services import github_api as gh


def _repo_required(user_id):
    """Returns repo name or None."""
    return session.get_repo(user_id)


# ── /repos ────────────────────────────────────────────────────────────────────

@restricted
async def cmd_repos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        repos = gh.get_repos()
        if not repos:
            await update.message.reply_text("No repos found.")
            return
        lines = [f"📦 *Your Repos* (last 15 updated)\n"]
        for r in repos:
            visibility = "🔒" if r["private"] else "🌐"
            lines.append(f"{visibility} `{r['name']}` — ⭐ {r['stargazers_count']}")
        lines.append("\nUse `/repo <name>` to set active repo.")
        await update.message.reply_text("\n".join(lines), parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")


# ── /repo <name> ──────────────────────────────────────────────────────────────

@restricted
async def cmd_repo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        current = _repo_required(update.effective_user.id)
        if current:
            branch = session.get_branch(update.effective_user.id)
            await update.message.reply_text(
                f"Active repo: `{current}` on branch `{branch}`", parse_mode="Markdown"
            )
        else:
            await update.message.reply_text("Usage: `/repo <name>`", parse_mode="Markdown")
        return

    repo_name = context.args[0]
    try:
        info = gh.get_repo_info(repo_name)
        session.set_repo(update.effective_user.id, repo_name)
        default_branch = info.get("default_branch", "main")
        session.set_branch(update.effective_user.id, default_branch)
        await update.message.reply_text(
            f"✅ Active repo set to `{repo_name}` (branch: `{default_branch}`)",
            parse_mode="Markdown",
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Repo not found or error: {e}")


# ── /repoinfo ─────────────────────────────────────────────────────────────────

@restricted
async def cmd_repoinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    repo = _repo_required(update.effective_user.id)
    if not repo:
        await update.message.reply_text("Set a repo first with `/repo <name>`", parse_mode="Markdown")
        return
    try:
        info = gh.get_repo_info(repo)
        commits = gh.get_latest_commits(repo, session.get_branch(update.effective_user.id), per_page=3)
        commit_lines = "\n".join(
            f"  • `{c['sha'][:7]}` {c['commit']['message'].splitlines()[0][:60]}"
            for c in commits
        )
        text = (
            f"📦 *{info['name']}*\n"
            f"{'🔒 Private' if info['private'] else '🌐 Public'} | "
            f"⭐ {info['stargazers_count']} | "
            f"🍴 {info['forks_count']}\n\n"
            f"📝 {info.get('description') or 'No description'}\n\n"
            f"🌿 Default branch: `{info['default_branch']}`\n"
            f"🔗 {info['html_url']}\n\n"
            f"*Recent commits:*\n{commit_lines}"
        )
        await update.message.reply_text(text, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")


# ── /branches ─────────────────────────────────────────────────────────────────

@restricted
async def cmd_branches(update: Update, context: ContextTypes.DEFAULT_TYPE):
    repo = _repo_required(update.effective_user.id)
    if not repo:
        await update.message.reply_text("Set a repo first with `/repo <name>`", parse_mode="Markdown")
        return
    try:
        branches = gh.get_branches(repo)
        active = session.get_branch(update.effective_user.id)
        lines = [f"🌿 *Branches in `{repo}`*\n"]
        for b in branches:
            marker = "👉 " if b["name"] == active else "   "
            lines.append(f"{marker}`{b['name']}`")
        lines.append("\nUse `/branch <name>` to switch or create a branch.")
        await update.message.reply_text("\n".join(lines), parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")


# ── /branch <name> ────────────────────────────────────────────────────────────

@restricted
async def cmd_branch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    repo = _repo_required(update.effective_user.id)
    if not repo:
        await update.message.reply_text("Set a repo first with `/repo <name>`", parse_mode="Markdown")
        return
    if not context.args:
        await update.message.reply_text("Usage: `/branch <name>`", parse_mode="Markdown")
        return

    branch_name = context.args[0]
    existing = [b["name"] for b in gh.get_branches(repo)]

    if branch_name in existing:
        session.set_branch(update.effective_user.id, branch_name)
        await update.message.reply_text(
            f"✅ Switched to branch `{branch_name}`", parse_mode="Markdown"
        )
    else:
        # Create new branch from current
        try:
            current_branch = session.get_branch(update.effective_user.id)
            gh.create_branch(repo, branch_name, from_branch=current_branch)
            session.set_branch(update.effective_user.id, branch_name)
            await update.message.reply_text(
                f"✅ Created and switched to new branch `{branch_name}` (from `{current_branch}`)",
                parse_mode="Markdown",
            )
        except Exception as e:
            await update.message.reply_text(f"❌ Error creating branch: {e}")


# ── /files [path] ─────────────────────────────────────────────────────────────

@restricted
async def cmd_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    repo = _repo_required(update.effective_user.id)
    if not repo:
        await update.message.reply_text("Set a repo first with `/repo <name>`", parse_mode="Markdown")
        return

    path = " ".join(context.args) if context.args else ""
    branch = session.get_branch(update.effective_user.id)

    try:
        contents = gh.get_files(repo, path, branch)
        if isinstance(contents, dict):
            # Single file returned
            await update.message.reply_text(
                f"📄 File: `{contents['path']}`\n"
                f"Size: {contents['size']} bytes\n"
                f"🔗 {contents['html_url']}",
                parse_mode="Markdown",
            )
            return

        lines = [f"📁 *`{repo}/{path or ''}` on `{branch}`*\n"]
        folders = [f for f in contents if f["type"] == "dir"]
        files = [f for f in contents if f["type"] == "file"]
        for f in sorted(folders, key=lambda x: x["name"]):
            lines.append(f"📂 `{f['name']}/`")
        for f in sorted(files, key=lambda x: x["name"]):
            lines.append(f"📄 `{f['name']}`")
        if not lines[1:]:
            lines.append("_(empty directory)_")
        await update.message.reply_text("\n".join(lines), parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")


# ── /issues ───────────────────────────────────────────────────────────────────

@restricted
async def cmd_issues(update: Update, context: ContextTypes.DEFAULT_TYPE):
    repo = _repo_required(update.effective_user.id)
    if not repo:
        await update.message.reply_text("Set a repo first with `/repo <name>`", parse_mode="Markdown")
        return
    try:
        issues = gh.get_issues(repo)
        if not issues:
            await update.message.reply_text(f"✅ No open issues in `{repo}`", parse_mode="Markdown")
            return
        lines = [f"🐛 *Open Issues in `{repo}`*\n"]
        for i in issues:
            lines.append(f"#{i['number']} — {i['title']}\n   🔗 {i['html_url']}")
        await update.message.reply_text("\n".join(lines), parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")


# ── /newissue <title> | <body> ────────────────────────────────────────────────

@restricted
async def cmd_newissue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    repo = _repo_required(update.effective_user.id)
    if not repo:
        await update.message.reply_text("Set a repo first with `/repo <name>`", parse_mode="Markdown")
        return
    if not context.args:
        await update.message.reply_text(
            "Usage: `/newissue <title> | <body>`\nBody is optional.",
            parse_mode="Markdown",
        )
        return

    full_text = " ".join(context.args)
    parts = full_text.split("|", 1)
    title = parts[0].strip()
    body = parts[1].strip() if len(parts) > 1 else ""

    try:
        issue = gh.create_issue(repo, title, body)
        await update.message.reply_text(
            f"✅ Issue created: *#{issue['number']}* — {issue['title']}\n🔗 {issue['html_url']}",
            parse_mode="Markdown",
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")


# ── /prs ──────────────────────────────────────────────────────────────────────

@restricted
async def cmd_prs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    repo = _repo_required(update.effective_user.id)
    if not repo:
        await update.message.reply_text("Set a repo first with `/repo <name>`", parse_mode="Markdown")
        return
    try:
        prs = gh.get_pull_requests(repo)
        if not prs:
            await update.message.reply_text(f"✅ No open PRs in `{repo}`", parse_mode="Markdown")
            return
        lines = [f"🔀 *Open PRs in `{repo}`*\n"]
        for pr in prs:
            lines.append(
                f"#{pr['number']} — {pr['title']}\n"
                f"   `{pr['head']['ref']}` → `{pr['base']['ref']}`\n"
                f"   🔗 {pr['html_url']}"
            )
        await update.message.reply_text("\n".join(lines), parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")
