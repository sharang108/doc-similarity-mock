import os
from contextlib import contextmanager

import psycopg2


@contextmanager
def db_conn_manager():
    conn = DBUtils.create_conn()
    try:
        yield conn
    finally:
        conn.commit()
        conn.close()


class DBUtils:
    def __init__(self) -> None:
        self.create_embedding_table()

    @staticmethod
    def create_conn() -> any:
        return psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
        )

    def create_embedding_table(self) -> None:
        with db_conn_manager() as conn:
            cursor = conn.cursor()
            create_table_query = """
            CREATE TABLE IF NOT EXISTS documents (
                id SERIAL PRIMARY KEY,
                text TEXT,
                embedding FLOAT[]
            );
            """
            cursor.execute(create_table_query)
            cursor.close()

    def insert_embeddings(self, embeddings: list[tuple]) -> None:
        with db_conn_manager() as conn:
            cursor = conn.cursor()
            for text, embedding in embeddings:
                insert_query = (
                    "INSERT INTO documents (text, embedding) VALUES (%s, %s);"
                )
                cursor.execute(insert_query, (text, embedding))
            cursor.close()

    def get_doc_count(self) -> int:
        with db_conn_manager() as conn:
            cursor = conn.cursor()
            doc_count_query = """select count(id) from documents"""
            cursor.execute(doc_count_query)
            count = cursor.fetchone()[0]
            cursor.close()
            return count

    def get_doc_data(self, offset: int, limit: int):
        with db_conn_manager() as conn:
            cursor = conn.cursor()
            select_query = """select text, embedding from documents order by id 
            offset %s limit %s;
            """
            cursor.execute(select_query, (offset, limit))
            rows = cursor.fetchall()
            cursor.close()
            return rows
