from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Annotated
from app.database.database import SessionLocal
from app.models.composers import Composer

from app.models.composers import Composer

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.get("/api/composers", tags=["作曲者"], summary="テーブルに保存されている作曲者情報を取得する", description="ここにエンドポイントの説明を記載する")
def get_composers(db: Annotated[Session, Depends(get_db)]):
    # composers = await get_composers_from_db(db)
    composers = get_composers_from_db()
    return composers

# def get_composers_from_db(db: Session):
#     try:
#         composers = db.query(Composer).all()
#         return composers
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    

def get_composers_from_db():
    composers = [
        {
            "id": 1,
            "name": "真島俊夫",
            "furigana": "ましまとしお",
        },
        {
            "id": 2,
            "name": "福島弘和",
            "furigana": "ふくしまひろかず",
        },
        {
            "id": 3,
            "name": "鈴木英史",
            "furigana": "すずきえいじ",
        },
        {
            "id": 4,
            "name": "酒井格",
            "furigana": "さかいいたる",
        }
    ]
    return composers
