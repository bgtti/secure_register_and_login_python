"""
SPAM_KEYWORDS can be used to check for common spam keywords in contact form messages.
This list may contain common words, so it should not be used to block content, but rather filter and flag to warn admin(s) to review it.
As any black-list, this is not exaustive and may only catch very common and obvious spam.
"""
import re

SPAM_KEYWORDS = [
    "100% free",
    "100% guaranteed",
    "act now!",
    "avoid bankruptcy",
    "backlinks",
    "be your own boss",
    "best price",
    "betting",
    "big bucks",
    "billion dollars",
    "bitcoin",
    "buy now",
    "casino",
    "click here",
    "collect child support",
    "congratulations",
    "crypto",
    "domain authority",
    "earn money fast",
    "easy money",
    "exclusive invitation",
    "explode your business",
    "extra income",
    "fantastic deal",
    "fast cash",
    "financial freedom",
    "forex",
    "free download",
    "free trial",
    "get paid",
    "get rich",
    "giving away",
    "guest post",
    "increase sales",
    "increase traffic",
    "investment opportunity",
    "join millions of americans",
    "limited time",
    "lose weight",
    "make money online",
    "once in a lifetime",
    "one hundred percent guaranteed",
    "online pharmacy",
    "order now",
    "porn",
    "rank your website",
    "rare opportunity",
    "risk-free",
    "save big money",
    "seo",
    "special invitation",
    "special promotion",
    "sponsored post",
    "telegram",
    "time-sensitive",
    "to our loyal customers",
    "viagra",
    "visit our website",
    "whatsapp investment",
    "work from home",
    "you have been chosen",
    "you have been selected",
    "you've been selected",
    "you're a winner!",
]

SUSPICIOUS_PATTERNS = [

    # URLs
    r"https?://",
    r"www\.",

    # suspicious TLDs
    r"\.click\b",
    r"\.cn\b",
    r"\.info\b",
    r"\.ru\b",
    r"\.shop\b",
    r"\.top\b",
    r"\.work\b",
    r"\.xyz\b",

    # suspicious contact attempts
    r"t\.me/",
    r"wa\.me/",
    r"telegram\.me",

    # suspicious formatting
    r"\$\$\$+",
    r"(?:free|easy|fast)\s+money",

    # crypto wallet patterns
    r"\b(?:btc|eth|usdt)\b",

    # repeated links
    r"(https?://.*?){2,}",
]
