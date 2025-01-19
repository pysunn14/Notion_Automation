from resources import Config 
import requests
import sys 

class Notion:
    
    header = {
        "Authorization": f"Bearer {Config.NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    def add_database(data):
        url = f"https://api.notion.com/v1/pages"
        
        response = requests.post(url, headers=Notion.header, data=data)
        if response.status_code == 200:
            print("항목 추가가 완료되었습니다.")
            
        else:
            print("업데이트 실패", response.text)

    def update_database(data, page_id : str):
        url = f"https://api.notion.com/v1/pages/{page_id}"
        
        response = requests.patch(url, headers=Notion.header, data=data)
        if response.status_code == 200:
            print("항목 수정이 완료되었습니다.")
        
        else:
            print("업데이트 실패", response.text)
            
    def get_database(database_id : str):
        url = f"https://api.notion.com/v1/databases/{database_id}/query"
        response = requests.post(url, headers=Notion.header)
        if response.status_code == 200:
            return response.json()
        
        else:
            sys.exit("노션 데이터베이스 정보 요청 실패 : " + response.text)
