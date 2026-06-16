#!/usr/bin/env python3
"""
second-opinion: local code review as a second opinion via Ollama.
Sends a diff (or files) to a local coding model and returns structured
findings. Free, runs entirely offline.

Usage:
  review.py                      # uncommitted changes (git diff HEAD)
  review.py --staged             # staged changes only
  review.py --range A..B         # commit range
  review.py file1.py file2.ts    # specific files (whole content)
  review.py --model <name>       # force a specific Ollama model
  review.py --raw                # diff from stdin

Env:
  OLLAMA_HOST            (default http://localhost:11434)
  SECOND_OPINION_MODEL   (default: first available coder model)
"""
import sys
import os
import json
import subprocess
import urllib.request

HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
PREFERRED = ["qwen2.5-coder:14b-instruct", "qwen2.5-coder", "qwen2.5:14b-instruct"]

SYSTEM = """You are an extremely thorough, skeptical senior code reviewer giving a SECOND OPINION on code that a different strong model wrote. Your job is NOT to praise it but to find real problems the first model may have missed.

Look specifically for:
- Correctness bugs, off-by-one, race conditions, null/undefined, wrong error handling
- Security holes (injection, missing validation, secrets, auth/RLS gaps)
- Edge cases not covered
- Logic bugs that look plausible but are wrong
- Unnecessary complexity / simpler solution possible
- Performance traps

Rules:
- Be concrete: file + line/function + WHY it's a problem.
- Don't invent problems. If something is correct, don't mention it.
- Tag every finding: [BUG] [SECURITY] [EDGE] [SIMPLIFY] [PERF] [NIT].
- If you find nothing substantive, say clearly 'No real problems found' instead of filler.
- Short and dense. No intro, no closing summary. Just findings as a list."""


def sh(args):
    return subprocess.run(args, capture_output=True, text=True).stdout


def pick_model():
    if os.environ.get("SECOND_OPINION_MODEL"):
        return os.environ["SECOND_OPINION_MODEL"]
    try:
        with urllib.request.urlopen(HOST + "/api/tags", timeout=5) as r:
            tags = [m["name"] for m in json.load(r).get("models", [])]
    except Exception:
        return PREFERRED[0]
    for p in PREFERRED:
        for t in tags:
            if t == p or t.startswith(p.split(":")[0]):
                return t
    return tags[0] if tags else PREFERRED[0]


def collect(argv):
    if "--raw" in argv:
        return sys.stdin.read(), "stdin (raw diff)"
    if "--staged" in argv:
        return sh(["git", "diff", "--cached"]), "git diff --cached"
    if "--range" in argv:
        rng = argv[argv.index("--range") + 1]
        return sh(["git", "diff", rng]), f"git diff {rng}"
    files = [a for a in argv if not a.startswith("--") and os.path.isfile(a)]
    if files:
        out = []
        for f in files:
            try:
                with open(f, encoding="utf-8", errors="replace") as fh:
                    out.append(f"=== FILE: {f} ===\n{fh.read()}")
            except Exception as e:
                out.append(f"=== FILE: {f} (read error: {e}) ===")
        return "\n\n".join(out), f"{len(files)} file(s)"
    return sh(["git", "diff", "HEAD"]), "git diff HEAD"


def main():
    argv = sys.argv[1:]
    model = argv[argv.index("--model") + 1] if "--model" in argv else pick_model()
    content, src = collect(argv)
    if not content.strip():
        print("Nothing to review (empty diff). Tip: --staged, --range A..B, or pass files.")
        return
    MAX = 60000
    if len(content) > MAX:
        content = content[:MAX] + "\n\n[... truncated, diff too large ...]"
    user = f"Source: {src}\n\nReview the following code/diff:\n\n{content}"
    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user},
        ],
        "stream": False,
        "options": {"temperature": 0.1, "num_ctx": 16384},
    }).encode()
    req = urllib.request.Request(HOST + "/api/chat", data=payload,
                                 headers={"Content-Type": "application/json"})
    print(f"# Second opinion ({model}) — {src}\n", flush=True)
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            resp = json.load(r)
        print(resp["message"]["content"].strip())
    except Exception as e:
        print(f"Ollama call failed ({HOST}): {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
