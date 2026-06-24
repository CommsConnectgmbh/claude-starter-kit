@echo off
REM start-claude.bat -- double-clickable Windows Desktop launcher for Claude Code.
REM
REM What it does:
REM   - Opens a Command Prompt window in your user home directory.
REM   - Starts the claude CLI with --dangerously-skip-permissions, so you don't
REM     get asked before every tool call. Only do this on a machine you trust.
REM
REM Install:
REM   1) Copy this file to your Desktop:
REM        copy templates\desktop-launchers\start-claude.bat "%USERPROFILE%\Desktop\"
REM   2) Double-click it.
REM
REM Tip: set CLAUDE_LAUNCHER_WORKDIR before launching to land in a specific dir,
REM      or edit the WORKDIR line below.

setlocal

if "%CLAUDE_LAUNCHER_WORKDIR%"=="" (
  set "WORKDIR=%USERPROFILE%"
) else (
  set "WORKDIR=%CLAUDE_LAUNCHER_WORKDIR%"
)

where claude >nul 2>nul
if errorlevel 1 (
  echo Error: 'claude' is not on PATH.
  echo Install Claude Code first: https://docs.claude.com/en/docs/claude-code
  echo.
  pause
  exit /b 1
)

cd /d "%WORKDIR%" || (
  echo Cannot cd into %WORKDIR%
  pause
  exit /b 1
)

claude --dangerously-skip-permissions
