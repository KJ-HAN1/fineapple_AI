import logging
from http.client import HTTPException

from fastapi import APIRouter, Request

from app.services.persnal_user_recommender import personal_recommend

router = APIRouter(
    prefix="/api/v1/chat",
    tags = ["recommend"]
)

@router.get("/intro")
async def recommend_chat_intro(request: Request):
    try:
        user_id = request.session.get("user_id")
        if user_id is None:
            raise ValueError("user_id is None")
    except Exception as e:
        logging.warning(f"[Chat Intro] user_id 추출 실패: {e}")
        raise HTTPException(status_code=401, detail="로그인이 필요합니다")

    response = await personal_recommend(user_id)
    return response