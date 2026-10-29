import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urldefrag
import time
import csv

url = "https://www.musashino-u.ac.jp/"

pending = [url]
visited = set()

data = {}

while pending:
    current_url = pending.pop(0)

    if current_url in visited:
        continue

    if visited:
        time.sleep(0.00001)

    visited.add(current_url)

    res = requests.get(current_url)

    print(f"ステータスコード:{res.status_code}")
    print(f"ステータスメッセージ:{res.reason}")

    print("取得したURL:", res.url)
    print("データの種類:", res.headers.get("Content-Type"))
    content_type = res.headers.get("Content-Type", "").lower()

    if "text/html" not in content_type and "application/xhtml+xml" not in content_type:
        continue

    html_soup = BeautifulSoup(res.content, "html.parser")
    title_pick = html_soup.find("title")
    if title_pick is not None:
        data[current_url] = title_pick.get_text()

    href_all = html_soup.find_all("a",href=True)

    for i in href_all:
        link_url = urljoin(current_url, i.get("href"))
        link_url = urldefrag(link_url)[0]
        if urlparse(link_url).scheme not in ("http", "https"):
            continue
        if urlparse(link_url).netloc !=urlparse(url).netloc:
            continue
        if link_url not in visited and link_url not in pending:
            pending.append(link_url)
print(data)
print(len(data))

with open("sitemap.csv", "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["key", "title"])
    writer.writerows(data.items())

print(f"{len(data)}件をCSVに保存しました")
