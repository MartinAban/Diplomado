from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Password, Config

engine = create_engine("sqlite:///password_manager.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()

def init_db():
    Base.metadata.create_all(engine)

def is_first_run():
    return session.query(Config).first() is None

def set_master_password_hash(hashed):
    config = Config(master_password_hash=hashed)
    session.add(config)
    session.commit()

def get_master_password_hash():
    config = session.query(Config).first()
    return config.master_password_hash if config else None

def update_master_password_hash(new_hashed):
    config = session.query(Config).first()
    if config:
        config.master_password_hash = new_hashed
        session.commit()

def add_password(title, username, encrypted_password):
    pw = Password(title=title, username=username, encrypted_password=encrypted_password)
    session.add(pw)
    session.commit()

def get_passwords():
    return session.query(Password).all()

def search_passwords_by_title(search):
    return session.query(Password).filter(Password.title.ilike(f"%{search}%")).all()

def delete_password(password_id):
    pw = session.query(Password).filter_by(id=password_id).first()
    if pw:
        session.delete(pw)
        session.commit()