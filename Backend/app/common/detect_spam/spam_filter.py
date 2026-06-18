import re
from app.constants.spam import SPAM_KEYWORDS, SUSPICIOUS_PATTERNS 

def looks_like_spam(
    message_body: str,
    subject: str = "",
    sender_name: str = "",
) -> bool:
    """
    Basic heuristic spam detector for contact forms.

    Detects common:
    - SEO spam
    - casino/crypto spam
    - marketing junk
    - suspicious link-heavy messages

    This function should NOT be used for permanent rejection.
    Suspicious submissions should instead be flagged or marked
    as spam for review.
    """

    text = (
        f"{subject} {message_body} {sender_name}"
    ).lower()

    score = 0

    # keyword checks
    for keyword in SPAM_KEYWORDS:
        if keyword in text:
            score += 2

    # regex pattern checks
    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, text):
            score += 1

    # excessive links
    url_count = len(
        re.findall(r"https?://|www\.", text)
    )

    if url_count >= 2:
        score += 3

    # excessive length
    if len(message_body) > 4000:
        score += 2

    # repeated characters
    if re.search(r"(.)\1{6,}", text):
        score += 1

    # weird capitalization
    letters_only = [
        c for c in message_body
        if c.isalpha()
    ]

    uppercase_ratio = (
        sum(1 for c in letters_only if c.isupper())
        / max(len(letters_only), 1)
    )

    if uppercase_ratio > 0.5:
        score += 1

    return score >= 4