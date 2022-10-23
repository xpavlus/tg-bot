from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker

from config import config
from corp_model import Employee

sql_connector = "%(engine)s+%(driver)s://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s" % config["database"]
_engine = create_engine(sql_connector)
_session = sessionmaker(bind=_engine)
db_session = _session()


def employee_search(name: str) -> [Employee]:
    _search_fields = [
        Employee.first_name,
        Employee.last_name,
        Employee.email
    ]
    _search_query = [c.ilike(f"%{name}%") for c in _search_fields]
    _search = db_session.query(Employee).filter(
        or_(*_search_query)
    ).all()
    return _search
