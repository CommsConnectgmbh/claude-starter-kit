#!/usr/bin/env python3
"""privacy-guard: PreToolUse-Hook für Claude Code und Codex. Datenschutz technisch erzwingen.

Regel des Setups: Kunden- und Personendaten gehen nur an Dienste mit Auftragsverarbeitungs-
vertrag (AVV), also Codex über ChatGPT Business, oder bleiben lokal (Ollama). Verbraucher-Abos
ohne AVV (Claude Pro/Max, Google AI Pro) bekommen solche Daten nicht.

Zwei Modi:
  privacy-guard.py            Für Codex (die Basis mit AVV). Blockiert nur Übergaben mit
                              Personendaten an Gemini (MCP gemini, Shell gemini-research/agy).
  privacy-guard.py --brain    Für Claude Code auf Pro/Max (das Gehirn ohne AVV). Blockiert
                              zusätzlich alle Werkzeuge, die Kundendaten holen würden
                              (Mail-, CRM-, Kalender-MCPs, siehe CUSTOMER_TOOLS).

Erkannt werden persönliche Mailadressen, IBANs und Pfade in Kunden-Ordner. Funktionsadressen
(info@, support@ ...) sind erlaubt. Namen und Konditionen im Fließtext erkennt kein Hook:
dafür gilt die Regel in CLAUDE.md bzw. AGENTS.md.

Einbindung siehe docs/11-advanced-setup.md, Abschnitt „Datenschutz technisch erzwingen“.
Antwort: JSON permissionDecision=deny auf stdout (versteht Claude Code und Codex).
"""
import json
import re
import sys

BRAIN = "--brain" in sys.argv

# Werkzeuge, die Kundendaten holen. Für das Gehirn (Claude ohne AVV) komplett gesperrt.
# An die eigenen MCP-Namen anpassen.
CUSTOMER_TOOLS = re.compile(
    r"^mcp__(?:(?!__).)*(gmail|outlook|mail|microsoft[_-]?365|graph|crm|hubspot|salesforce|pipedrive|calendar)",
    re.I)
# Übergaben an Modelle ohne AVV.
NO_DPA_MCP = re.compile(r"^mcp__(?:(?!__).)*gemini", re.I)
NO_DPA_CMD = re.compile(r"(^|[\s;&|(/\\`$\"'])(gemini-research|agy|gemini)(\.exe|\.cmd|\.py)?(\s|$|[\"'])", re.I)

EMAIL = re.compile(r"\b([A-Za-z0-9._%+-]+)@([A-Za-z0-9.-]+\.[A-Za-z]{2,})\b")
IBAN = re.compile(r"\b[A-Z]{2}[0-9]{2}(?: ?[0-9A-Z]{4}){3,}")
ROLE = {"hi", "info", "support", "hello", "kontakt", "contact", "noreply", "no-reply",
        "datenschutz", "privacy", "security", "admin", "office", "service", "team",
        "sales", "billing", "abuse", "postmaster", "webmaster", "presse", "press", "jobs"}
ROLE_DOMAINS = {"example.com", "example.org", "example.net", "users.noreply.github.com"}
CUSTOMER_PATH = re.compile(r"[/\\](kunden|customers|accounts)([/\\]|\b)", re.I)


def personal_mail(text):
    return any(m.group(1).lower() not in ROLE and m.group(2).lower() not in ROLE_DOMAINS
               for m in EMAIL.finditer(text))


def reason(text):
    if personal_mail(text):
        return "eine persönliche Mailadresse"
    if IBAN.search(text):
        return "eine IBAN"
    if CUSTOMER_PATH.search(text):
        return "einen Pfad in einen Kunden-Ordner"
    return None


def deny(msg):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                             "permissionDecision": "deny",
                                             "permissionDecisionReason": msg}}, ensure_ascii=True))
    print(msg, file=sys.stderr)
    sys.exit(0)


def main():
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    raw = sys.stdin.buffer.read().decode("utf-8", "replace")
    try:
        d = json.loads(raw)
    except ValueError:
        if re.search(r"gemini|\bagy\b", raw, re.I):
            deny("BLOCKIERT (Datenschutz): Aufruf nicht prüfbar.")
        sys.exit(0)

    tool = str(d.get("tool_name", ""))
    inp = d.get("tool_input", {})
    text = inp if isinstance(inp, str) else json.dumps(inp, ensure_ascii=False)

    if BRAIN and CUSTOMER_TOOLS.match(tool):
        deny(f"BLOCKIERT (Datenschutz): {tool} holt Kundendaten. Claude ist hier das Gehirn ohne "
             "Auftragsverarbeitungsvertrag; Mail- und Kundenarbeit gehört zu Codex (Business) oder lokal.")

    if BRAIN and CUSTOMER_PATH.search(text):
        deny("BLOCKIERT (Datenschutz): Zugriff auf einen Kunden-Ordner. Claude ist hier das Gehirn ohne "
             "Auftragsverarbeitungsvertrag; Kundendaten bearbeitet Codex (Business) oder ein lokales Modell.")

    if NO_DPA_MCP.match(tool):
        why = reason(text)
        if why:
            deny(f"BLOCKIERT (Datenschutz): Übergabe an Gemini enthält {why}. Gemini (Google AI Pro) "
                 "hat keinen Auftragsverarbeitungsvertrag. Aufgabe ohne diese Daten formulieren.")
        sys.exit(0)

    if tool.startswith("mcp__"):
        sys.exit(0)
    cmd = inp.get("command", inp.get("cmd", "")) if isinstance(inp, dict) else text
    cmd = " ".join(map(str, cmd)) if isinstance(cmd, list) else str(cmd)
    if NO_DPA_CMD.search(cmd):
        why = reason(cmd)
        if why:
            deny(f"BLOCKIERT (Datenschutz): Shell-Aufruf an Gemini enthält {why}.")
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        deny("BLOCKIERT (Datenschutz): Hook konnte den Aufruf nicht prüfen.")
