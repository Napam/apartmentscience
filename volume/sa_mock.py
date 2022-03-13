from dataclasses import dataclass, field
from typing import Any
import sqlalchemy as sa
from sqlalchemy import orm
import datetime

mapper_registry = orm.registry()

Base = orm.declarative_base()


@mapper_registry.mapped
@dataclass
class Test:
    __table__ = sa.Table(
        "test",
        mapper_registry.metadata,
        sa.Column("_id", sa.Integer, autoincrement=True, primary_key=True),
        sa.Column("_str", sa.UnicodeText),
        sa.Column("_int", sa.Integer),
        sa.Column("_float", sa.Float),
    )
    _id: int = field(init=False)
    _str: str = None
    _int: int = None
    _float: float = None


if __name__ == "__main__":
    engine = sa.create_engine("sqlite:///test.db", echo=True, future=True)
    with orm.Session(engine) as session:
        session.add_all(
            [
                Test(_str="Test1", _int=1, _float=1),
                Test(_str="Test2", _int=2, _float=2),
                Test(_str="Test3", _int=3, _float=3),
            ]
        )
        session.commit()
    # conn: sa.engine.Connection
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
