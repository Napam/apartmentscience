import pathlib
import configparser

_alembicConfig = configparser.ConfigParser()
_alembicConfig.read("alembic.ini")

SQL_ADDRESS = _alembicConfig["alembic"]["sqlalchemy.url"]
TMP_DIR = pathlib.Path("data") / "tmp"
FINN_URL = "https://www.finn.no/api/search-qf"
