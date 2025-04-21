import pandas as pd
from app.db.vectorize import vectorize_product_data, calculate_cosine_similarity
from app.db.connection import get_product_data

def recommend_similar_items(product_id: int):

    df = get_product_data()
    if product_id not in df['product_id'].values:
        return {"message": f"{product_id}에 대한 추천 결과가 없습니다."}

    # 벡터화
    vectors = vectorize_product_data(df)

    cosine_sim = calculate_cosine_similarity(vectors)

    # 상품 ID 기준으로 추천 정리
    sim_df = pd.DataFrame(cosine_sim, index=df['product_id'], columns=df['product_id'])

    # 유사 상품 3개 추출
    similar_items = sim_df[product_id].sort_values(ascending=False).drop(product_id).head(3)

    return {
        "product_id": product_id,
        "recommended_items": similar_items.index.tolist()
    }