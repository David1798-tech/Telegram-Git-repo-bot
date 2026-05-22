import logging
from telegram.ext import Application, CommandHandler
from config import TELEGRAM_TOKEN
from handlers.general import start, help_command
from handlers.github import (
    cmd_repos, cmd_repo, cmd_files, cmd_branches,
    cmd_branch, cmd_issues, cmd_newissue, cmd_prs, cmd_repoinfo
)
from handlers.deploy import cmd_deploy, cmd_deploystatus

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # General
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # GitHub
    app.add_handler(CommandHandler("repos", cmd_repos))
    app.add_handler(CommandHandler("repo", cmd_repo))
    app.add_handler(CommandHandler("repoinfo", cmd_repoinfo))
    app.add_handler(CommandHandler("files", cmd_files))
    app.add_handler(CommandHandler("branches", cmd_branches))
    app.add_handler(CommandHandler("branch", cmd_branch))
    app.add_handler(CommandHandler("issues", cmd_issues))
    app.add_handler(CommandHandler("newissue", cmd_newissue))
    app.add_handler(CommandHandler("prs", cmd_prs))

    # Deploy
    app.add_handler(CommandHandler("deploy", cmd_deploy))
    app.add_handler(CommandHandler("deploystatus", cmd_deploystatus))

    logger.info("GitBot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
