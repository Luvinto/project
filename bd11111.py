from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from pydantic import BaseModel, field_validator
from sqlalchemy.types import Enum as SQLEnum
from typing import Literal
from pydantic import EmailStr


Base=declarative_base()

class Users(Base):
    __tablename__='Users'
    id=Column(Integer, primary_key=True)
    login=Column(String, unique=True)
    password=Column(String)
    email=Column(String)
    age=Column(Integer)
    groups=Column(SQLEnum('Ученик', 'Учитель', name='group_enum'))
    progress=relationship('Progress', back_populates='users')

class Users_validation(BaseModel):
    id:int
    login:str
    password:str
    email:EmailStr
    age:int
    groups:Literal['Ученик', 'Учитель']

    @field_validator('email')
    def validation_email(cls, email):
        if '@' not in email:
            raise ValueError(f'Недопустимое имя электронной почты: {email}')
        return email

    @field_validator('age')
    def validation_age(cls, age):
        if age>99:
            raise ValueError('Слишком старый))))')
        return age

    @field_validator('password')
    def validation_password(cls, password):
        numbers='0123456789'
        if (len(password)<5) or (sum([1 for i in password if i in numbers])<1):
            raise ValueError('Пароль должен быть больше 5 символов и содержать цифры')
        return password

    class Config:
        from_attributes=True


class Progress(Base):
    __tablename__='Progress'
    id=Column(Integer, primary_key=True)
    nomer_lesson=Column(Integer)
    users_id=Column(Integer, ForeignKey('Users.id'))
    users=relationship('Users',back_populates='progress')

class Progress_validation(BaseModel):
    id:int
    nomer_lesson:int
    users_id:int

    class Config:
        from_attributes=True

class Teoriay(Base):
    __tablename__='Teoriay'
    id=Column(Integer, primary_key=True)
    text=Column(String)
    practika=relationship('Practika', back_populates='teoriay')

class Teoriay_validation(BaseModel):
    id:int
    text:str

    class Config:
        from_attributes=True


class Practika(Base):
    __tablename__='Practika'
    id=Column(Integer, primary_key=True)
    text=Column(String)
    input_data=Column(Integer)
    output_data=Column(Integer)
    teoriay_id=Column(Integer, ForeignKey('Teoriay.id'))
    teoriay=relationship('Teoriay', back_populates='practika')

class Practika_validation(BaseModel):
    id:int
    text:str
    input_data:int
    output_data:int
    teoriay_id:int

    class Config:
        from_attributes=True


