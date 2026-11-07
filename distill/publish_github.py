# -*- coding: utf-8 -*-
"""用本地一次性 PAT 创建公开仓库并推送 novel-forge 全部文件。

安全约定：
- token 只从本地文件读取，不打印、不写入 git 配置、不进入命令行输出；
- 所有命令输出都做脱敏；
- 无论成功失败，结束时删除 token 文件。
"""
import os, re, sys, json, subprocess, urllib.request, urllib.error
from pathlib import Path

TOKEN_FILE = Path(r"D:/漫剧/小说/.github-token")
REPO_DIR = Path(r"D:/漫剧/小说/novel-forge")
OWNER = "zhang78esd"
REPO = "novel-forge"
DESC = ("中文小说/网文创作全流程 Agent Skill：用仓颉 skill v2.5 把 9 个开源写小说 skill "
        "蒸馏成 1 个路由入口 + 15 张 RIA++ 能力卡")


def redact(s, token):
    return str(s).replace(token, "<redacted>")


def api(method, path, token, data=None):
    url = "https://api.github.com" + path
    body = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=body, method=method, headers={
        "Authorization": "Bearer " + token,
        "Accept": "application/vnd.github+json",
        "User-Agent": "novel-forge-publisher",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read().decode("utf-8")
            return r.status, (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "ignore")
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, {"message": raw[:300]}
    except Exception as e:
        return -1, {"message": redact(e, token)}


def git(*args, token=None):
    p = subprocess.run(["git"] + list(args), cwd=str(REPO_DIR),
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (p.stdout or "") + (p.stderr or "")
    if token:
        out = redact(out, token)
    if p.returncode != 0:
        raise RuntimeError("git %s failed:\n%s" % (" ".join(args[:2]), out.strip()[:800]))
    return out.strip()


def read_token_file(path):
    """兼容 PowerShell 5.1 的 UTF-16 LE、UTF-8 BOM 与无 BOM UTF-8。"""
    raw = path.read_bytes()
    if raw.startswith(b"\xff\xfe"):
        return raw.decode("utf-16-le"), "UTF-16 LE (PowerShell 5.1 default)"
    if raw.startswith(b"\xfe\xff"):
        return raw.decode("utf-16-be"), "UTF-16 BE"
    if raw.startswith(b"\xef\xbb\xbf"):
        return raw.decode("utf-8-sig"), "UTF-8 with BOM"
    return raw.decode("utf-8", errors="replace"), "UTF-8 no BOM"


def main():
    if not TOKEN_FILE.exists():
        print("WAITING_FOR_TOKEN")
        print("请把 GitHub Personal Access Token 写入：%s" % TOKEN_FILE)
        return 2
    raw_text, enc = read_token_file(TOKEN_FILE)
    cleaned = raw_text.strip().replace("\x00", "")
    for ch in ['"', "'", "\u201c", "\u201d", "\u2018", "\u2019", "`",
               "<", ">", "\u300c", "\u300d", "\u300e", "\u300f"]:
        cleaned = cleaned.strip(ch)
    cleaned = "".join(cleaned.split())
    if cleaned.lower().startswith(("token=", "pat=", "github_token=")):
        cleaned = cleaned.split("=", 1)[1]
    non_ascii = any(ord(c) > 127 for c in cleaned)
    m = (re.search(r"ghp_[A-Za-z0-9]{36}", cleaned) or
         re.search(r"github_pat_[A-Za-z0-9_]{20,}", cleaned) or
         re.search(r"gh[osu]_[A-Za-z0-9]{20,}", cleaned))
    token = m.group(0) if m else cleaned
    kind = ("classic PAT" if token.startswith("ghp_") else
            "fine-grained PAT" if token.startswith("github_pat_") else
            "OAuth/App token" if token.startswith(("gho_", "ghs_", "ghu_")) else
            "unrecognized prefix")
    print("token file: encoding=%s kind=%s length=%d non_ascii=%s extracted=%s" % (
        enc, kind, len(token), non_ascii, bool(m)))
    if len(token) < 20:
        print("ERROR: token 内容为空或过短，请确认文件里只有 token 本身。")
        return 1

    success = False
    try:
        # 1) 校验 token 与账号
        code, me = api("GET", "/user", token)
        if code != 200:
            print("ERROR: token 校验失败 HTTP %s — %s" % (code, me.get("message")))
            print("排查：① token 是否完整复制（classic 通常 40 位）；② 是否已过期或被撤销；")
            print("      ③ 是否误贴了 App/OAuth token 或授权码；④ 生成时是否勾选了 repo 权限。")
            print("token 文件已保留，修正后告诉我重跑即可。")
            return 1
        login = me.get("login")
        print("authenticated as: %s" % login)
        if login.lower() != OWNER.lower():
            print("ERROR: token 属于 %s，与目标账号 %s 不一致，已停止。" % (login, OWNER))
            return 1

        # 2) 仓库不存在则创建（公开、空仓库，避免 README 冲突）
        code, info = api("GET", "/repos/%s/%s" % (OWNER, REPO), token)
        if code == 404:
            code, info = api("POST", "/user/repos", token, {
                "name": REPO, "description": DESC, "private": False,
                "auto_init": False, "has_issues": True, "has_wiki": False,
            })
            if code not in (200, 201):
                print("ERROR: 创建仓库失败 HTTP %s — %s" % (code, info.get("message")))
                return 1
            print("created public repository: %s/%s" % (OWNER, REPO))
        elif code == 200:
            print("repository already exists (private=%s)" % info.get("private"))
            if info.get("size", 0) > 0:
                print("ERROR: 目标仓库已有内容，为避免覆盖已停止。请清空仓库或换个名字。")
                return 1
        else:
            print("ERROR: 查询仓库失败 HTTP %s — %s" % (code, info.get("message")))
            return 1

        # 3) 本地分支统一为 main，并确认提交
        print(git("branch", "-M", "main", token=token))
        head = git("rev-parse", "HEAD", token=token)
        n_files = len(git("ls-files", token=token).splitlines())
        print("local commit: %s | files: %d" % (head[:8], n_files))

        # 4) 一次性推送（token 只在本次命令行，不写入 .git/config）
        push_url = "https://x-access-token:%s@github.com/%s/%s.git" % (token, OWNER, REPO)
        clean_url = "https://github.com/%s/%s.git" % (OWNER, REPO)
        push_failed = False
        try:
            out = git("push", push_url, "main:refs/heads/main", token=token)
            print(redact(out, token)[-600:])
        except RuntimeError as e:
            push_failed = True
            print(redact(e, token))
        finally:
            try:
                if "origin" in git("remote", token=token):
                    git("remote", "remove", "origin", token=token)
                git("remote", "add", "origin", clean_url, token=token)
                git("fetch", "origin", token=token)
                git("branch", "--set-upstream-to=origin/main", "main", token=token)
            except Exception as e:
                print("WARN: 本地 remote/upstream 设置未完成（不影响远端）：%s" % redact(e, token))
        if push_failed:
            return 1

        # 5) 远端验证
        code, info = api("GET", "/repos/%s/%s" % (OWNER, REPO), token)
        code2, items = api("GET", "/repos/%s/%s/contents/" % (OWNER, REPO), token)
        remote_files = len(items) if isinstance(items, list) else -1
        print("\n=== RESULT ===")
        print("url            : %s" % info.get("html_url"))
        print("visibility     : %s" % ("private" if info.get("private") else "public"))
        print("default_branch : %s" % info.get("default_branch"))
        print("root entries   : %d" % remote_files)
        if isinstance(items, list):
            print("root names     : %s" % ", ".join(sorted(x["name"] for x in items)))
        success = True
        return 0
    finally:
        if success:
            try:
                TOKEN_FILE.unlink()
                print("token file removed: %s" % TOKEN_FILE)
            except FileNotFoundError:
                pass
            except Exception as e:
                print("WARN: 请手动删除 token 文件：%s (%s)" % (TOKEN_FILE, e))
        else:
            print("token file kept for retry: %s" % TOKEN_FILE)


if __name__ == "__main__":
    sys.exit(main())
