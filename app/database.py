
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker

from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base: DeclarativeMeta = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()








#this row connects my code with my database, however this is made by psycopg2 postgres driver, and my database connection has been 
#also made with sqlalchemy in the code above, so this block of code is entirely redundant, that being said, im gonna leave it for educational 
#purposes
#While True:
#  try:
#        conn = psycopg2.connect(host = 'localhost', database='fastapi', user='postgres', password='patryk1998', cursor_factory=RealDictCursor)#this  line
 #       #is responsible for setting a connection between database and my code
 #       cursor = conn.cursor() #variable needed to execute SQL statements
 #       print("Database connection was succesful!!")
 #       break
 #   except Exception as error:
 #       print("Connecting to database failed")
  #      print("Error: ", error)
  #      time.sleep(3)