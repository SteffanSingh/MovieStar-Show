
from sqlalchemy import  create_engine
from sqlalchemy.orm import declarative_base, sessionmaker,joinedload




Base = declarative_base()

engine = create_engine(f'sqlite:///moviewebapp.sqlite')
Base.metadata.create_all(engine)

# Create a database session
Session = sessionmaker(bind=engine)
session = Session()