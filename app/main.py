from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import firebase_admin
from firebase_admin import auth, credentials

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# サーバーの起動
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # フロントエンドのオリジン
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# リクエストボディの定義
class Message(BaseModel):
    name: str

def get_current_user(cred: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    if not cred:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    try:
        token = cred.credentials
        decoded_token = auth.verify_id_token(token)
        print(f"Decoded Token: {decoded_token}")
        return decoded_token
    except Exception as e:
        print(f"Token verification error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

@app.get("/")
async def root():
    return {"message": "Hello World"}

# getを定義
@app.get("/hello")
def read_root(cred = Depends(get_current_user)):
    uid = cred.get("uid")
    return {"message": f"Hello, {uid}!"}

# postを定義
@app.post("/hello")
def create_message(message: Message, cred = Depends(get_current_user)):
    uid = cred.get("uid")
    return {"message": f"Hello, {message.name}! Your uid is [{uid}]"}

#トークン検証のエンドポイント
@app.post("/verify-token")
def verify_token(cred: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    user = get_current_user(cred)
    return {"uid": user["uid"], "email": user["email"]}

#認証が必要なエンドポイントの保護
@app.get("/protected-endpoint")
def protected_endpoint(user: dict = Depends(get_current_user)):
    return {"message": f"Hello, {user['email']}! This is a protected endpoint."}

