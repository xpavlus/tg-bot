from unittest import TestCase
from sqlalchemy import or_, and_
from test_utils import generate_string
from corp_model import Employee
from sql import db_session, employee_search_query, employee_search_by_name, employee_search_by_id


class Empl:
    def __init__(self):
        self.login = "test_" + generate_string(10, use_numbers=False)
        self.name = generate_string(10, use_numbers=False).capitalize()
        self.surname = generate_string(10, use_numbers=False).capitalize()
        self.email = generate_string(10) + "@test.com"


class TestSQL(TestCase):
    _empl1 = Empl()
    _empl2 = Empl()
    _empl2.name = _empl1.name

    def setUp(self) -> None:
        for e in [self._empl1, self._empl2]:
            db_session.add(
                Employee(
                    login=e.login,
                    first_name=e.name,
                    last_name=e.surname,
                    email=e.email
                )
            )
        db_session.commit()

    def tearDown(self) -> None:
        db_session.query(Employee).filter(
            Employee.login.in_([self._empl1.login, self._empl2.login])
        ).delete()
        db_session.commit()

    def test__employee_search_query(self):
        for _empl in employee_search_query(Employee.login == self._empl1.login):        # Should return one element
            self.assertIsInstance(_empl, Employee)
        for _empl in employee_search_query(Employee.first_name == self._empl1.name):    # Should return two elements
            self.assertIsInstance(_empl, Employee)

    def test_employee_search_by_name(self):
        _query_login = employee_search_by_name(self._empl1.login)    # One element
        self.assertEqual(len(_query_login), 1)
        for _empl in _query_login:
            self.assertEqual(_empl.login, self._empl1.login)

        _query_name = employee_search_by_name(self._empl1.name)      # Two elements
        self.assertEqual(len(_query_name), 2)
        for _empl in _query_name:
            self.assertIn(_empl.login, [self._empl1.login, self._empl2.login])

        _query_surname = employee_search_by_name(self._empl1.surname)      # One element
        self.assertEqual(len(_query_surname), 1)
        for _empl in _query_surname:
            self.assertEqual(_empl.login, self._empl1.login)

    def test_employee_search_by_id(self):
        _empl = db_session.query(Employee).filter(Employee.login == self._empl1.login).first()
        _empl_id = _empl.id
        _query1 = employee_search_by_id(_empl_id)  # one element
        self.assertEqual(_query1.login, self._empl1.login)
