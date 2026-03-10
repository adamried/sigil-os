#!/usr/bin/env bash
# Hook: load-team-config
# Trigger: SessionStart (after preflight-check)
# Purpose: Detect active team from repo context using user-configured team mappings
#
# SETUP: Create .sigil/team-config.yaml with your team patterns:
#
#   teams:
#     - name: platform
#       patterns: ["platform-*", "*-api", "*-infra"]
#       team_id: "your-jira-team-id"
#       board_id: "123"
#     - name: mobile
#       patterns: ["*-mobile", "*-ios", "*-android"]
#       team_id: "another-team-id"
#       board_id: "456"
#
# The hook matches repo name / remote URL against each team's patterns
# and writes: sigil_team, sigil_team_id, sigil_board_id to .sigil/config.yaml

set -euo pipefail
SIGIL_DIR=".sigil"
CONFIG_FILE="${SIGIL_DIR}/config.yaml"
TEAM_CONFIG="${SIGIL_DIR}/team-config.yaml"

# Exit silently if not in a Sigil project or no team config
[[ -d "$SIGIL_DIR" ]] || exit 0
[[ -f "$TEAM_CONFIG" ]] || exit 0

# Skip if team already set
if grep -q "^sigil_team:" "$CONFIG_FILE" 2>/dev/null; then exit 0; fi

REPO_NAME=$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || echo "")
REMOTE_URL=$(git remote get-url origin 2>/dev/null || echo "")

# Python-based pattern matching against team-config.yaml
python3 - "$REPO_NAME" "$REMOTE_URL" "$TEAM_CONFIG" "$CONFIG_FILE" << 'PYEOF'
import sys
import fnmatch

repo_name = sys.argv[1]
remote_url = sys.argv[2]
team_config_path = sys.argv[3]
config_path = sys.argv[4]

# Minimal YAML parse for team-config structure (no external deps)
def parse_team_config(path):
    teams = []
    current_team = None
    in_patterns = False
    try:
        with open(path) as f:
            for line in f:
                stripped = line.rstrip()
                if stripped.strip().startswith('- name:'):
                    if current_team:
                        teams.append(current_team)
                    current_team = {'name': stripped.split(':', 1)[1].strip(), 'patterns': [], 'team_id': '', 'board_id': ''}
                    in_patterns = False
                elif current_team and 'patterns:' in stripped:
                    in_patterns = True
                elif current_team and in_patterns and stripped.strip().startswith('- '):
                    pat = stripped.strip()[2:].strip().strip('"\'')
                    current_team['patterns'].append(pat)
                elif current_team and 'team_id:' in stripped:
                    in_patterns = False
                    current_team['team_id'] = stripped.split(':', 1)[1].strip().strip('"\'')
                elif current_team and 'board_id:' in stripped:
                    current_team['board_id'] = stripped.split(':', 1)[1].strip().strip('"\'')
        if current_team:
            teams.append(current_team)
    except Exception:
        pass
    return teams

teams = parse_team_config(team_config_path)
match = None
for team in teams:
    for pat in team.get('patterns', []):
        if fnmatch.fnmatch(repo_name, pat) or fnmatch.fnmatch(remote_url, pat):
            match = team
            break
    if match:
        break

if match:
    lines = []
    try:
        with open(config_path) as f:
            lines = f.readlines()
    except FileNotFoundError:
        pass
    with open(config_path, 'a') as f:
        if lines and not lines[-1].endswith('\n'):
            f.write('\n')
        f.write(f"sigil_team: {match['name']}\n")
        if match.get('team_id'):
            f.write(f"sigil_team_id: {match['team_id']}\n")
        if match.get('board_id'):
            f.write(f"sigil_board_id: {match['board_id']}\n")
PYEOF
