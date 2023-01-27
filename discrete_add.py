import re
import requests
from bs4 import BeautifulSoup
import datetime

notion_api_token = 'Your notion api token'
notion_database_id = 'Your database id'

def Discrete_Add():
    # 首先输入
    pattern = re.compile(r"p=(\d+)")
    url_template = input('请输入视频链接：') # 这是链接的模板
    print('由于现在是自定义课表 请输入需要学习的课程的网页编号')
    page_num = list(map(int, input().split()))
    date = datetime.datetime.today()
    cnt = 0
    comment = input('请输入标签：')
    days_interval = int(input('请输入学习间隔天数：'))

    for i in page_num:
        page_url = pattern.sub("p=" + str(i), url_template) # 在url中匹配到的 就用前面的p=替换
        r = requests.get(page_url)
        soup = BeautifulSoup(r.text, 'html.parser') # 解析
        title = soup.find('title').text # 找到对应标题

        url = "https://api.notion.com/v1/pages"
        payload = {
            "parent": {
                "type": "database_id",
                "database_id": notion_database_id,
            },
            "properties": {
            "Name": { "title": [{"type": "text","text": {"content":  title}}]},
                "Tags": {"type": "rich_text", "rich_text": [{"type": "text", "text": {"content": comment}}]},
                "Date": {"date": {"start": date.strftime('%Y-%m-%d')}},
                "URL": {"url": page_url},
            }
        }
        headers = {
            "Accept": "application/json",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + notion_api_token,
        }
        r = requests.post(url, json=payload, headers = headers)
        date += datetime.timedelta(days_interval)
        if r.status_code == 200:
            print(f'Successfully adding {title} into notion database')
            cnt += 1
        else:
            print(f'Failed to add {title} ', r.text)
    print(f'The sum is {cnt}')