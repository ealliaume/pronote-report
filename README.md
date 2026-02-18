# Pronote Weekly Report

Fetches grades from Pronote for all children of a parent account and sends a formatted email every Monday morning.

## Setup

### 1. Install dependencies (local testing)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env with your actual values
```

| Variable | Description |
|---|---|
| `PRONOTE_URL` | URL of your school's Pronote parent page (ends with `parent.html`) |
| `PRONOTE_USERNAME` | Your Pronote username |
| `PRONOTE_PASSWORD` | Your Pronote password |
| `RESEND_API_KEY` | API key from [resend.com](https://resend.com) (free) |
| `EMAIL_FROM` | Verified sender address on Resend |
| `EMAIL_TO` | Your email address |

### 3. Test locally

```bash
python main.py
```

### 4. Deploy to GitHub Actions

1. Push this repo to GitHub (can be private).
2. Go to **Settings → Secrets and variables → Actions**.
3. Add each variable from `.env.example` as a **Repository secret**.
4. The workflow runs every **Monday at 7:00 AM** (Paris time).
   You can also trigger it manually from the **Actions** tab → **Weekly Pronote Report** → **Run workflow**.

## Finding your Pronote URL

Log into Pronote as a parent in your browser. Copy the URL from the address bar — it looks like:

```
https://YOUR_SCHOOL.index-education.net/pronote/parent.html
```

## Email provider

The script uses [Resend](https://resend.com). The free plan allows 3 000 emails/month.
You need to verify a sending domain. If you don't have a custom domain, Resend offers an `@resend.dev` address for testing.
