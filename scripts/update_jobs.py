#!/usr/bin/env python3
"""Update public recruitment-news leads and keep the official career directory."""
import json, re, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "jobs.json"
FEEDS = [
    "https://news.google.com/rss/search?q=2027%E5%B1%8A+%E8%8D%AF%E4%BC%81+%E6%A0%A1%E6%8B%9B&hl=zh-CN&gl=CN&ceid=CN:zh-Hans",
    "https://news.google.com/rss/search?q=2027%E6%A0%A1%E6%8B%9B+%E5%8C%BB%E8%8D%AF+OR+CRO+OR+%E5%8C%BB%E7%96%97%E5%99%A8%E6%A2%B0&hl=zh-CN&gl=CN&ceid=CN:zh-Hans",
    "https://news.google.com/rss/search?q=2027+graduate+recruitment+pharma+China&hl=en-US&gl=US&ceid=US:en"
]
KEYWORDS = re.compile(r"校招|秋招|春招|校园招聘|应届生|毕业生|graduate|campus|招聘|招募|招聘启事|管培生", re.I)
JUNK = re.compile(r"考研|考公|公务员|高考|招聘会举办|培训班", re.I)
UA = "Mozilla/5.0 (compatible; PharmaCampusJobsBot/1.0; public RSS only)"
def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=25) as resp:
        return resp.read()
def clean(s):
    return re.sub(r"\\s+", " ", s or "").strip()
def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    existing = {j.get("id") for j in data.get("jobs", [])}
    leads = []
    for feed in FEEDS:
        try:
            root = ET.fromstring(get(feed))
            for item in root.findall(".//item"):
                title = clean(item.findtext("title"))
                link = clean(item.findtext("link"))
                desc = clean(re.sub("<[^>]+>", " ", item.findtext("description") or ""))
                pub = clean(item.findtext("pubDate"))
                key = re.sub(r"[^a-z0-9]+", "-", (title + "|" + link).lower()).strip("-")[:140]
                jid = "news-" + __import__("hashlib").sha1((title + "|" + link).encode()).hexdigest()[:16]
                if not title or not link or not KEYWORDS.search(title + " " + desc) or JUNK.search(title):
                    continue
                if jid in existing:
                    continue
                leads.append({
                    "id": jid, "company": "招聘线索（请核验企业）", "title": title,
                    "type": "生命科学/其他", "direction": "综合校招",
                    "sourceType": "公开新闻/RSS线索（非官方岗位页）", "url": link,
                    "location": "以原文为准", "publishedAt": pub,
                    "analysis": "自动发现的公开招聘线索。请打开原文追溯发布企业，再前往企业官方招聘系统核对岗位是否仍开放；此线索不是经过核实的投递岗位。"
                })
                existing.add(jid)
        except Exception as e:
            print("Feed failed:", feed, str(e)[:240])
    # Add newest leads first and cap accumulating old news.
    data["jobs"] = leads[:120] + [j for j in data.get("jobs", []) if not str(j.get("id","")).startswith("news-")][:250]
    data["updatedAt"] = datetime.now(timezone.utc).isoformat()
    data["lastRun"] = {"checkedAt": data["updatedAt"], "feedsAttempted": len(FEEDS), "newLeads": len(leads)}
    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated at", data["updatedAt"], "| new leads:", len(leads), "| total entries:", len(data["jobs"]))
if __name__ == "__main__":
    main()
