from fastapi import APIRouter

from app.db.connection import get_product_data
from app.services.persnal_user_recommender import personal_recommend
from app.services.recommender import recommend_similar_items

router = APIRouter(
    prefix="/api/v1/recommend",
    tags = ["recommend"]
)

@router.get("/{product_id}")
def get_recommendations(product_id: int):
    return recommend_similar_items(product_id)

@router.get("{user_id}")
def personal_recommendations(user_id: int):
    return personal_recommend(user_id)