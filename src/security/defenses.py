# ── Prompt Hacking Defense Helpers ──────────────────────────────────────────
# Defense layers for protecting the AI chatbot from prompt injection attacks.

INJECTION_KEYWORDS = [
    "ignore all previous instructions",
    "ignore previous instructions",
    "forget your role",
    "forget you are",
    "you are now",
    "act as an unrestricted",
    "pretend you are",
    "system prompt",
    "repeat your instructions",
    "jailbreak",
    " dan ",
    "no restrictions",
    "do anything now",
    "your instructions",
    "override your",
]

SUSPICIOUS_RESPONSE_KEYWORDS = [
    "system prompt",
    "my instructions are",
    "i am now",
    "DAN",
    "unrestricted",
    "no longer a cooking",
    "i have no restrictions",
]


def is_injection_attempt(text: str) -> bool:
    """Defense 1: Input Validation — check for known attack patterns."""
    lowered = text.lower()
    return any(keyword in lowered for keyword in INJECTION_KEYWORDS)


def is_suspicious_response(text: str) -> bool:
    """Defense 4: Output Filtering — check if AI response was manipulated."""
    lowered = text.lower()
    return any(keyword in lowered for keyword in SUSPICIOUS_RESPONSE_KEYWORDS)
