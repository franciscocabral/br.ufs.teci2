'''
pip install Flask-API
pip install -U flask-cors
'''
from flask.ext.api import FlaskAPI
from flask import request
from flask.ext.cors import CORS, cross_origin
import main as p1


app = FlaskAPI(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/treat/<string:text>", methods=['GET'])
@cross_origin()
def treat(text):
    if(request.method == 'GET'):
        return p1.getLembreteInfo(text)
        
if __name__ == "__main__":
    app.run(debug=False)
