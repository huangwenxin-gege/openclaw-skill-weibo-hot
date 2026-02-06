import requests
from bs4 import BeautifulSoup
import datetime
import sys

def get_weibo_hot_search():
    url = "https://s.weibo.com/top/summary"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Cookie": "SUB=1"
    }

    try:
        # 使用本地安装的 python3 运行，确保能找到库
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"抓取失败，状态码: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select("tbody tr")
        
        # 简化输出，方便 Agent 解析或直接展示
        count = 0
        for item in items:
            td_content = item.select_one("td.td-02")
            if not td_content: continue
            
            link_tag = td_content.select_one("a")
            if not link_tag: continue
            
            title = link_tag.get_text().strip()
            # 过滤掉广告（通常没有 rank 数字）
            rank_td = item.select_one("td.td-01")
            rank = rank_td.get_text().strip() if rank_td else ""
            
            if rank.isdigit():
                hot_val_tag = td_content.select_one("span")
                hot_value = hot_val_tag.get_text().strip() if hot_val_tag else "N/A"
                print(f"{rank}. {title} ({hot_value})")
                count += 1
                
            if count >= 10:
                break
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_weibo_hot_search()
