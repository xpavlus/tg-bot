from typing import List

from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.elements import BinaryExpression, BooleanClauseList

from main import config, log
from corp_model import Employee

sql_config = config.get_section('database')

sql_connector = "%(engine)s+%(driver)s://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s" % sql_config
_engine = create_engine(sql_connector)
_session = sessionmaker(bind=_engine)
db_session = _session()


def _employee_search_query(cond) -> list[Employee]:
    _search = db_session.query(Employee).filter(cond)
    _st = _search.statement.compile(_engine, compile_kwargs={"literal_binds": True})
    log.debug(f"Statement: {_st}")
    return _search.all()


def employee_search_by_name(name: str) -> [Employee]:
    log.info(f"Trying to find name: {name}")
    _query = [c.ilike(name) for c in [
        Employee.first_name,
        Employee.last_name,
        Employee.email
    ]]
    return _employee_search_query(or_(*_query))


def employee_search_by_id(emp_id: str) -> Employee:
    log.info(f"Trying to find id: {emp_id}")
    return _employee_search_query(Employee.id == emp_id)[0]
