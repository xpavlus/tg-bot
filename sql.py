from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from main import config
from corp_model import Employee

sql_config = config.get_section('database')

sql_connector = "%(engine)s+%(driver)s://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s" % sql_config
_engine = create_engine(sql_connector)
_session = sessionmaker(bind=_engine)
db_session = _session()


def employee_search(search_criteria: {str: str}) -> [Employee]:
    _search_fields = {
        'name': [
            Employee.first_name,
            Employee.last_name,
            Employee.email],
        'id': [Employee.id, ]
    }
    _search_query = []
    for cr_name, cr_value in search_criteria.items():
        _search_query += [c.ilike(f"%{cr_value}%") for c in _search_fields[cr_name]]

    if len(_search_query) == 1:
        _filter = _search_query[0]
    else:
        _filter = or_(*_search_query)
    _search = db_session.query(Employee).filter(
        _filter
    ).all()
    return _search
