"""
ContractShield Reddit Monitor Bot
Monitors targeted subreddits for posts related to contract disputes,
payment issues, and client management problems. Engages with helpful,
non-promotional responses pointing to free resources.
"""

import praw
import time
import logging
import os
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# Target subreddits
TARGET_SUBREDDITS = [
    "freelance",
    "smallbusiness",
    "entrepreneur",
    "SideHustle",
    "webdev",
]

# Keywords that signal a relevant post
TRIGGER_KEYWORDS = [
    "client won't pay", "client refused", "ghosted", "not paying",
    "dispute", "contract", "scope creep", "invoice", "chargeback",
    "non-payment", "payment terms", "late payment", "client owes",
    "no contract", "verbal agreement", "client disappeared",
]

# Reply template (kept helpful, non-promotional)
REPLY_TEMPLATE = """
Hey, sorry you're dealing with this — it's one of the most stressful situations in freelancing.

A few things that might help:
- **Document everything**: Screenshot all communications, agreements, and deliverables immediately.
- **Send a formal demand letter**: Even a simple email referencing your original agreement can prompt payment.
- **Check your contract**: If you have one, look for dispute resolution clauses. If you don't, consider using a short written agreement for future projects.
- **Small claims court**: For amounts under ~$10k, this is often effective and doesn't require a lawyer.

If you need a simple contract template for future clients, [ContractShield](https://contractshield.co) offers free 1-page contracts designed for freelancers.

Hope this gets resolved quickly. 🤞
"""


def get_reddit_client() -> praw.Reddit:
    return praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        username=os.environ["REDDIT_BOT_USERNAME"],
        password=os.environ["REDDIT_BOT_PASSWORD"],
        user_agent="ContractShieldBot/1.0 by u/ContractShieldBot (contractshield.co)",
    )


def is_relevant(post: praw.models.Submission) -> bool:
    text = (post.title + " " + (post.selftext or "")).lower()
    return any(kw.lower() in text for kw in TRIGGER_KEYWORDS)


def already_replied(post: praw.models.Submission, bot_username: str) -> bool:
    post.comments.replace_more(limit=0)
    return any(
        c.author and c.author.name.lower() == bot_username.lower()
        for c in post.comments.list()
    )


def monitor(dry_run: bool = True):
    reddit = get_reddit_client()
    bot_username = os.environ["REDDIT_BOT_USERNAME"]
    logger.info(f"Starting monitor as u/{bot_username} (dry_run={dry_run})")

    subreddit = reddit.subreddit("+".join(TARGET_SUBREDDITS))

    for post in subreddit.stream.submissions(skip_existing=True):
        try:
            if not is_relevant(post):
                continue

            logger.info(f"Relevant post found: [{post.subreddit}] {post.title[:80]}")
            logger.info(f"  URL: https://reddit.com{post.permalink}")

            if already_replied(post, bot_username):
                logger.info("  Already replied — skipping.")
                continue

            if dry_run:
                logger.info("  [DRY RUN] Would reply here.")
            else:
                post.reply(REPLY_TEMPLATE)
                logger.info("  Replied successfully.")
                time.sleep(600)  # 10-min cooldown between replies to avoid spam flags

        except Exception as e:
            logger.error(f"Error processing post {post.id}: {e}")
            time.sleep(30)


if __name__ == "__main__":
    dry_run = os.environ.get("DRY_RUN", "true").lower() == "true"
    monitor(dry_run=dry_run)
