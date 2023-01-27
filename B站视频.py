import requests
from bs4 import BeautifulSoup
from notion_client import Client
import datetime
import re

notion_api_token = 'secret_LkzKBXTnhokPoxOv3kzhcq9naMVosxZ3UoaXuCLD5u4'
notion_database_id = '4fe3b4ab53a04af894363348b49bc647'

# Initialize a counter
count = 0
# 日期调整
date = datetime.datetime.today()
# 索要视频链接
video_link = input("请输入哔哩哔哩视频链接：")
# 使用者输入的自定义内容
custom_tags = input("请输入自定义标签(用空格隔开)：")
tags_list = custom_tags.split(' ')

# 使用正则表达式匹配页码
pattern = re.compile(r"p=(\d+)")
match = pattern.search(video_link)

# 如果匹配到页码，循环输出视频标题
if match:
    page_num = int(match.group(1))
    start_page = int(input("请输入开始页码："))
    days_interval = int(input("请输入日期间隔天数："))
    for i in range(start_page, page_num + 1):
        # 替换页码
        new_url = pattern.sub("p=" + str(i), video_link)
        # 发送 HTTP 请求，获取 HTML 源代码
        html = requests.get(new_url).text

        # 使用 BeautifulSoup 解析 HTML 源代码
        soup = BeautifulSoup(html, "html.parser")

        # 提取视频标题
        title = soup.find("h1", class_="video-title").text

        # 将页码加到视频标题前面
        title = f"{i}: {title}"

        # 使用 Notion API 将视频标题和发货日期添加到 Notion 数据库中
        url = "https://api.notion.com/v1/pages"
        payload = {
            "parent": {
                "type": "database_id",
                "database_id": notion_database_id,
            },
            "properties": {
            "Name": { "title": [{"type": "text","text": {"content":  title}}]},
                "Tags": {"type": "rich_text", "rich_text": [{"type": "text", "text": {"content":"编译原理"}}]},
                "Date": {"date": {"start": date.strftime('%Y-%m-%d')}},
                "URL": {"url": new_url},
            }
        }
        headers = {
            "Accept": "application/json",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + notion_api_token,
        }
        # Send the request
        response = requests.post(url, json=payload, headers=headers)
        # 将日期往后推
        date += datetime.timedelta(days=days_interval)
        print(date)
        # Check for success
        if response.status_code == 200:
            print(f"Successfully added {title} to Notion database")
            # Increment the counter
            count += 1
        else:
            print(f"Error adding {title} to Notion database:", response.text)
    print(f"Number of videos added to Notion database: {count}")
else:
    print("Invalid video link")