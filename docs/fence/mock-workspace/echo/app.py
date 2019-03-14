"""A mock API."""
from flask import Flask
from flask import jsonify
from flask import request
import requests

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    """A simple way to create a Catch-All function which serves every URL including / is to chain two route filters. One for the root path '/' and one including a path placeholder for the rest.
       We can't just use one route filter including a path placeholder because each placeholder must at least catch one character."""

    # call fence and get information on the user
    fence_user = requests.get('http://fence-service/user', cookies=request.cookies)

    # just dump out all the data
    return jsonify(
        {'path': path,
         'headers': dict(**request.headers),
         'cookies': dict(**request.cookies),
         'fence': fence_user.json()
         })

if __name__ == '__main__':
    app.run(debug=True)
