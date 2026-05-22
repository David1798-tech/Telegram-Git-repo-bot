from telegram import Update
from telegram.ext import ContextTypes
from auth import restricted


@restricted
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👾 *GitBot* — Your GitHub & Deploy Assistant\n\n"
        "Type /help to see all commands.",
        parse_mode="Markdown",
    )


@restricted
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📖 *GitBot Commands*\n\n"
        "*🗂 Repo Management*\n"
        "`/repos` — List your repos\n"
        "`/repo <name>` — Set active repo\n"
        "`/repoinfo` — Info about active repo\n\n"
        "*🌿 Branches*\n"
        "`/branches` — List branches\n"
        "`/branch <name>` — Switch or create a branch\n\n"
        "*📁 Files*\n"
        "`/files` — Root directory\n"
        "`/files <path>` — Browse a folder\n\n"
        "*🐛 Issues*\n"
        "`/issues` — Open issues\n"
        "`/newissue <title> | <body>` — Create issue\n\n"
        "*🔀 Pull Requests*\n"
        "`/prs` — Open PRs\n\n"
        "*🚀 Deploy*\n"
        "`/deploy vercel` — Trigger Vercel deploy\n"
        "`/deploy render` — Trigger Render deploy\n"
        "`/deploystatus vercel` — Latest Vercel deploy\n"
        "`/deploystatus render` — Latest Render deploy\n"
    )
    await update.message.reply_text(text, parse_mode="Markdown")
