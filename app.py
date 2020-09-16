from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

engine = create_engine('postgresql://localhost:5432/Practice')
Session = sessionmaker(bind=engine)
session = Session()
app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

import routes
