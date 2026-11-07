# -*- coding: utf-8 -*-
"""一次性完成仓库收尾：CI 校验、distill 分支、topics、v1.0.0 release。

用一次性 classic PAT 通过 GitHub REST / Git Data API 完成，绕开本机 git.exe 的 TLS 问题。
幂等：重复运行会跳过已存在的 CI 文件、distill 分支与 release。
成功后删除 token 文件。
"""
import os, re, sys, json, base64
import urllib.request, urllib.error
from pathlib import Path

TOKEN_FILE = Path(r"D:/漫剧/小说/.github-token")
DISTILL_DIR = Path(r"D:/漫剧/小说/novel-forge-distill")
OWNER, REPO = "zhang78esd", "novel-forge"
BASE = "/repos/%s/%s" % (OWNER, REPO)

TOPICS = ["agent-skills", "claude-code", "claude-skills", "novel-writing",
          "chinese-novel", "webnovel", "writing-assistant",
          "skill-distillation", "cangjie-skill", "prompt-engineering"]

VALIDATE_YML = """name: validate skill

on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Cangjie skill pack validation
        run: |
          git clone --depth 1 https://github.com/kangarooking/cangjie-skill.git "$RUNNER_TEMP/cangjie"
          python "$RUNNER_TEMP/cangjie/scripts/validate_skill_pack.py" .
      - name: RIA++ capability card contract
        run: python .github/scripts/check_cards.py
"""

CHECK_CARDS_PY = """# -*- coding: utf-8 -*-
\"\"\"Check the RIA++ contract for every capability card and all SKILL.md references.\"\"\"
import pathlib, re, sys

root = pathlib.Path(__file__).resolve().parents[2]
skill = root / "SKILL.md"
errors = []

if not skill.exists():
    errors.append("SKILL.md missing")
else:
    text = skill.read_text(encoding="utf-8")
    if not text.startswith("---"):
        errors.append("SKILL.md: missing frontmatter")
    else:
        front = text.split("---", 2)[1]
        for key in ("name:", "description:"):
            if key not in front:
                errors.append("SKILL.md: missing %s in frontmatter" % key)
    for ref in sorted(set(re.findall(r"references/[\\w\\-./]+\\.md", text))):
        if not (root / ref).exists():
            errors.append("broken ref in SKILL.md: %s" % ref)

cap_dir = root / "references" / "capabilities"
caps = sorted(cap_dir.glob("*.md")) if cap_dir.is_dir() else []
if len(caps) != 15:
    errors.append("expected 15 capability cards, found %d" % len(caps))

sections = ("## R \\u2014", "## I \\u2014", "## A1 \\u2014",
            "## A2 \\u2014", "## E \\u2014", "## B \\u2014")
for p in caps:
    t = p.read_text(encoding="utf-8")
    missing = [s for s in sections if s not in t]
    if missing:
        errors.append("%s missing sections: %s" % (p.name, ", ".join(missing)))

if errors:
    print("FAIL")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("PASS: %d capability cards, RIA++ six sections complete, all SKILL.md refs resolve" % len(caps))
"""

RELEASE_NAME = "novel-forge v1.0.0 — 九源蒸馏的中文小说创作 Agent Skill"
RELEASE_BODY = """## novel-forge v1.0.0

用 [kangarooking/cangjie-skill](https://github.com/kangarooking/cangjie-skill) v2.5 的 RIA-TV++ 流水线，把 GitHub 上 9 个高星写小说 skill 蒸馏成 **1 个路由入口 + 15 张 RIA++ 能力卡**。

### 安装

```bash
npx skills add zhang78esd/novel-forge
```

### 内容

- `SKILL.md`：意图路由表 / 7 条核心原则 / 加载规则 / 边界判停
- `references/capabilities/`：15 张能力卡（开书定位、扫榜、拆文、大纲、状态底账、信息边界、伏笔账本、逐章写作、短篇情绪、断点续写、去 AI 味、审查门禁、并行连写、逆向导入、失败模式诊断）
- `references/`：能力索引、速查、术语词典、资料集概览

### 验证

- 仓颉 `validate_skill_pack.py`：**0 errors / 0 warnings**
- 触发评测：**24/24**（15 正例 + 6 诱饵 + 3 边界）
- 输出评测：2 个代表任务 PASS
- 覆盖率：19 类关键任务全部有去向，9/9 来源至少贡献 1 张卡

### 边界

只提炼方法论，不含来源仓库的专有设定与脚本；经验阈值标为诊断参数；触发评测为关键词/意图级确定性匹配，非多模型盲测。详见 `README.md` 与 `distill` 分支的审计文件。

MIT License。
"""


def read_token():
    raw = TOKEN_FILE.read_bytes()
    if raw.startswith(b"\xff\xfe"):
        text, enc = raw.decode("utf-16-le"), "UTF-16 LE"
    elif raw.startswith(b"\xfe\xff"):
        text, enc = raw.decode("utf-16-be"), "UTF-16 BE"
    elif raw.startswith(b"\xef\xbb\xbf"):
        text, enc = raw.decode("utf-8-sig"), "UTF-8 BOM"
    else:
        text, enc = raw.decode("utf-8", errors="replace"), "UTF-8 no BOM"
    cleaned = text.strip().replace("\x00", "")
    for ch in ['"', "'", "\u201c", "\u201d", "\u2018", "\u2019", "`",
               "<", ">", "\u300c", "\u300d", "\u300e", "\u300f"]:
        cleaned = cleaned.strip(ch)
    cleaned = "".join(cleaned.split())
    m = re.search(r"ghp_[A-Za-z0-9]{36}", cleaned) or re.search(r"github_pat_[A-Za-z0-9_]{20,}", cleaned)
    return (m.group(0) if m else cleaned), enc


def api(method, path, token, data=None):
    body = json.dumps(data, ensure_ascii=False).encode("utf-8") if data is not None else None
    req = urllib.request.Request("https://api.github.com" + path, data=body, method=method, headers={
        "Authorization": "Bearer " + token,
        "Accept": "application/vnd.github+json",
        "User-Agent": "novel-forge-finalizer",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            raw = r.read().decode("utf-8")
            return r.status, (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "ignore")
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, {"message": raw[:400]}
    except Exception as e:
        return -1, {"message": str(e).replace(token, "<redacted>")}


def collect_distill_files():
    out = {}
    for p in sorted(DISTILL_DIR.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(DISTILL_DIR).as_posix()
        if "__pycache__" in rel or rel.endswith(".pyc"):
            continue
        out["distill/" + rel] = p.read_bytes()
    return out


def main():
    if not TOKEN_FILE.exists():
        print("WAITING_FOR_TOKEN")
        print("请把 GitHub Personal Access Token 写入：%s" % TOKEN_FILE)
        return 2
    token, enc = read_token()
    print("token file: encoding=%s length=%d" % (enc, len(token)))
    success = False
    try:
        code, me = api("GET", "/user", token)
        if code != 200 or me.get("login", "").lower() != OWNER:
            print("ERROR: token 校验失败 HTTP %s — %s" % (code, me.get("message")))
            return 1
        print("authenticated as: %s" % me["login"])

        code, repo = api("GET", BASE, token)
        if code != 200:
            print("ERROR: 仓库查询失败 HTTP %s" % code)
            return 1
        branch = repo.get("default_branch") or "main"
        code, ref = api("GET", BASE + "/git/ref/heads/" + branch, token)
        if code != 200:
            print("ERROR: 读取 %s 引用失败 HTTP %s" % (branch, code))
            return 1
        main_sha = ref["object"]["sha"]
        code, commit_obj = api("GET", BASE + "/git/commits/" + main_sha, token)
        main_tree = commit_obj["tree"]["sha"]
        print("main head: %s tree: %s" % (main_sha[:8], main_tree[:8]))

        blob_shas = {}

        def blob(content):
            code, r = api("POST", BASE + "/git/blobs", token, {
                "content": base64.b64encode(content).decode("ascii"), "encoding": "base64"})
            if code not in (200, 201):
                raise RuntimeError("blob HTTP %s — %s" % (code, r.get("message")))
            return r["sha"]

        def build_tree(node):
            entries = []
            for name, val in sorted(node.items()):
                if isinstance(val, dict):
                    entries.append({"path": name, "mode": "040000", "type": "tree",
                                    "sha": build_tree(val)})
                else:
                    entries.append({"path": name, "mode": "100644", "type": "blob",
                                    "sha": blob_shas[val]})
            code, r = api("POST", BASE + "/git/trees", token, {"tree": entries})
            if code not in (200, 201):
                raise RuntimeError("tree HTTP %s — %s" % (code, r.get("message")))
            return r["sha"]

        def nest(paths):
            root = {}
            for rel in paths:
                parts = rel.split("/")
                node = root
                for part in parts[:-1]:
                    node = node.setdefault(part, {})
                node[parts[-1]] = rel
            return root

        author = {"name": OWNER, "email": OWNER + "@users.noreply.github.com"}

        # ---------- 1) CI 文件：能写的直接写，workflow 文件缺 scope 时不阻塞 ----------
        ci_pending = []
        ci = {
            ".github/workflows/validate.yml": VALIDATE_YML.encode("utf-8"),
            ".github/scripts/check_cards.py": CHECK_CARDS_PY.encode("utf-8"),
        }
        ci_added = 0
        for rel, content in ci.items():
            code, chk = api("GET", BASE + "/contents/" + rel + "?ref=" + branch, token)
            if code == 200:
                print("already present: %s" % rel)
                continue
            c_put, r_put = api("PUT", BASE + "/contents/" + rel, token, {
                "message": "ci: add " + rel,
                "content": base64.b64encode(content).decode("ascii"),
                "branch": branch,
            })
            if c_put in (200, 201):
                print("added %s" % rel)
                ci_added += 1
            else:
                print("WARN: %s 写入被拒 HTTP %s（classic PAT 缺 workflow scope），模板改放 distill/ci/" % (rel, c_put))
                ci_pending.append((rel, content))
        if ci_added:
            code, ref = api("GET", BASE + "/git/ref/heads/" + branch, token)
            main_sha = ref["object"]["sha"]
            code, commit_obj = api("GET", BASE + "/git/commits/" + main_sha, token)
            main_tree = commit_obj["tree"]["sha"]
            print("CI files committed, main head now: %s" % main_sha[:8])

        # ---------- 2) topics ----------
        code, t = api("PUT", BASE + "/topics", token, {"names": TOPICS})
        if code not in (200, 201):
            print("WARN: topics 设置失败 HTTP %s — %s" % (code, t.get("message")))
        else:
            print("topics set: %s" % ", ".join(x for x in t.get("names", [])))

        # ---------- 3) release / tag v1.0.0 ----------
        code, rel = api("GET", BASE + "/releases/tags/v1.0.0", token)
        if code == 200:
            print("release v1.0.0 already exists: %s" % rel.get("html_url"))
        else:
            code, rel = api("POST", BASE + "/releases", token, {
                "tag_name": "v1.0.0", "target_commitish": branch,
                "name": RELEASE_NAME, "body": RELEASE_BODY,
                "draft": False, "prerelease": False,
            })
            if code not in (200, 201):
                print("WARN: release 创建失败 HTTP %s — %s" % (code, rel.get("message")))
            else:
                print("release created: %s" % rel.get("html_url"))

        # ---------- 4) distill 分支 ----------
        code, existing = api("GET", BASE + "/git/ref/heads/distill", token)
        if code == 200:
            print("distill branch already exists, skipping")
        else:
            dfiles = collect_distill_files()
            for rel, content in ci_pending:
                dfiles["distill/ci/" + rel.split("/")[-1]] = content
            print("distill files to upload: %d (含 %d 个 CI 模板)" % (len(dfiles), len(ci_pending)))
            for rel, content in dfiles.items():
                blob_shas[rel] = blob(content)
            d_tree = build_tree(nest(list(dfiles))["distill"])
            code, r = api("POST", BASE + "/git/trees", token, {
                "base_tree": main_tree,
                "tree": [{"path": "distill", "mode": "040000", "type": "tree", "sha": d_tree}],
            })
            if code not in (200, 201):
                raise RuntimeError("distill root tree HTTP %s — %s" % (code, r.get("message")))
            code, c = api("POST", BASE + "/git/commits", token, {
                "message": "docs: add full distillation workspace on distill branch",
                "tree": r["sha"], "author": author, "committer": author, "parents": [main_sha],
            })
            if code not in (200, 201):
                raise RuntimeError("distill commit HTTP %s — %s" % (code, c.get("message")))
            code, r = api("POST", BASE + "/git/refs", token,
                          {"ref": "refs/heads/distill", "sha": c["sha"]})
            if code not in (200, 201):
                raise RuntimeError("distill ref HTTP %s — %s" % (code, r.get("message")))
            print("distill branch created: %s" % c["sha"][:8])

        # ---------- 5) 验证 ----------
        code, final = api("GET", BASE, token)
        code2, mt = api("GET", BASE + "/git/trees/main?recursive=1", token)
        code3, dt = api("GET", BASE + "/git/trees/distill?recursive=1", token)
        main_blobs = len([x for x in mt.get("tree", []) if x.get("type") == "blob"]) if code2 == 200 else -1
        d_blobs = len([x for x in dt.get("tree", []) if x.get("type") == "blob"]) if code3 == 200 else -1
        code4, release = api("GET", BASE + "/releases/tags/v1.0.0", token)
        print("\n=== RESULT ===")
        print("url          : %s" % final.get("html_url"))
        print("visibility   : %s" % ("private" if final.get("private") else "public"))
        print("topics       : %s" % ", ".join(final.get("topics", [])))
        print("main blobs   : %d" % main_blobs)
        print("distill blobs: %d" % d_blobs)
        print("release      : %s" % (release.get("html_url") if code4 == 200 else "MISSING"))
        print("tag          : %s" % (release.get("tag_name") if code4 == 200 else "MISSING"))
        print("ci workflow  : %s" % ("present" if not ci_pending else "pending manual / workflow-scope token"))
        ok = main_blobs >= 23 and d_blobs >= 25 and code4 == 200 and len(final.get("topics", [])) >= 5
        print("verification : %s" % ("PASS" if ok else "CHECK ABOVE"))
        if not ok:
            return 1
        success = True
        return 0
    finally:
        if success:
            try:
                TOKEN_FILE.unlink()
                print("token file removed: %s" % TOKEN_FILE)
            except Exception as e:
                print("WARN: 请手动删除 token 文件：%s (%s)" % (TOKEN_FILE, e))
        else:
            print("token file kept for retry: %s" % TOKEN_FILE)


if __name__ == "__main__":
    sys.exit(main())
