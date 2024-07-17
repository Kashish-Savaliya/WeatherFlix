from datetime import datetime
from project import db, login_manager
from flask_login import UserMixin
from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# engine = create_engine('sqlite:///C:\\Users\\abc\\Desktop\\WeatherFlix\\myenv\\WFlix/site.db')
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# # db = SessionLocal()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# def add_column(engine, table_name, column):
#     column_name = column.compile(dialect=engine.dialect)
#     column_type = column.type.compile(engine.dialect)
#     engine.execute('ALTER TABLE %s ADD COLUMN %s %s ' %(table_name, column_name, column_type))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    # column = db.Column('city',db.String(100),nullable=False)
    # add_column(engine,User,column)
    # image_file = db.Column(db.String(20), nullable=False ,default='default.jpeg')
    password = db.Column(db.String(60), nullable=False)
    # posts = db.relationship('Post', backref='author', lazy=True)
    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.city}','{self.password}')"

# result = db.execute('SELECT * FROM user')

# result = engine.execute('SELECT * FROM user')
# column = db.Column('city',db.String(100),nullable=False)
# add_column(engine,User,column)