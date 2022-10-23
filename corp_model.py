# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Index, Integer, TIMESTAMP, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TEXT, TINYINT, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Company(Base):
    __tablename__ = 'companies'
    __table_args__ = {'extend_existing': True}

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(255), nullable=False)


class CompaniesEmployee(Base):
    __tablename__ = 'companies_employees'

    id = Column(INTEGER, primary_key=True)
    employee_id = Column(Integer, nullable=False)
    company_id = Column(Integer, nullable=False)
    position = Column(Integer)
    hiring_date = Column(DateTime)
    dismissal_date = Column(DateTime)
    department = Column(Integer, nullable=False)


class Department(Base):
    __tablename__ = 'departments'

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(255), nullable=False)


class Document(Base):
    __tablename__ = 'documents'

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(255), nullable=False, unique=True)
    type = Column(VARCHAR(255), nullable=False)
    size = Column(Integer, nullable=False)
    url = Column(VARCHAR(255), nullable=False)
    folder = Column(Integer, nullable=False)


class Employee(Base):
    __tablename__ = 'employees'

    id = Column(INTEGER, primary_key=True)
    login = Column(VARCHAR(64), nullable=False, unique=True)
    email = Column(VARCHAR(255))
    password = Column(VARCHAR(255))
    last_name = Column(VARCHAR(50), nullable=False)
    first_name = Column(VARCHAR(50), nullable=False)
    middle_name = Column(VARCHAR(255))
    birthdate = Column(Date)
    photo = Column(VARCHAR(255))
    internal_phone = Column(VARCHAR(15))
    external_phone = Column(VARCHAR(15))
    floor = Column(Integer)
    cabinet = Column(VARCHAR(5))
    is_active = Column(TINYINT(1), nullable=False, server_default=text("'1'"))
    notify_flags = Column(Integer, nullable=False, server_default=text("'0'"))
    vacation_from = Column(Date)
    vacation_till = Column(Date)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    remember_token = Column(VARCHAR(100))
    objectguid = Column(VARCHAR(36))

    @property
    def name(self) -> str:
        _name = [self.last_name, self.first_name]
        if self.middle_name:
            _name.append(self.middle_name)
        return " ".join(_name)

    def __repr__(self):
        _attr = [f"{self.last_name} {self.first_name} {self.middle_name or ''}",
                 f"email: {self.email}" if self.email else 'нет эл.почты']
        if self.internal_phone:
            _attr.append(f"тел.: {self.internal_phone}")
        if self.external_phone:
            _attr.append(f"моб.: {self.external_phone}")
        return ", ".join(_attr)


class PersonalAccessToken(Base):
    __tablename__ = 'personal_access_tokens'
    __table_args__ = (
        Index('personal_access_tokens_tokenable_type_tokenable_id_index', 'tokenable_type', 'tokenable_id'),
    )

    id = Column(BIGINT, primary_key=True)
    tokenable_type = Column(VARCHAR(255), nullable=False)
    tokenable_id = Column(BIGINT, nullable=False)
    name = Column(VARCHAR(255), nullable=False)
    token = Column(VARCHAR(64), nullable=False, unique=True)
    abilities = Column(TEXT)
    last_used_at = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
