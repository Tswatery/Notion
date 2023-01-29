import requests
import datetime

notion_api_token = 'Your notion api token'
notion_database_id = 'Your database id'

def Custom_Add():
    event = input("请输入插入事件名称：")
    comment = input("请输入事件有关标签：")
    days_interval = int(input("请输入事件间隔日期："))
    year, month, day = list(map(int, input('请输入日期 格式为（年，月，日）：').split()))
    date = datetime.datetime(year, month, day)
    for _ in range(5):
        url = "https://api.notion.com/v1/pages"
        payload = {
            "parent": {
                "type": "database_id",
                "database_id": notion_database_id,
            },
            "properties": {
            "Name": { "title": [{"type": "text","text": {"content":  event}}]},
                "Tags": {"type": "rich_text", "rich_text": [{"type": "text", "text": {"content": comment}}]},
                "Date": {"date": {"start": date.strftime('%Y-%m-%d')}},
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
            print(f'在 {date} {event}')
            date += datetime.timedelta(days_interval)
        else:
            print('插入失败', r.text)

Custom_Add()