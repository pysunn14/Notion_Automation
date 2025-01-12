import sys 
import json
import os 
import requests
from dotenv import load_dotenv
from datetime import datetime

# 환경 변수 로드 
load_dotenv()
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("DATABASE_ID")
USER = os.getenv("USER")

if NOTION_API_KEY == None:
    sys.exit("API KET가 적절하지 않습니다.")
    
if DATABASE_ID == None:
    sys.exit("Database id가 적절하지 않습니다.")
    
if USER == None:
    sys.exit("user id가 적절하지 않습니다.")
    
class SolvedAPI:
    
    def get_user_solved(user_id):
        url = f"https://solved.ac/api/v3/search/problem?query=solved_by%3A{user_id}&sort=level&direction=desc"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("items")
                
        else:
            sys.exit("유저 문제풀이 정보 가져오기 실패")
    
    def information_to_data(infor, solution, status):
        
        # level
        
        # 1이 b5로, level값을 5로 나눈 몫이 0 : 브론즈, 1 : 실버, 2 : 골드 3 : 플레티넘...으로 설정 단 5의 배수인 경우 예외처리 (1 줄여주기)
        # level값을 5로 나눈 나머지와 6의 차이 : 티어 내에서 난이도값
        Tier = { "0" : "B", "1" : "S", "2" : "G", "3" : "P", "4" : "D", "5" : "R" }
        
        level = infor['level']
        
        if level == 0:
            tier = "unrated"
        
        else:
            if level % 5 == 0:
                level = infor['level'] // 5 - 1
                tier = Tier[str(level)] + "1"
                
            else:
                level = infor['level'] // 5
                tier = Tier[str(level)] + str(6 - infor['level'] % 5)
        
        # name
        print("문제 : ", infor['titleKo'], tier)
        
        # tags
        tags = infor['tags']
        
        newProblemData = {
            'parent': {
                'type': 'database_id',
                'database_id': DATABASE_ID
            },
            
            "properties":{
                "링크": {
                    "url": f"https://www.acmicpc.net/problem/{id}" 
                },
                "알고리즘": {
                    "multi_select": [
                    ]
                },
                "난이도": {
                    "select": {
                        "name": f"{tier}" 
                    }
                },
                "문제": {
                    "title": [
                        {
                            "text": {
                                "content": f"{infor['titleKo']}"  
                            }
                        }
                    ]
                },
                "날짜": {
                    "date": {
                        "start": f"{datetime.now().date()}" 
                    }
                },
                "상태": {
                    "status": {"name": f"{status}" }
                },
                "문제 번호": {
                    "number": id
                }
            },    
            "children": [  # 페이지 내용
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": "풀이"
                                }
                            }
                        ]
                    }
                },
                {
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": f"{solution}"
                                }
                            }
                        ]
                    }
                }
            ]
        }   
        
        # tags
        for tag in tags:
            newProblemData["properties"]["알고리즘"]["multi_select"].append({"name" : f"{tag['key']}"})
            
        return newProblemData
    
    def get_solved_problem_information(id):
        
        url = 'https://solved.ac/api/v3/problem/show'
        query = {"problemId":f"{id}"}
        header = {
            "x-solvedac-language" : "ko",
            "Accept": "application/json"
        }
        
        response = requests.get(url, headers=header, params=query)
        if(response.status_code == 200):
            return response.json()
            
        else:
            sys.exit("문제를 찾는데 실패했습니다." + response.text)
            
class Notion:
    
    header = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
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

    def update_database(data, page_id):
        url = f"https://api.notion.com/v1/pages/{page_id}"
        
        response = requests.patch(url, headers=Notion.header, data=data)
        if response.status_code == 200:
            print("항목 수정이 완료되었습니다.")
        
        else:
            print("업데이트 실패", response.text)
            
    def get_database(database_id):
        url = f"https://api.notion.com/v1/databases/{database_id}/query"
        response = requests.post(url, headers=Notion.header)
        if response.status_code == 200:
            return response.json()
        
        else:
            sys.exit("노션 데이터베이스 정보 요청 실패 : " + response.text)

if __name__ == '__main__':
    
    id = int(input("문제 번호 입력 : "))
    information = SolvedAPI.get_solved_problem_information(id)
    
    items = SolvedAPI.get_user_solved(USER)
    
    # 이미 노션 데이터베이스에 업로드한 문제인지 판단
    database = Notion.get_database(DATABASE_ID)
    
    for data in database['results']:
        if data['properties']['문제 번호']['number'] == id:
            print('노션에서 해당 문제 항목을 찾았습니다.')
            
            # --- 개발중 ---
            
            sys.exit(0)

    print('아직 노션에 업로드한 문제가 아닙니다. 새로 추가하겠습니다.')
                
    # 아직 업로드한 문제가 아니라면, 이미 푼 문제인지 아닌지 판단 (AC / 미해결 판단)
    for item in items:
        if item['problemId'] == id:
            solution = input("문제 해결 풀이법을 간단하게 적으세요 : ")
            data = SolvedAPI.information_to_data(information, solution, "AC")
            Notion.add_database(json.dumps(data))
            sys.exit(0)
        
    print('아직 해결하지 못한 문제입니다.')
    data = SolvedAPI.information_to_data(information, '해결 중인 문제', "미해결")
    Notion.add_database(json.dumps(data))
    