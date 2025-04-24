from pydantic import BaseModel
from typing import List

class RecommendationResponse(BaseModel):
    product_id: int
    recommended_items: List[int]
