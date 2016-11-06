from flask import request, url_for
from flask.ext.api import FlaskAPI, status, exceptions
import main as p1

app = FlaskAPI(__name__)


@app.route("/treat/<string:text>", methods=['GET'])
def treat(text):
    if(request.method == 'GET'):
        return p1.getLembreteInfo(text)
        
if __name__ == "__main__":
    app.run(debug=False)
