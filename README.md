# ContractShield Reddit Monitor

A bot that monitors freelance and small business subreddits for posts about contract disputes, payment issues, and client problems — then engages with helpful, non-promotional responses.

## Target Subreddits
- r/freelance
- r/smallbusiness
- r/entrepreneur
- r/SideHustle
- r/webdev

## Setup

```bash
pip install praw
```

Set environment variables:
```
REDDIT_CLIENT_ID=...
REDDIT_CLIENT_SECRET=...
REDDIT_BOT_USERNAME=...
REDDIT_BOT_PASSWORD=...
DRY_RUN=true  # set to false to actually post
```

Run:
```bash
python bot/monitor.py
```

## Purpose
Built for [ContractShield](https://contractshield.co) — free contract templates for freelancers.
