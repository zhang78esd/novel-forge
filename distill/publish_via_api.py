# -*- coding: utf-8 -*-
"""git.exe 的 TLS 握手失败时，改用 GitHub Git Data API 一次性创建 commit 并上传全部文件。

不依赖 git 网络栈；token 不打印、不落盘到配置；成功后删除 token 文件。
"""
import os, re, sys, json, base64
import urllib.request, urllib.error
from pathlib import Path

TOKEN_FILE = Path(r"D:/漫剧/小说/.github-token")
REPO_DIR = Path(r"D:/漫剧/小说/novel-forge")
OWNER, REPO = "zhang78esd", "novel-forge"
BASE = "/repos/%s/%s" % (OWNER, REPO)
COMMIT_MSG = ("feat: novel-forge — 九源蒸馏的中文小说创作 Agent Skill\n\n"
              "1 个路由入口 SKILL.md + 15 张 RIA++ 能力卡 + 索引/速查/术语/概览。\n"
              "由 kangarooking/cangjie-skill v2.5 RIA-TV++ 流水线编译；\n"
              "validate_skill_pack.py 0 errors / 0 warnings，触发评测 24/24。")


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
        "User-Agent": "novel-forge-publisher",
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


def collect_files():
    out = {}
    for p in sorted(REPO_DIR.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(REPO_DIR).as_posix()
        if rel == ".git" or rel.startswith(".git/"):
            continue
        out[rel] = p.read_bytes()
    return out


def main():
    if not TOKEN_FILE.exists():
        print("WAITING_FOR_TOKEN")
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

        code, info = api("GET", BASE, token)
        if code != 200:
            print("ERROR: 仓库查询失败 HTTP %s — %s" % (code, info.get("message")))
            return 1
        print("repository: %s (private=%s, size=%s)" % (info.get("full_name"), info.get("private"), info.get("size")))

        branch = info.get("default_branch") or "main"
        code, existing = api("GET", BASE + "/git/ref/heads/" + branch, token)
        if code == 200:
            print("ERROR: %s 分支已存在且有内容，为避免覆盖已停止。" % branch)
            return 1

        # 空仓库的 Git Data API 会返回 409；先用 Contents API 建立引导提交
        code, boot = api("PUT", BASE + "/contents/.gitkeep", token, {
            "message": "chore: initialize repository",
            "content": base64.b64encode(b"init\n").decode("ascii"),
        })
        if code not in (200, 201):
            print("ERROR: 引导提交失败 HTTP %s — %s" % (code, boot.get("message")))
            return 1
        refinfo = None
        for b in (branch, "main", "master"):
            c2, r2 = api("GET", BASE + "/git/ref/heads/" + b, token)
            if c2 == 200:
                branch, refinfo = b, r2
                break
        if refinfo is None:
            print("ERROR: 引导提交后仍找不到分支引用。")
            return 1
        parent_sha = refinfo["object"]["sha"]
        print("bootstrap commit: %s on %s" % (parent_sha[:8], branch))

        files = collect_files()
        print("local files to upload: %d" % len(files))

        # 1) 为每个文件创建 blob
        blob_sha = {}
        for i, (rel, content) in enumerate(files.items(), 1):
            code, r = api("POST", BASE + "/git/blobs", token, {
                "content": base64.b64encode(content).decode("ascii"),
                "encoding": "base64",
            })
            if code not in (200, 201):
                print("ERROR: blob 创建失败 %s HTTP %s — %s" % (rel, code, r.get("message")))
                return 1
            blob_sha[rel] = r["sha"]
        print("blobs created: %d" % len(blob_sha))

        # 2) 构建嵌套目录树
        tree = {}
        for rel in files:
            parts = rel.split("/")
            node = tree
            for part in parts[:-1]:
                node = node.setdefault(part, {})
            node[parts[-1]] = ("blob", rel)

        def build(node, label):
            entries = []
            for name, val in sorted(node.items()):
                if isinstance(val, dict):
                    sub = build(val, label + "/" + name)
                    entries.append({"path": name, "mode": "040000", "type": "tree", "sha": sub})
                else:
                    entries.append({"path": name, "mode": "100644", "type": "blob",
                                    "sha": blob_sha[val[1]]})
            code, r = api("POST", BASE + "/git/trees", token, {"tree": entries})
            if code not in (200, 201):
                raise RuntimeError("tree %s HTTP %s — %s" % (label, code, r.get("message")))
            return r["sha"]

        root_sha = build(tree, "")
        print("root tree: %s" % root_sha[:8])

        # 3) 创建 commit 与 main 分支
        author = {"name": OWNER, "email": OWNER + "@users.noreply.github.com"}
        code, commit = api("POST", BASE + "/git/commits", token, {
            "message": COMMIT_MSG, "tree": root_sha, "author": author, "committer": author,
            "parents": [parent_sha],
        })
        if code not in (200, 201):
            print("ERROR: commit 创建失败 HTTP %s — %s" % (code, commit.get("message")))
            return 1
        code, ref = api("PATCH", BASE + "/git/refs/heads/" + branch, token,
                        {"sha": commit["sha"], "force": False})
        if code not in (200, 201):
            print("ERROR: ref 更新失败 HTTP %s — %s" % (code, ref.get("message")))
            return 1
        print("commit: %s -> refs/heads/%s" % (commit["sha"][:8], branch))

        api("PATCH", BASE, token, {"default_branch": branch})

        # 4) 远端验证
        code, final = api("GET", BASE, token)
        code2, t = api("GET", BASE + "/git/trees/" + branch + "?recursive=1", token)
        remote_blobs = [x for x in t.get("tree", []) if x.get("type") == "blob"] if code2 == 200 else []
        code3, items = api("GET", BASE + "/contents/", token)
        root_names = sorted(x["name"] for x in items) if isinstance(items, list) else []
        print("\n=== RESULT ===")
        print("url            : %s" % final.get("html_url"))
        print("visibility     : %s" % ("private" if final.get("private") else "public"))
        print("default_branch : %s" % final.get("default_branch"))
        print("remote blobs   : %d (local %d)" % (len(remote_blobs), len(files)))
        print("root entries   : %s" % ", ".join(root_names))
        ok = len(remote_blobs) == len(files)
        print("verification   : %s" % ("PASS" if ok else "MISMATCH"))
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
