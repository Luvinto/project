from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session
from pydantic import BaseModel, field_validator, ConfigDict
from sqlalchemy.types import Enum as SQLEnum
from typing import Literal
from pydantic import EmailStr


Base=declarative_base()
engine=create_engine('postgresql://postgres:Dfhzu123@localhost:5432/my_bd')
Sessions=sessionmaker(bind=engine)
sessions=Sessions()

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

    model_config = ConfigDict()


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

    model_config = ConfigDict()

class Teoriay(Base):
    __tablename__='Teoriay'
    id=Column(Integer, primary_key=True)
    text=Column(String)
    practika=relationship('Practika', back_populates='teoriay')

class Teoriay_validation(BaseModel):
    id:int
    text:str

    model_config = ConfigDict()

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

    model_config = ConfigDict()


Base.metadata.create_all(bind=engine)

# Проверка
def validations(objects_users,object_dict,class_validation,sessions_func):
    try:
        user_validation=class_validation(**object_dict)
        print(f'Объект: {objects_users} прошел проверку')
        sessions_func.add(objects_users)
        print('Объект готов к подгрузке')
        sessions_func.commit()
        return True

    except Exception as e:
        sessions_func.rollback()
        return False

    finally:
        sessions_func.close()


oleg=Users(login='lox',password='lox123',email='lox123@mail.ru',age=12,groups='Ученик')
oleg_dict={
    "id": 0,
    "login": oleg.login,
    "password": oleg.password,
    "email": oleg.email,
    "age": oleg.age,
    "groups": oleg.groups,
}


olegprogress1=Progress(nomer_lesson=1, users_id=1)
olegprogress1_dict={
    'id':0,
    "nomer_lesson":1,
    'users_id':1
}
