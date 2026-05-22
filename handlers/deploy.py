from telegram import Update
from telegram.ext import ContextTypes
from auth import restricted
from services import vercel_api, render_api


# ── /deploy <platform> ────────────────────────────────────────────────────────

@restricted
async def cmd_deploy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Usage: `/deploy vercel` or `/deploy render`", parse_mode="Markdown"
        )
        return

    platform = context.args[0].lower()

    if platform == "vercel":
        try:
            await update.message.reply_text("🚀 Triggering Vercel deploy...")
            result = vercel_api.trigger_deploy()
            job_id = result.get("job", {}).get("id", "N/A")
            await update.message.reply_text(
                f"✅ Vercel deploy triggered!\nJob ID: `{job_id}`\n\n"
                f"Use `/deploystatus vercel` to check status.",
                parse_mode="Markdown",
            )
        except Exception as e:
            await update.message.reply_text(f"❌ Vercel deploy failed: {e}")

    elif platform == "render":
        try:
            await update.message.reply_text("🚀 Triggering Render deploy...")
            render_api.trigger_deploy()
            await update.message.reply_text(
                "✅ Render deploy triggered!\n\n"
                "Use `/deploystatus render` to check status.",
                parse_mode="Markdown",
            )
        except Exception as e:
            await update.message.reply_text(f"❌ Render deploy failed: {e}")

    else:
        await update.message.reply_text("❌ Unknown platform. Use `vercel` or `render`.", parse_mode="Markdown")


# ── /deploystatus <platform> ─────────────────────────────────────────────────

@restricted
async def cmd_deploystatus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Usage: `/deploystatus vercel` or `/deploystatus render`",
            parse_mode="Markdown",
        )
        return

    platform = context.args[0].lower()

    if platform == "vercel":
        try:
            deploy = vercel_api.get_latest_deployment()
            if not deploy:
                await update.message.reply_text("No Vercel deployments found.")
                return
            state = deploy.get("state", "unknown").upper()
            name = deploy.get("name", "N/A")
            url = deploy.get("url", "")
            created = deploy.get("created", "")
            emoji = {"READY": "✅", "ERROR": "❌", "BUILDING": "🔄", "QUEUED": "⏳"}.get(state, "❓")
            await update.message.reply_text(
                f"{emoji} *Vercel — Latest Deploy*\n\n"
                f"Project: `{name}`\n"
                f"Status: `{state}`\n"
                f"URL: https://{url}\n"
                f"Created: {created}",
                parse_mode="Markdown",
            )
        except Exception as e:
            await update.message.reply_text(f"❌ Error fetching Vercel status: {e}")

    elif platform == "render":
        try:
            deploy = render_api.get_latest_deployment()
            if not deploy:
                await update.message.reply_text("No Render deployments found.")
                return
            status = deploy.get("status", "unknown").upper()
            deploy_id = deploy.get("id", "N/A")
            created_at = deploy.get("createdAt", "")
            emoji = {
                "LIVE": "✅", "DEACTIVATED": "⚪", "BUILD_FAILED": "❌",
                "UPDATE_FAILED": "❌", "INPROGRESS": "🔄"
            }.get(status, "❓")
            await update.message.reply_text(
                f"{emoji} *Render — Latest Deploy*\n\n"
                f"Deploy ID: `{deploy_id}`\n"
                f"Status: `{status}`\n"
                f"Created: {created_at}",
                parse_mode="Markdown",
            )
        except Exception as e:
            await update.message.reply_text(f"❌ Error fetching Render status: {e}")

    else:
        await update.message.reply_text(
            "❌ Unknown platform. Use `vercel` or `render`.", parse_mode="Markdown"
        )
