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


@app.route("/treat", methods=['GET'])
@cross_origin()
def treat():
    if(request.method == 'GET'):
        text = request.args['text']
        return p1.getLembreteInfo(text)
        
if __name__ == "__main__":
    app.run(debug=False)
