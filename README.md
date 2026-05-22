# 👾 GitBot — Telegram GitHub & Deploy Assistant

Interact with your GitHub repos and trigger deployments to Vercel and Render — all from Telegram.

---

## Commands

| Command | Description |
|---|---|
| `/repos` | List your GitHub repos |
| `/repo <name>` | Set active repo |
| `/repoinfo` | Info + recent commits for active repo |
| `/branches` | List branches |
| `/branch <name>` | Switch to or create a branch |
| `/files [path]` | Browse repo files |
| `/issues` | List open issues |
| `/newissue <title> \| <body>` | Create a new issue |
| `/prs` | List open pull requests |
| `/deploy vercel` | Trigger Vercel deployment |
| `/deploy render` | Trigger Render deployment |
| `/deploystatus vercel` | Latest Vercel deploy status |
| `/deploystatus render` | Latest Render deploy status |

---

## Setup

### 1. Clone & install

```bash
git clone https://github.com/David1798-tech/gitbot.git
cd gitbot
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
```

Fill in your `.env` file:

- **TELEGRAM_TOKEN** — From [@BotFather](https://t.me/BotFather) → `/newbot`
- **ALLOWED_USER_IDS** — Your Telegram user ID (get from [@userinfobot](https://t.me/userinfobot))
- **GITHUB_TOKEN** — GitHub → Settings → Developer Settings → Personal Access Tokens (needs `repo` scope)
- **GITHUB_USERNAME** — Your GitHub username
- **VERCEL_TOKEN** — vercel.com → Account Settings → Tokens
- **VERCEL_PROJECT_ID** — vercel.com → Project → Settings → General
- **VERCEL_DEPLOY_HOOK** — vercel.com → Project → Settings → Git → Deploy Hooks
- **RENDER_API_KEY** — render.com → Account → API Keys
- **RENDER_SERVICE_ID** — render.com → Service → Settings (starts with `srv-`)
- **RENDER_DEPLOY_HOOK** — render.com → Service → Settings → Deploy Hook

### 3. Run locally

```bash
python bot.py
```

---

## Hosting

### Railway (recommended)
1. Push to GitHub
2. New project → Deploy from GitHub repo
3. Add all env vars in the Variables tab
4. Set start command: `python bot.py`

### Render
1. New → Background Worker
2. Connect GitHub repo
3. Start command: `python bot.py`
4. Add env vars

---

## Project Structure

```
gitbot/
├── bot.py              # Entry point
├── config.py           # Env vars
├── session.py          # Per-user state (active repo/branch)
├── auth.py             # User ID whitelist guard
├── handlers/
│   ├── general.py      # /start, /help
│   ├── github.py       # Repo, branch, file, issue, PR commands
│   └── deploy.py       # Vercel + Render deploy commands
├── services/
│   ├── github_api.py   # GitHub REST API wrapper
│   ├── vercel_api.py   # Vercel API + deploy hooks
│   └── render_api.py   # Render API + deploy hooks
├── requirements.txt
├── .env.example
└── Procfile
```
