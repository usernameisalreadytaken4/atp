from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from restful.tables import TableAPI


app = Flask(__name__)
api = Api(app)

app.config.from_object('config')
db = SQLAlchemy(app)

api.add_resource(TableAPI, '/tables', endpoint='tables')

if __name__ == '__main__':
    app.run(debug=True)