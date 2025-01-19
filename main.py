from resources import *
import sys 
import json
from datetime import datetime

class Handler:
    
    def update():
        id, timestamp = SolvedApi.get_recent_solved(Config.USER)
        information = SolvedApi.get_solved_problem_information(id)
                
        # 이미 노션 데이터베이스에 업로드한 문제인지 판단
        database = Notion.get_database(Config.DATABASE_ID)
        
        for data in database['results']:
            if data['properties']['문제 번호']['number'] == int(id):
                print('이미 노션에 업로드했던 문제입니다!')        
                # --- 개발중 ---
                page_id = data['id']
                
                # 이미 노션에 올라간 문제라면, 난이도 상태와 유저의 해결 상태가 바뀌었을 수 있으므로 그것을 업데이트하자      
                sys.exit(0)

        print('아직 노션에 업로드한 문제가 아닙니다. 새로 추가하겠습니다.')
        solution = input("문제 해결 풀이법을 간단하게 적으세요 : ")
        data = SolvedApi.information_to_data(information, solution, timestamp, "AC")
        Notion.add_database(json.dumps(data))
        sys.exit(0)

    def notion():
        id = int(input("문제 번호 입력 : "))

        information = SolvedApi.get_solved_problem_information(id)

        items = SolvedApi.get_user_solved(Config.USER)

        # 이미 노션 데이터베이스에 업로드한 문제인지 판단
        database = Notion.get_database(Config.DATABASE_ID)

        for data in database['results']:
            if data['properties']['문제 번호']['number'] == id:
                print('노션에서 해당 문제 항목을 찾았습니다.')

                # --- 개발중 ---
                page_id = data['id']

                # 이미 노션에 올라간 문제라면, 난이도 상태와 유저의 해결 상태가 바뀌었을 수 있으므로 그것을 업데이트하자
                sys.exit(0)

        print('아직 노션에 업로드한 문제가 아닙니다. 새로 추가하겠습니다.')

        # 아직 업로드한 문제가 아니라면, 이미 푼 문제인지 아닌지 판단 (AC / 미해결 판단)
        for item in items:
            if item['problemId'] == id:
                solution = input("문제 해결 풀이법을 간단하게 적으세요 : ")
                data = SolvedApi.information_to_data(information, solution, "AC")
                Notion.add_database(json.dumps(data))
                sys.exit(0)

        print('아직 해결하지 못한 문제입니다.')
        data = SolvedApi.information_to_data(information, "해결 중인 문제", datetime.now(), "미해결")
        json_data = json.dumps(data, indent=4, ensure_ascii=False)
        Notion.add_database(json_data)
        exit(0)

    def codeforces():
        pass 
    
    def option():
        pass 

if __name__ == '__main__':
    
    while True:
        
        cmd = int(input("1 : 문제번호로 올리기 , 2 : codeforce , 3 : option, 4 : exit, 5 : 최근문제기준 업데이트 >> "))
        
        if cmd == 1:
            Handler.notion()
            
        elif cmd == 2:
            Handler.codeforces()
                
        elif cmd == 3:
            Handler.option()
        
        elif cmd == 4:
            sys.exit(0)
        
        elif cmd == 5:
            Handler.update()
            
        else:
            print('try again!')