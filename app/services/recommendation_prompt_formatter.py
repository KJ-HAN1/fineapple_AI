import pandas as pd

from app.db.connection import get_product_data


def format_recommendation_prompt(product_id: int, recommended_items: list) -> str:
    """
    상품 ID 및 추천된 상품 ID 리스트를 받아, 자연어 스타일로 추천 메시지를 생성.
    -> llm 프롬프트용

    Parameters:
        product_id (int): 기준 상품 ID
        recommended_items (list): 추천된 상품 ID 목록 3가지 유사 상품 추천
        df (pd.DataFrame): 전체 상품

    Returns:
        str: 자연어 추천 메시지
    """
    df = get_product_data()
    base_product = df[df['product_id'] == product_id].iloc[0]
    base_name = base_product['name']

    recommended_items = df[df['product_id'].isin(recommended_items)]

    lines = [f"최근에 '{base_name}' 상품을 보셨네요. 이와 유사한 제품들을 추천드립니다:"]
    for idx, row in recommended_items.iterrows():
        name = row['name']
        price = row['price']
        category = row['category_id']
        lines.append(f"- '{name}' (가격: {price}원, 카테고리: {category})")

    return "\n".join(lines)