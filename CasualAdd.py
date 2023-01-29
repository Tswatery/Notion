from threadquick import main, worker
import re
import requests
from bs4 import BeautifulSoup
import datetime

notion_api_token = 'Your notion api token'
notion_database_id = 'Your database id'

def CasualAdd():
    url_list = []
    print('请输入要编排的课表链接')
    while 1:
        url = input()
        if url == 'Done': break
        url_list.append(url)
    comment = input('请输入标签：')
    days_interval = int(input('请输入学习间隔天数：'))
    perday = int(input('请输入每天学几节课：'))
    date = datetime.datetime.today()
    cnt = 0
    params_url_list = []
    for i, url in enumerate(url_list):
        params_url_list.append(url)
        print(params_url_list)
        if(len(params_url_list) == perday or i == len(url_list) - 1):
            DayThings = main(params_url_list)
            print(params_url_list)
            params_url_list = [] # 清空
            for item in DayThings:
                title, page_url = item[0], item[1]
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
                if r.status_code == 200:
                    print(f'Successfully adding {title} into notion database')
                    cnt += 1
                else:
                    print(f'Failed to add {title} ', r.text)
            date += datetime.timedelta(days_interval)
    print(f'sum is {cnt}')

# CasualAdd()