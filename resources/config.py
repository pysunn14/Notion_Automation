from dotenv import load_dotenv
import os, sys

# 환경 변수 로드 
load_dotenv()

class Config:
    NOTION_API_KEY = os.getenv("NOTION_API_KEY")
    DATABASE_ID = os.getenv("DATABASE_ID")
    USER = os.getenv("USER")
    
    def __init__(self):
        if Config.NOTION_API_KEY is None:
            sys.exit("[!] API KET가 적절하지 않습니다.")
            
        if Config.DATABASE_ID is None:
            sys.exit("[!] Database id가 적절하지 않습니다.")
            
        if Config.USER is None:
            sys.exit("[!] user id가 적절하지 않습니다.")