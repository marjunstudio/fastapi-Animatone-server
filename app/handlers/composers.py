from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session, Depends
from typing import Annotated
from database import SessionLocal

from app.models.composers import Composer

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.get("/composers", tags=["作曲者"], summary="テーブルに保存されている作曲者情報を取得する", description="ここにエンドポイントの説明を記載する")
async def get_composers(db: Annotated[Session, Depends(get_db)]):
    composers = await get_composers_from_db(db)
    return composers

def get_composers_from_db(db: Session):
    try:
        composers = db.query(Composer).all()
        return composers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
