import requests
import time

TOKEN = "봇토큰말고 유저토큰 넣으셈"

session = requests.Session()
session.headers.update({
    "Authorization": TOKEN,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
})

print("자동 수락 시작!")

while True:
    try:
        r = session.get("https://discord.com/api/v9/users/@me/relationships")
        pending = [rel for rel in r.json() if rel.get('type') == 3]
        
        if pending:
            for req in pending:
                user = req['user']
                name = user.get('global_name') or user['username']
                
                r = session.put(f"https://discord.com/api/v9/users/@me/relationships/{req['id']}", 
                              json={"confirm_stranger_request": False})
                if r.status_code == 400:
                    r = session.put(f"https://discord.com/api/v9/users/@me/relationships/{req['id']}",
                                   json={"confirm_stranger_request": True})
                
                if r.status_code == 204:
                    print(f"✅ 친구요청 수락성공 : {name}")
                else:
                    print(f"❌ 수락실패 : {name}")
                
                time.sleep(0.1)
        
        time.sleep(0.1)
        
    except KeyboardInterrupt:
        print("\n👋 친구 자동수락 종료")
        break
    except:
        time.sleep(0.1)
