import mysql.connector
from mysql.connector import pooling
import pandas as pd
from app.core import config
from elasticsearch import Elasticsearch

es = Elasticsearch(
    [config.ES_HOST]
)

dbconfig = {
    "host": config.DB_HOST,
    "user": config.DB_USER,
    "password":config.DB_PASSWORD,
    "database":config.DB_NAME
}
# 커넥션 풀 생성 size만큼 접속 가능
connection_pool = pooling.MySQLConnectionPool(
    pool_name="click_pool",
    pool_size=5,
    **dbconfig
)

# 클릭로그 커넥션 풀에서 받아오기
def get_click_log():
    conn = connection_pool.get_connection()

    try:
        query = "SELECT user_id, session_id, product_id FROM ClickLog"
        click_log_df = pd.read_sql(query, conn)
    finally:
        conn.close()
    return click_log_df

# 벡터화용 상품테이블 정보 가져오기
def get_product_data():
    conn = connection_pool.get_connection()
    try:
        query = "SELECT product_id, name, category_id, price FROM Product"
        product_data_df = pd.read_sql(query, conn)
    finally:
        conn.close()
    return product_data_df

#유저의 최근 본 상품 정보
# def get_recent_view_product(user_id):
#     conn = connection_pool.get_connection()
#     try:
#         query = """
#         select product_id, clicked_at from ClickLog
#         where user_id = %s
#         order by clicked_at desc
#         limit 1;
#         """
#         recent_view_df = pd.read_sql(query, conn, params=(user_id,))
#     finally:
#         conn.close()
#     return recent_view_df
def get_recent_view_product_from_els(user_id, index="product-access-*"):
    try:
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"userId.keyword": str(user_id)}},  # userId.keyword 사용
                        {"term": {"eventType.keyword": "product_access"}}  # eventType도 keyword로 사용
                    ]
                }
            },
            "sort": [
                {"@timestamp": {"order": "desc"}}
            ],
            "size": 1
        }

        response = es.search(index=index, body=query)
        hits = response["hits"]["hits"]
        if not hits:
            return pd.DataFrame()

        doc = hits[0]["_source"]
        return pd.DataFrame([{
            "product_id": doc.get("productId"),
            "clicked_at": doc.get("@timestamp")
        }])
    except Exception as e:
        print(f"[ERROR] Elasticsearch 조회 실패: {e}")
        return pd.DataFrame()