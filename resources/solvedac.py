from resources import Config 
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import sys 

class SolvedApi:

    def get_recent_solved(user_id : str):
        url = f'https://www.acmicpc.net/status?option-status-pid=on&problem_id=&user_id={user_id}&language_id=-1&result_id=-1'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        response = requests.get(url, headers=headers) 
        
        if response.status_code != 200:
            sys.exit("[!] 유저 최근 문제풀이 정보 기록 가져오기 실패" + response.text)
        
        # 페이지 파싱
        soup = BeautifulSoup(response.text, 'html.parser')
        
        records = soup.find_all('tr')[1:]
        for record in records:
            result_span = record.find('span', class_='result-text result-ac')
            
            if result_span is None:
                continue

            elif result_span.get_text() == '맞았습니다!!' or result_span.get_text() == '100점':
                
                # 문제 제목 추출
                problem_title = record.find('a', class_='problem_title')
                print(problem_title.get('title'))
                
                # 문제 번호 추출    
                print(problem_title.text)
                
                # 타임스탬프 추출
                problem_timestamp = record.find('a', class_='real-time-update')

                # 한국 표준시로 변환
                kst_time = datetime.fromisoformat(problem_timestamp.get('title'))
                print("KST : ", kst_time.isoformat() + "+09:00")
                
                return problem_title.text, kst_time.isoformat()
            
    def get_user_solved(user_id : str):
        url = f"https://solved.ac/api/v3/search/problem?query=solved_by%3A{user_id}&sort=level&direction=desc"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("items")
                
        else:
            sys.exit("[!] 유저 문제풀이 정보 가져오기 실패")
    
    def information_to_data(infor, solution : str, timestamp : str, status : str):
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
                'database_id': Config.DATABASE_ID
            },
            "properties":{
                "링크": {
                    "url": f"https://www.acmicpc.net/problem/{infor['problemId']}" 
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
                        "start": f"{timestamp}" 
                    }
                },
                "상태": {
                    "status": {"name": f"{status}" }
                },
                "문제 번호": {
                    "number": infor['problemId']
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
    
    def get_solved_problem_information(id : str):
        
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
                