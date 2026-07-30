#!/usr/bin/env bash
# ============================================================
# laravel-to-fastapi-master — 分档导出（无 zip）
#
# 用法:
#   ./release.sh --oss  <目录> [--update]   导出试读公开仓（MIT · EP00/02/05）
#   ./release.sh --pro  <目录> [--update]   导出付费私有仓（商业授权 · 全 15 期）
#   ./release.sh --meta [oss|pro]           推送 description / topics
#   ./release.sh --check                    工作区与分档清单自检
#
# 拓扑（与 terminal-kit 一致，无 zip）:
#   laravel-to-fastapi-master  (private · 母版)
#     ├── --oss → laravel-to-fastapi       (public · MIT)
#     └── --pro → laravel-to-fastapi-pro   (private · 商业授权)
# ============================================================
set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

g='\033[1;32m'; r='\033[1;31m'; y='\033[1;33m'; b='\033[1;34m'; d='\033[2m'; o='\033[0m'

OSS_REPO="huiyonghkw/laravel-to-fastapi"
PRO_REPO="huiyonghkw/laravel-to-fastapi-pro"

OSS_DESC="Learn FastAPI with Laravel muscle memory. Free trial: 3 runnable lessons (worldview, routing, Pydantic). Left Laravel / right FastAPI, copy-paste and run. Full 15-ep series is the paid private repo."
OSS_TOPICS="laravel,fastapi,python,php,tutorial,openapi,pydantic"
OSS_HOMEPAGE="https://huiyonghkw.github.io/laravel-to-fastapi/"

PRO_DESC="Full Laravel↔FastAPI对照学: all 15 HTML lessons + runnable FastAPI skeleton + Laravel source对照 + Alembic/tests/Docker. Commercial license. Free trial: laravel-to-fastapi (MIT)."
PRO_TOPICS="laravel,fastapi,python,php,tutorial,openapi,pydantic,sqlalchemy,alembic"

# 付费独占：导出 oss 时剔除（按能力：完整路线图，不是残废 demo）
PAID_PATHS=(
  "ep01"
  "ep03"
  "ep04"
  "ep06"
  "ep07"
  "ep08"
  "ep09"
  "ep10"
  "ep11"
  "ep12"
  "ep13"
  "ep14"
  "ep15"
  "fastapi/app/ep01.py"
  "fastapi/app/ep03.py"
  "fastapi/app/ep04.py"
  "fastapi/app/ep06.py"
  "fastapi/app/ep07.py"
  "fastapi/app/ep08.py"
  "fastapi/app/ep09.py"
  "fastapi/app/ep10.py"
  "fastapi/app/ep11.py"
  "fastapi/app/ep13.py"
  "fastapi/app/ep14.py"
  "fastapi/app/ep15.py"
  "fastapi/app/db.py"
  "fastapi/alembic"
  "fastapi/alembic.ini"
  "fastapi/tests/test_ep12.py"
  "PLAN.md"
)

# 只留在母版：导出两档都不带
INTERNAL_PATHS=(
  "release"
)

die() { printf "${r}✗ %s${o}\n" "$*" >&2; exit 1; }
ok()  { printf "  ${g}✓${o} %s\n" "$*"; }
info(){ printf "${b}%s${o}\n" "$*"; }

version() {
  local v
  v="$(tr -d ' \n' < VERSION 2>/dev/null || true)"
  [ -n "$v" ] || die "VERSION 缺失"
  printf '%s' "$v"
}

# ── 拷贝工作区跟踪文件（不含 .git）──
copy_tree() {
  local dest="$1"
  mkdir -p "$dest"
  git ls-files --cached --others --exclude-standard -z 2>/dev/null \
    | while IFS= read -r -d '' f; do
        [ -f "$f" ] || continue
        mkdir -p "$dest/$(dirname "$f")"
        cp "$f" "$dest/$f"
      done
}

apply_overlay() {
  local mode="$1" dest="$2"
  local ov="$SCRIPT_DIR/release/overlays/$mode"
  [ -d "$ov" ] || die "缺少 overlay: $ov"
  # 覆盖同名文件；目录结构保留
  (cd "$ov" && find . -type f -print0) | while IFS= read -r -d '' f; do
    f="${f#./}"
    mkdir -p "$dest/$(dirname "$f")"
    cp "$ov/$f" "$dest/$f"
    printf "  ${d}overlay %s${o}\n" "$f"
  done
}

strip_paid() {
  local dest="$1" p
  info "剔除付费件"
  for p in "${PAID_PATHS[@]}"; do
    if [ -e "$dest/$p" ]; then
      rm -rf "$dest/$p"
      printf "  ${d}- %s${o}\n" "$p"
    fi
  done
}

strip_internal() {
  local dest="$1" p
  for p in "${INTERNAL_PATHS[@]}"; do
    [ -e "$dest/$p" ] && rm -rf "$dest/$p" && printf "  ${d}- internal %s${o}\n" "$p"
  done
}

# 试读 HTML 导航改成试读三期串起来，避免指到已剔除的 EP
fix_oss_nav() {
  local dest="$1"
  local f
  f="$dest/ep00/index.html"
  if [ -f "$f" ]; then
    python3 - "$f" <<'PY'
import pathlib, re, sys
p = pathlib.Path(sys.argv[1])
t = p.read_text(encoding="utf-8")
t = re.sub(
    r'<div class="epnav">.*?</div>',
    '<div class="epnav"><span></span><a class="next" href="../ep02/"><div class="lbl">下一期试读 →</div><div class="ttl">EP02 · 路由</div></a></div>',
    t, count=1, flags=re.S)
p.write_text(t, encoding="utf-8")
PY
  fi
  f="$dest/ep02/index.html"
  if [ -f "$f" ]; then
    python3 - "$f" <<'PY'
import pathlib, re, sys
p = pathlib.Path(sys.argv[1])
t = p.read_text(encoding="utf-8")
t = re.sub(
    r'<div class="epnav">.*?</div>',
    '<div class="epnav"><a class="prev" href="../ep00/"><div class="lbl">← 上一期试读</div><div class="ttl">EP00 · 世界观</div></a><a class="next" href="../ep05/"><div class="lbl">下一期试读 →</div><div class="ttl">EP05 · 校验</div></a></div>',
    t, count=1, flags=re.S)
p.write_text(t, encoding="utf-8")
PY
  fi
  f="$dest/ep05/index.html"
  if [ -f "$f" ]; then
    python3 - "$f" <<'PY'
import pathlib, re, sys
p = pathlib.Path(sys.argv[1])
t = p.read_text(encoding="utf-8")
t = re.sub(
    r'<div class="epnav">.*?</div>',
    '<div class="epnav"><a class="prev" href="../ep02/"><div class="lbl">← 上一期试读</div><div class="ttl">EP02 · 路由</div></a><span></span></div>',
    t, count=1, flags=re.S)
p.write_text(t, encoding="utf-8")
PY
  fi
}

verify_oss() {
  local dest="$1" p
  info "验收 oss"
  for p in ep00 ep02 ep05 fastapi/app/ep00.py fastapi/app/ep02.py fastapi/app/ep05.py LICENSE README.md; do
    [ -e "$dest/$p" ] || die "oss 缺必备: $p"
  done
  for p in "${PAID_PATHS[@]}"; do
    [ -e "$dest/$p" ] && die "oss 仍含付费件: $p"
  done
  grep -q "MIT License" "$dest/LICENSE" || die "oss LICENSE 不是 MIT"
  # 降级真跑：独立 venv → import → pytest（避开 PEP 668）
  local venv="$dest/fastapi/.venv-release-check"
  rm -rf "$venv"
  python3 -m venv "$venv" || die "无法创建 venv"
  # shellcheck disable=SC1091
  . "$venv/bin/activate"
  pip install -q -r "$dest/fastapi/requirements.txt" || die "oss pip install 失败"
  (cd "$dest/fastapi" && python -c "
from fastapi.testclient import TestClient
from app.main import app
c = TestClient(app)
assert c.get('/').json()['tier'] == 'oss-trial'
assert c.get('/ep00/hello').status_code == 200
assert c.get('/ep02/health').status_code == 200
print('http_ok')
") || die "oss main 无法 import 或路由不全"
  (cd "$dest/fastapi" && python -m pytest -q) || die "oss pytest 失败"
  deactivate 2>/dev/null || true
  rm -rf "$venv"
  ok "oss 验收通过"
}

verify_pro() {
  local dest="$1"
  info "验收 pro"
  for p in ep00 ep15 fastapi/app/ep15.py fastapi/alembic LICENSE README.md; do
    [ -e "$dest/$p" ] || die "pro 缺必备: $p"
  done
  grep -q "商业授权" "$dest/LICENSE" || die "pro LICENSE 必须是商业授权"
  grep -qi "MIT License" "$dest/LICENSE" && die "pro LICENSE 不能是 MIT"
  [ -e "$dest/release" ] && die "pro 不应含母版 release/"
  ok "pro 验收通过"
}

build_tree() {
  local mode="$1" dest="$2"
  [ "$mode" = "oss" ] || [ "$mode" = "pro" ] || die "mode 必须是 oss|pro"
  info "导出 $mode → $dest"
  copy_tree "$dest"
  strip_internal "$dest"
  if [ "$mode" = "oss" ]; then
    strip_paid "$dest"
    apply_overlay oss "$dest"
    # 母版 fastapi/app/main.py 已被 overlay 覆盖
    fix_oss_nav "$dest"
    # 确保没有把母版 MIT 以外的东西弄乱：db 已剔
    verify_oss "$dest"
  else
    apply_overlay pro "$dest"
    # 母版若有 MIT LICENSE 文件则已被 pro LICENSE 覆盖
    verify_pro "$dest"
  fi
}

cmd_export() {
  local mode="$1" dest="$2" update="${3:-}"
  [ -n "$dest" ] || die "请指定目标目录"
  dest="$(cd "$(dirname "$dest")" && pwd)/$(basename "$dest")"
  if [ "$update" = "--update" ]; then
    [ -d "$dest/.git" ] || die "--update 目标必须已是 git 仓: $dest"
    if [ -n "$(git -C "$dest" status --porcelain 2>/dev/null)" ]; then
      die "目标仓工作区不干净，先处理: $dest"
    fi
    local tmp
    tmp="$(mktemp -d)"
    build_tree "$mode" "$tmp"
    rsync -a --delete --exclude=.git "$tmp"/ "$dest"/
    rm -rf "$tmp"
    info "已 rsync 到 $dest（未自动提交）"
    git -C "$dest" status --short | head -40
  else
    [ -e "$dest" ] && [ "$(find "$dest" -mindepth 1 -maxdepth 1 | wc -l | tr -d ' ')" != "0" ] \
      && die "目标目录非空，首次导出请给空目录，或改用 --update: $dest"
    mkdir -p "$dest"
    build_tree "$mode" "$dest"
    ok "首次导出完成: $dest"
  fi
}

cmd_check() {
  info "母版自检"
  local v p
  v="$(version)"; ok "VERSION=$v"
  [ -d release/overlays/oss ] || die "缺 oss overlay"
  [ -d release/overlays/pro ] || die "缺 pro overlay"
  for p in "${PAID_PATHS[@]}"; do
    # 允许部分路径尚未存在，但核心 HTML 应付费存在
    :
  done
  for p in ep01 ep06 ep15 fastapi/app/ep15.py; do
    [ -e "$p" ] || die "母版缺付费内容 $p（分档无意义）"
  done
  for p in ep00 ep02 ep05 fastapi/app/ep00.py; do
    [ -e "$p" ] || die "母版缺试读内容 $p"
  done
  # description 长度门（GitHub 350）
  local n
  n="$(printf '%s' "$OSS_DESC" | wc -c | tr -d ' ')"; [ "$n" -le 350 ] || die "OSS_DESC 超 350: $n"
  n="$(printf '%s' "$PRO_DESC" | wc -c | tr -d ' ')"; [ "$n" -le 350 ] || die "PRO_DESC 超 350: $n"
  ok "description 长度合格"
  ok "check 通过"
}

cmd_meta() {
  local which="${1:-both}"
  command -v gh >/dev/null || die "需要 gh"
  if [ "$which" = "oss" ] || [ "$which" = "both" ]; then
    info "meta → $OSS_REPO"
    gh repo edit "$OSS_REPO" -d "$OSS_DESC" --homepage "$OSS_HOMEPAGE"
    # topics：先拿到现有，算差集
    local cur want
    cur="$(gh api "repos/$OSS_REPO" --jq '.topics[]' 2>/dev/null | tr '\n' ' ')"
    IFS=',' read -r -a want_arr <<< "$OSS_TOPICS"
    local t
    for t in $cur; do
      local keep=0 w
      for w in "${want_arr[@]}"; do [ "$t" = "$w" ] && keep=1; done
      [ "$keep" = 0 ] && gh repo edit "$OSS_REPO" --remove-topic "$t" >/dev/null
    done
    for w in "${want_arr[@]}"; do
      gh repo edit "$OSS_REPO" --add-topic "$w" >/dev/null
    done
    ok "oss meta 已推"
  fi
  if [ "$which" = "pro" ] || [ "$which" = "both" ]; then
    info "meta → $PRO_REPO"
    gh repo edit "$PRO_REPO" -d "$PRO_DESC" --homepage ""
    local cur want_arr t w keep
    cur="$(gh api "repos/$PRO_REPO" --jq '.topics[]' 2>/dev/null | tr '\n' ' ')"
    IFS=',' read -r -a want_arr <<< "$PRO_TOPICS"
    for t in $cur; do
      keep=0
      for w in "${want_arr[@]}"; do [ "$t" = "$w" ] && keep=1; done
      [ "$keep" = 0 ] && gh repo edit "$PRO_REPO" --remove-topic "$t" >/dev/null
    done
    for w in "${want_arr[@]}"; do
      gh repo edit "$PRO_REPO" --add-topic "$w" >/dev/null
    done
    ok "pro meta 已推"
  fi
}

usage() {
  sed -n '2,16p' "$0" | sed 's/^# \{0,1\}//'
}

main() {
  [ $# -ge 1 ] || { usage; exit 1; }
  case "$1" in
    --check) cmd_check ;;
    --meta) shift; cmd_meta "${1:-both}" ;;
    --oss)
      shift
      local dest="${1:-}"; shift || true
      local upd=""
      [ "${1:-}" = "--update" ] && upd="--update"
      [ -n "$dest" ] || die "--oss 需要目标目录"
      cmd_export oss "$dest" "$upd"
      ;;
    --pro)
      shift
      local dest="${1:-}"; shift || true
      local upd=""
      [ "${1:-}" = "--update" ] && upd="--update"
      [ -n "$dest" ] || die "--pro 需要目标目录"
      cmd_export pro "$dest" "$upd"
      ;;
    -h|--help) usage ;;
    *) die "未知参数: $1" ;;
  esac
}

main "$@"
