#!/usr/bin/env bash
# secret — unified credential CLI. private repo. bash + python3 stdlib.
set -euo pipefail

SECRET_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CREDS="${SECRET_ROOT}/credentials"
FLAT_SECTION="flat"

_die() { echo "secret: $*" >&2; exit 2; }

# key normalization
#   dotted form  : section.name        (lowercase + underscore, single dot)
#   flat form    : ANY_UPPER_SNAKE     -> stored under [flat] as lowercased name
#                  except prefixed forms like AWS_BRAKET_REGION -> aws_braket.region
#                  if the leading token matches an existing section.
_resolve_key() {
    local raw="$1"
    [[ -z "$raw" ]] && _die "key required"
    [[ "$raw" == *".."* ]] && _die "key contains '..'"
    [[ "$raw" == "/"* || "$raw" == "."* ]] && _die "key starts with reserved char"
    if [[ "$raw" == *.* ]]; then
        local lc; lc="$(printf '%s' "$raw" | tr '[:upper:]' '[:lower:]')"
        [[ "$lc" =~ ^[a-z][a-z0-9_]*\.[a-z][a-z0-9_]*$ ]] || \
            _die "key must be section.name (lowercase + underscore), got '$raw'"
        printf '%s' "$lc"
        return
    fi
    [[ "$raw" =~ ^[A-Za-z][A-Za-z0-9_]*$ ]] || _die "invalid flat key '$raw'"
    local lc; lc="$(printf '%s' "$raw" | tr '[:upper:]' '[:lower:]')"
    # try to match leading token against existing sections
    if [ -f "$CREDS" ]; then
        local sec
        while IFS= read -r sec; do
            [[ -z "$sec" ]] && continue
            if [[ "$lc" == "${sec}_"* ]]; then
                printf '%s.%s' "$sec" "${lc#${sec}_}"
                return
            fi
        done < <(SECRET_PATH="$CREDS" python3 - <<'PY'
import os, re
for line in open(os.environ["SECRET_PATH"]):
    m = re.match(r'^\[([^\]]+)\]\s*$', line.strip())
    if m:
        print(m.group(1))
PY
)
    fi
    printf '%s.%s' "$FLAT_SECTION" "$lc"
}

_get() {
    local key; key="$(_resolve_key "$1")"
    [ -f "$CREDS" ] || _die "credentials not found at $CREDS"
    local section="${key%.*}" name="${key#*.}"
    SECRET_SECTION="$section" SECRET_NAME="$name" SECRET_PATH="$CREDS" \
    python3 - <<'PY' || { _suggest "$key"; exit 1; }
import os, re, sys
section = os.environ["SECRET_SECTION"]
name    = os.environ["SECRET_NAME"]
path    = os.environ["SECRET_PATH"]
with open(path) as f:
    text = f.read()
in_section = False
for line in text.splitlines():
    s = line.strip()
    if not s or s.startswith('#'):
        continue
    m = re.match(r'^\[([^\]]+)\]\s*$', s)
    if m:
        in_section = (m.group(1).strip() == section)
        continue
    if in_section:
        mm = re.match(r'^(\w+)\s*=\s*["\'](.*)["\']\s*$', s)
        if mm and mm.group(1) == name:
            sys.stdout.write(mm.group(2))
            sys.exit(0)
sys.exit(1)
PY
}

_list() {
    [ -f "$CREDS" ] || _die "credentials not found"
    SECRET_PATH="$CREDS" python3 - <<'PY'
import os, re
path = os.environ["SECRET_PATH"]
current = None
with open(path) as f:
    for line in f:
        s = line.strip()
        if not s or s.startswith('#'):
            continue
        m = re.match(r'^\[([^\]]+)\]\s*$', s)
        if m:
            current = m.group(1).strip()
            continue
        if current:
            mm = re.match(r'^(\w+)\s*=\s*', s)
            if mm:
                print(f"{current}.{mm.group(1)}")
PY
}

_all_keys() { _list 2>/dev/null || true; }

_suggest() {
    local missing="$1"
    echo "secret: key '$missing' not found" >&2
    local hint
    hint="$(_all_keys | awk -v k="$missing" '
        BEGIN{best=""; bestlen=0}
        { n=length(k); m=length($0); s=0
          for(i=1;i<=n;i++){ for(j=1;j<=m;j++){ if(substr(k,i,1)==substr($0,j,1)){s++; break} } }
          if(s>bestlen){bestlen=s; best=$0} }
        END{ if(best!="") print best }')"
    [ -n "$hint" ] && echo "secret: did you mean '$hint'?" >&2
    return 0
}

# read value safely:
#   - argv form: $1 carries value (user-chosen convenience, value in shell history)
#   - tty stdin: prompt with read -s (echo off)
#   - pipe stdin: read raw, strip single trailing newline
_read_value() {
    if [ "$#" -ge 1 ]; then
        printf '%s' "$1"
        return
    fi
    if [ -t 0 ]; then
        local v
        IFS= read -rs -p "value: " v </dev/tty
        echo >&2
        printf '%s' "$v"
        return
    fi
    local v
    v="$(cat)"
    printf '%s' "${v%$'\n'}"
}

_set() {
    local raw="$1"; shift || true
    local key; key="$(_resolve_key "$raw")"
    local section="${key%.*}" name="${key#*.}"
    local value
    value="$(_read_value "$@")"
    [ -n "$value" ] || _die "empty value (stdin/argv both empty)"
    mkdir -p "$(dirname "$CREDS")"
    if [ ! -f "$CREDS" ]; then
        printf '# secret credentials — private repo\n' > "$CREDS"
    fi
    chmod 600 "$CREDS"
    SECRET_SECTION="$section" SECRET_NAME="$name" SECRET_VALUE="$value" SECRET_PATH="$CREDS" \
    python3 - <<'PY'
import os, re
section = os.environ["SECRET_SECTION"]
name    = os.environ["SECRET_NAME"]
value   = os.environ["SECRET_VALUE"]
path    = os.environ["SECRET_PATH"]
with open(path) as f:
    lines = f.read().splitlines()
out = []
current = None
section_found = False
key_replaced = False
for raw in lines:
    s = raw.strip()
    m = re.match(r'^\[([^\]]+)\]', s)
    if m:
        if current == section and not key_replaced:
            out.append(f'{name} = "{value}"')
            key_replaced = True
        current = m.group(1).strip()
        if current == section:
            section_found = True
        out.append(raw)
        continue
    mm = re.match(r'^(\w+)\s*=', s)
    if mm and current == section and mm.group(1) == name:
        out.append(f'{name} = "{value}"')
        key_replaced = True
    else:
        out.append(raw)
if current == section and not key_replaced:
    out.append(f'{name} = "{value}"')
    key_replaced = True
if not section_found:
    if out and out[-1].strip():
        out.append('')
    out.append(f'[{section}]')
    out.append(f'{name} = "{value}"')
with open(path, 'w') as f:
    f.write('\n'.join(out) + '\n')
PY
    chmod 600 "$CREDS"
    echo "ok: ${section}.${name}" >&2
}

_rm() {
    local key; key="$(_resolve_key "$1")"
    [ -f "$CREDS" ] || _die "credentials not found"
    local section="${key%.*}" name="${key#*.}"
    SECRET_SECTION="$section" SECRET_NAME="$name" SECRET_PATH="$CREDS" \
    python3 - <<'PY'
import os, re, sys
section = os.environ["SECRET_SECTION"]
name    = os.environ["SECRET_NAME"]
path    = os.environ["SECRET_PATH"]
with open(path) as f:
    lines = f.read().splitlines()
out = []
current = None
removed = False
for raw in lines:
    s = raw.strip()
    m = re.match(r'^\[([^\]]+)\]', s)
    if m:
        current = m.group(1).strip()
        out.append(raw)
        continue
    mm = re.match(r'^(\w+)\s*=', s)
    if mm and current == section and mm.group(1) == name:
        removed = True
        continue
    out.append(raw)
if not removed:
    sys.exit(3)
# strip empty sections
final, i = [], 0
while i < len(out):
    s = out[i].strip()
    if s.startswith('['):
        j = i + 1
        while j < len(out) and not out[j].strip().startswith('['):
            j += 1
        body = [x for x in out[i+1:j] if re.match(r'^\w+\s*=', x.strip())]
        if not body:
            while final and final[-1].strip() == '': final.pop()
            i = j; continue
    final.append(out[i]); i += 1
while final and final[-1].strip() == '': final.pop()
with open(path, 'w') as f:
    f.write('\n'.join(final) + '\n')
PY
    local rc=$?
    if [ $rc -eq 3 ]; then
        _suggest "$key"
        exit 1
    fi
    chmod 600 "$CREDS"
    echo "removed: ${section}.${name}" >&2
}

_check() {
    local key; key="$(_resolve_key "$1")"
    _get "$key" >/dev/null 2>&1 && exit 0 || exit 1
}

_help() {
    cat <<EOF
secret — unified credential CLI

usage:
  secret get  <key>                read value to stdout (no trailing newline)
  secret set  <key> [value]        write value; argv (convenient) or stdin (safe)
  secret rm   <key>                delete key
  secret check <key>               exit 0 if exists, 1 otherwise
  secret list                      enumerate keys (values hidden)
  secret help                      this text

key forms:
  section.name                     dotted, lowercase + underscore (e.g. zenodo.token)
  FLAT_UPPER                       auto-mapped: AWS_BRAKET_REGION -> aws_braket.region
                                   unmatched -> [flat] section (e.g. MY_TOKEN -> flat.my_token)

set forms:
  secret set zenodo.token \$TOKEN          # argv: convenient, leaks to shell history + ps
  echo \$TOKEN | secret set zenodo.token   # pipe: no history, no echo
  secret set zenodo.token                 # tty: prompts with read -s (no echo)

examples:
  secret get runpod.api_key
  secret set AWS_BRAKET_REGION us-east-1
  pbpaste | secret set github.token
  secret rm test.probe
  secret check arxiv.user && echo configured
EOF
}

case "${1:-help}" in
    get)        shift; [ $# -ge 1 ] || { _list; exit 0; }; _get "$1" ;;
    list|ls)    _list ;;
    set)        shift; [ $# -ge 1 ] || _die "set requires <key>"; _set "$@" ;;
    rm|del|delete) shift; [ $# -ge 1 ] || _die "rm requires <key>"; _rm "$1" ;;
    check)      shift; [ $# -ge 1 ] || _die "check requires <key>"; _check "$1" ;;
    help|-h|--help) _help ;;
    *) _die "unknown command '$1'. try: secret help" ;;
esac
