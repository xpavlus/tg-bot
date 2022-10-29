from unittest import TestCase
from sql import employee_search
from sqlalchemy import or_, and_
from test_utils import generate_string
from corp_model import Employee
from sql import db_session


_empl_login1 = "test_" + generate_string(10, use_numbers=False)
_empl_login2 = "test_" + generate_string(10, use_numbers=False)
_empl_name = generate_string(10, use_numbers=False)
_empl1_surname = generate_string(10, use_numbers=False)
_empl2_surname = generate_string(10, use_numbers=False)


class Test(TestCase):
    def setUp(self) -> None:

        db_session.add(Employee(login=_empl_login1, first_name=_empl_name, last_name=_empl1_surname))
        db_session.add(Employee(login=_empl_login2, first_name=_empl_name, last_name=_empl2_surname))
        db_session.commit()

    def tearDown(self) -> None:
        db_session.query(Employee.id).filter(Employee.id.in_([_empl_login1, _empl_login2])).delete()

    def test_employee_search(self):
        self.fail()
