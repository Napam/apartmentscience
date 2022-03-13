import pathlib
import configparser

alembicConfig = configparser.ConfigParser()
alembicConfig.read("alembic.ini")

SQL_ADDRESS = alembicConfig["alembic"]["sqlalchemy.url"]
TMP_DIR = pathlib.Path("data") / "indexjsons"
FINN_URL = "https://www.finn.no/api/search-qf"
