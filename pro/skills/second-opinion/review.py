#!/usr/bin/env python3
"""
second-opinion: code review as a second opinion from a different model.
Prefers OpenAI Codex when logged in, otherwise falls back to a free local
model (Ollama). Sends a diff (or files) and returns structured findings.

Usage:
  review.py                      # uncommitted changes (git diff HEAD)
  review.py --staged             # staged changes only
  review.py --range A..B         # commit range
  review.py file1.py file2.ts    # specific files (whole content)
  review.py --model <name>       # force a specific Ollama model
  review.py --raw                # diff from stdin

Env:
  SECOND_OPINION_BACKEND   auto (default) | codex | ollama
  SECOND_OPINION_CODEX_MODEL   override Codex model (default: CLI default)
  OLLAMA_HOST              (default http://localhost:11434)
  SECOND_OPINION_MODEL    (default: first available coder model)
"""
import sys
import os
import json
import shutil
import tempfile
import subprocess
import urllib.request

HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
PREFERRED = ["qwen2.5-coder:14b-instruct", "qwen2.5-coder", "qwen2.5:14b-instruct"]

# Backend: "auto" (default) uses real OpenAI Codex when logged in, else Ollama.
# Force with SECOND_OPINION_BACKEND=codex|ollama.
BACKEND = os.environ.get("SECOND_OPINION_BACKEND", "auto").lower()

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


def codex_ready():
    """True if the Codex CLI is installed AND logged in (subscription/API key)."""
    if BACKEND == "ollama":
        return False
    if not shutil.which("codex"):
        return False
    try:
        r = subprocess.run(["codex", "login", "status"],
                           capture_output=True, text=True, timeout=15)
        return r.returncode == 0
    except Exception:
        return False


def run_codex(user, src):
    """Review via real OpenAI Codex. Read-only sandbox, no repo required."""
    prompt = SYSTEM + "\n\n" + user
    fd, out_path = tempfile.mkstemp(suffix=".txt")
    os.close(fd)
    cmd = ["codex", "exec", "--skip-git-repo-check", "--ephemeral",
           "-s", "read-only", "--color", "never",
           "-o", out_path]
    model = os.environ.get("SECOND_OPINION_CODEX_MODEL")
    if model:
        cmd += ["-m", model]
    cmd += ["-"]
    label = model or "codex"
    print(f"# Second opinion ({label}) — {src}\n", flush=True)
    try:
        p = subprocess.run(cmd, input=prompt, capture_output=True,
                           text=True, timeout=900)
        if p.returncode != 0 or not os.path.exists(out_path):
            err = (p.stderr or p.stdout or "unknown error").strip()
            print(f"Codex call failed (exit {p.returncode}): {err}\n"
                  f"Tip: run 'codex login' or set SECOND_OPINION_BACKEND=ollama.",
                  file=sys.stderr)
            sys.exit(1)
        with open(out_path, encoding="utf-8", errors="replace") as fh:
            print(fh.read().strip())
    except Exception as e:
        print(f"Codex call failed: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        try:
            os.remove(out_path)
        except OSError:
            pass


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


def opt_value(argv, flag):
    """Value right after a flag, or None if the flag is missing / has no value."""
    if flag not in argv:
        return None
    i = argv.index(flag)
    if i + 1 >= len(argv) or argv[i + 1].startswith("--"):
        return None
    return argv[i + 1]


def die(msg):
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(2)


def collect(argv):
    if "--raw" in argv:
        return sys.stdin.read(), "stdin (raw diff)"
    if "--staged" in argv:
        return sh(["git", "diff", "--cached"]), "git diff --cached"
    if "--range" in argv:
        rng = opt_value(argv, "--range")
        if not rng:
            die("--range needs a value, e.g. --range main..HEAD")
        return sh(["git", "diff", rng]), f"git diff {rng}"
    # Positional arguments = explicitly requested files (option values excluded).
    consumed = {v for f in ("--range", "--model") if (v := opt_value(argv, f))}
    positional = [a for a in argv if not a.startswith("--") and a not in consumed]
    if positional:
        missing = [p for p in positional if not os.path.isfile(p)]
        if missing:
            die("file(s) not found: " + ", ".join(missing))
        out = []
        for f in positional:
            try:
                with open(f, encoding="utf-8", errors="replace") as fh:
                    out.append(f"=== FILE: {f} ===\n{fh.read()}")
            except Exception as e:
                out.append(f"=== FILE: {f} (read error: {e}) ===")
        return "\n\n".join(out), f"{len(positional)} file(s)"
    return sh(["git", "diff", "HEAD"]), "git diff HEAD"


def main():
    argv = sys.argv[1:]
    content, src = collect(argv)
    if not content.strip():
        print("Nothing to review (empty diff). Tip: --staged, --range A..B, or pass files.")
        return
    MAX = 60000
    if len(content) > MAX:
        content = content[:MAX] + "\n\n[... truncated, diff too large ...]"
    user = f"Source: {src}\n\nReview the following code/diff:\n\n{content}"

    # Prefer real Codex (subscription), otherwise local Ollama fallback.
    force_codex = BACKEND == "codex"
    if force_codex or (BACKEND == "auto" and "--model" not in argv and codex_ready()):
        run_codex(user, src)
        return

    model = opt_value(argv, "--model") or pick_model()
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
