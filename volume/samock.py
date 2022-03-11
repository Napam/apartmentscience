import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

Base = declarative_base()


if __name__ == "__main__":
    engine = sa.create_engine("sqlite:///test.db", echo=True, future=True)
    conn: sa.engine.Connection
    # with engine.connect() as conn:
    #     conn.execute(
    #         sa.text("INSERT INTO test (text, int, float) VALUES (:text, :int, :float)"),
    #         [
    #             {"text": "aaa", "int": 1, "float": 1},
    #             {"text": "bbb", "int": 2, "float": 2},
    #             {"text": "bbb", "int": "4", "float": "4"},
    #             {"text": None, "int": None, "float": None},
    #             {"text": str([1, 2, 3]), "int": None, "float": None},
    #         ],
    #     )
    #     # conn.execute(sa.text("DELETE FROM test"))
    #     conn.commit()
