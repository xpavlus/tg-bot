from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import config

sql_connector = "%(engine)s+%(driver)s://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s" % config["database"]
_engine = create_engine(sql_connector)
_session = sessionmaker(bind=_engine)
db_session = _session()
