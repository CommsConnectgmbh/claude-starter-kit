#!/usr/bin/env python3
"""
second-opinion: lokaler Code-Review als zweite Meinung via Ollama.
Schickt einen Diff (oder Dateien) an ein lokales Code-Modell und gibt
strukturierte Findings zurueck. Kostenlos, laeuft komplett offline.

Usage:
  review.py                      # uneingecheckte Aenderungen (git diff HEAD)
  review.py --staged             # nur gestagte Aenderungen
  review.py --range A..B         # Commit-Range
  review.py file1.py file2.ts    # konkrete Dateien (ganzer Inhalt)
  review.py --model <name>       # anderes Ollama-Modell erzwingen
  review.py --raw                # Diff von stdin

Env:
  OLLAMA_HOST   (default http://localhost:11434)
  SECOND_OPINION_MODEL  (default: erstes verfuegbares coder-Modell)
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

# Backend: "auto" (default) nutzt echtes OpenAI-Codex wenn eingeloggt, sonst Ollama.
# Erzwingen mit SECOND_OPINION_BACKEND=codex|ollama.
BACKEND = os.environ.get("SECOND_OPINION_BACKEND", "auto").lower()

SYSTEM = """Du bist ein extrem gruendlicher, skeptischer Senior-Code-Reviewer und gibst eine ZWEITE MEINUNG zu Code, den ein anderes starkes Modell geschrieben hat. Deine Aufgabe ist NICHT zu loben, sondern echte Probleme zu finden, die dem ersten Modell entgangen sein koennten.

Pruefe gezielt auf:
- Korrektheits-Bugs, Off-by-one, Race Conditions, Null/Undefined, falsche Fehlerbehandlung
- Sicherheitsluecken (Injection, fehlende Validierung, Secrets, Auth/RLS-Luecken)
- Edge-Cases die nicht abgedeckt sind
- Logikfehler die plausibel aussehen aber falsch sind
- Unnoetige Komplexitaet / einfachere Loesung moeglich
- Performance-Fallen

Regeln:
- Sei konkret: Datei + Zeile/Funktion + WARUM es ein Problem ist.
- Erfinde keine Probleme. Wenn etwas korrekt ist, sag es nicht.
- Ordne jedes Finding ein: [BUG] [SECURITY] [EDGE] [SIMPLIFY] [PERF] [NIT].
- Wenn du nichts Substantielles findest, sag klar 'Keine echten Probleme gefunden' statt zu fuellen.
- Kurz und dicht. Keine Einleitung, keine Zusammenfassung am Ende. Nur die Findings als Liste."""


def sh(args):
    return subprocess.run(args, capture_output=True, text=True).stdout


def codex_ready():
    """True wenn Codex-CLI installiert UND eingeloggt (Abo/API-Key)."""
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
    """Review via echtes OpenAI-Codex. Read-only Sandbox, kein Repo-Zwang."""
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
    print(f"# Zweite Meinung ({label}) — {src}\n", flush=True)
    try:
        p = subprocess.run(cmd, input=prompt, capture_output=True,
                           text=True, timeout=900)
        if p.returncode != 0 or not os.path.exists(out_path):
            err = (p.stderr or p.stdout or "unbekannter Fehler").strip()
            print(f"Codex-Call fehlgeschlagen (exit {p.returncode}): {err}\n"
                  f"Tipp: 'codex login' ausfuehren oder SECOND_OPINION_BACKEND=ollama.",
                  file=sys.stderr)
            sys.exit(1)
        with open(out_path, encoding="utf-8", errors="replace") as fh:
            print(fh.read().strip())
    except Exception as e:
        print(f"Fehler beim Codex-Call: {e}", file=sys.stderr)
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
    """Wert direkt nach einem Flag, oder None wenn Flag fehlt/ohne Wert am Ende."""
    if flag not in argv:
        return None
    i = argv.index(flag)
    if i + 1 >= len(argv) or argv[i + 1].startswith("--"):
        return None
    return argv[i + 1]


def die(msg):
    print(f"Fehler: {msg}", file=sys.stderr)
    sys.exit(2)


def collect(argv):
    if "--raw" in argv:
        return sys.stdin.read(), "stdin (raw diff)"
    if "--staged" in argv:
        return sh(["git", "diff", "--cached"]), "git diff --cached"
    if "--range" in argv:
        rng = opt_value(argv, "--range")
        if not rng:
            die("--range braucht einen Wert, z.B. --range main..HEAD")
        return sh(["git", "diff", rng]), f"git diff {rng}"
    # Positionale Argumente = explizit gemeinte Dateien (Option-Werte ausgenommen).
    consumed = {v for f in ("--range", "--model") if (v := opt_value(argv, f))}
    positional = [a for a in argv if not a.startswith("--") and a not in consumed]
    if positional:
        missing = [p for p in positional if not os.path.isfile(p)]
        if missing:
            die("Datei(en) nicht gefunden: " + ", ".join(missing))
        out = []
        for f in positional:
            try:
                with open(f, encoding="utf-8", errors="replace") as fh:
                    out.append(f"=== FILE: {f} ===\n{fh.read()}")
            except Exception as e:
                out.append(f"=== FILE: {f} (lesefehler: {e}) ===")
        return "\n\n".join(out), f"{len(positional)} Datei(en)"
    return sh(["git", "diff", "HEAD"]), "git diff HEAD"


def main():
    argv = sys.argv[1:]
    content, src = collect(argv)
    if not content.strip():
        print("Nichts zu reviewen (leerer Diff). Tipp: --staged, --range A..B oder Dateien angeben.")
        return
    MAX = 60000
    if len(content) > MAX:
        content = content[:MAX] + "\n\n[... abgeschnitten, Diff zu gross ...]"
    user = f"Quelle: {src}\n\nReviewe folgenden Code/Diff:\n\n{content}"

    # Bevorzugt echtes Codex (Abo), sonst lokaler Ollama-Fallback.
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
    print(f"# Zweite Meinung ({model}) — {src}\n", flush=True)
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            resp = json.load(r)
        print(resp["message"]["content"].strip())
    except Exception as e:
        print(f"Fehler beim Ollama-Call ({HOST}): {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
