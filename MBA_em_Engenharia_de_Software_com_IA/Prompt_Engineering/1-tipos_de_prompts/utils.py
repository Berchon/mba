# utils.py — ANSI version (no rich)

RESET = "\033[0m"

BOLD = "\033[1m"

GREEN = "\033[32m"
BLUE = "\033[34m"
WHITE = "\033[37m"
YELLOW = "\033[33m"
BRIGHT_BLACK = "\033[90m"


def estimate_tokens(text: str) -> int:
    """
    Rough token estimation.
    Assumption: ~4 characters per token (common LLM heuristic).
    """
    if not text:
        return 0
    return max(1, len(text) // 4)


def _normalize_gemini_content(content):
    """
    Gemini 3.x may return content as a list of parts.
    Convert it to plain text without changing behavior for other models.
    """
    if isinstance(content, list):
        text_parts = []
        for part in content:
            if isinstance(part, dict) and part.get("type") == "text":
                text_parts.append(part.get("text", ""))
        return "\n".join(text_parts)

    return content


def print_llm_result(prompt, response):
    # --- Prompt ---
    print(f"{BOLD}{GREEN}USER PROMPT:{RESET}")
    print(f"{BOLD}{BLUE}{prompt}{RESET}\n")

    # --- Response ---
    print(f"{BOLD}{GREEN}LLM RESPONSE:{RESET}")

    content = _normalize_gemini_content(response.content)
    content = str(content)

    print(f"{BOLD}{BLUE}{content}{RESET}\n")

    # --- Metadata ---
    metadata = response.response_metadata or {}
    model_name = metadata.get("model_name", "unknown")

    print(f"{BOLD}{WHITE}Model:{RESET} {BRIGHT_BLACK}{model_name}{RESET}")

    # --- Token usage (real or estimated) ---
    token_usage = metadata.get("token_usage")

    if token_usage:
        prompt_tokens = token_usage.get("prompt_tokens", 0)
        completion_tokens = token_usage.get("completion_tokens", 0)
        total_tokens = token_usage.get(
            "total_tokens", prompt_tokens + completion_tokens
        )

        print(f"{BOLD}{GREEN}Token usage (provider):{RESET}")
    else:
        prompt_tokens = estimate_tokens(str(prompt))
        completion_tokens = estimate_tokens(content)
        total_tokens = prompt_tokens + completion_tokens

        print(f"{BOLD}{YELLOW}Token usage (estimated):{RESET}")

    print(f"  Input tokens:  {BRIGHT_BLACK}{prompt_tokens}{RESET}")
    print(f"  Output tokens: {BRIGHT_BLACK}{completion_tokens}{RESET}")
    print(f"  Total tokens:  {BRIGHT_BLACK}{total_tokens}{RESET}")

    print(f"{YELLOW}{'-' * 50}{RESET}")
