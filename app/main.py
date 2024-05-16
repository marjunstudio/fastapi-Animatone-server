from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import firebase_admin
from firebase_admin import auth, credentials

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# サーバーの起動
app = FastAPI()

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