"""queue/*.json 중 posted/ 에 기록이 없는 글을 Blogger에 올립니다.
publish_at: "now" 또는 한국 시간 "YYYY-MM-DDTHH:MM" (미래면 Blogger 예약 게시).
필요: secrets BLOGGER_CLIENT_ID, BLOGGER_CLIENT_SECRET, BLOGGER_REFRESH_TOKEN, BLOGGER_BLOG_ID
"""
import json, os, pathlib, sys, urllib.parse, urllib.request
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))
API = "https://www.googleapis.com/blogger/v3"

def req(method, url, data=None, token=None, form=False):
    body, headers = None, {}
    if data is not None:
        if form:
            body = urllib.parse.urlencode(data).encode()
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        else:
            body = json.dumps(data).encode()
            headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = "Bearer " + token
    r = urllib.request.Request(url, data=body, method=method, headers=headers)
    try:
        with urllib.request.urlopen(r) as res:
            return json.loads(res.read() or b"{}")
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, e.read().decode()[:500]); raise

def token():
    return req("POST", "https://oauth2.googleapis.com/token", {
        "client_id": os.environ["BLOGGER_CLIENT_ID"], "client_secret": os.environ["BLOGGER_CLIENT_SECRET"],
        "refresh_token": os.environ["BLOGGER_REFRESH_TOKEN"], "grant_type": "refresh_token"}, form=True)["access_token"]

def main():
    blog = os.environ["BLOGGER_BLOG_ID"]
    todo = [p for p in sorted(pathlib.Path("queue").glob("*.json")) if not pathlib.Path("posted", p.name).exists()]
    if not todo:
        print("올릴 글 없음"); return
    tk = token()
    for meta_p in todo:
        meta = json.loads(meta_p.read_text())
        hp = meta_p.with_suffix(".html")
        content = hp.read_text() if hp.exists() else ""
        src = meta.get("content_from")
        if src:
            content = pathlib.Path("queue", src).read_text()
        if meta.get("post_id"):  # 이미 올린 글 고치기
            pub = req("PATCH", f"{API}/blogs/{blog}/posts/{meta['post_id']}", {
                "title": meta["title"], "content": content, "labels": meta.get("labels", [])}, tk)
            rec = {"title": meta["title"], "post_id": pub.get("id"), "url": pub.get("url"), "status": pub.get("status"),
                   "updated": pub.get("updated"), "done_at": datetime.now(KST).isoformat(timespec="minutes"), "update": True}
            pathlib.Path("posted", meta_p.name).write_text(json.dumps(rec, ensure_ascii=False, indent=1))
            print("고침:", rec["url"]); continue
        post = req("POST", f"{API}/blogs/{blog}/posts?isDraft=true", {
            "kind": "blogger#post", "title": meta["title"], "content": content, "labels": meta.get("labels", [])}, tk)
        q = ""
        at = meta.get("publish_at", "now")
        if at != "now":
            when = datetime.fromisoformat(at).replace(tzinfo=KST)
            if when > datetime.now(KST):
                q = "?publishDate=" + urllib.parse.quote(when.isoformat())
        pub = req("POST", f"{API}/blogs/{blog}/posts/{post['id']}/publish{q}", {}, tk)
        rec = {"title": meta["title"], "keyword": meta.get("keyword"), "source_url": meta.get("source_url"),
               "post_id": pub.get("id"), "url": pub.get("url"), "status": pub.get("status"),
               "published": pub.get("published"), "done_at": datetime.now(KST).isoformat(timespec="minutes")}
        pathlib.Path("posted", meta_p.name).write_text(json.dumps(rec, ensure_ascii=False, indent=1))
        print("올림:", rec["status"], rec["url"], rec["published"])

if __name__ == "__main__":
    main()
