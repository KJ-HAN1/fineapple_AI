import pandas as pd
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

def vectorize_product_data(df):
    # 상품 이름 벡터화 TF-IDF
    vectorize = TfidfVectorizer(stop_words='english')
    product_name_vectors = vectorize.fit_transform(df['name'])

    # 카테고리 벡터화 원- 핫 인코딩
    category_vectors = pd.get_dummies(df['category_id'])

    # 가격 정규화
    scaler = StandardScaler()
    price_vectors = scaler.fit_transform(df[['price']])

    # 벡터화 합치기
    combined_vectors = hstack([product_name_vectors, category_vectors, price_vectors])

    return combined_vectors

def calculate_cosine_similarity(combined_vectors):
    # 코사인 유사도 계산.
    cosine_sim = cosine_similarity(combined_vectors)
    return cosine_sim