from sqlalchemy import create_engine

db_user = 'dwail'
db_password = 'qchef-dwail'
db_host = 'localhost'  # or your database host
db_port = 3306  # or your database port
db_name = 'qchef'


def connecty_stuff():
    return create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')