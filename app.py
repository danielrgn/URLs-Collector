from flask import Flask, request, jsonify
from models.url import Url

import settings.database as db
import atexit
import os

app = Flask(__name__, static_url_path='')

port = int(os.getenv('PORT', 8000))


@app.route('/')
def root():
    return app.send_static_file('index.html')


# /**
#  * Endpoint to get a array of all the urls from _id param in the database
#  * REST API example:
#  * <code>
#  * GET http://localhost:8000/api/urls/1
#  * </code>
#  *
#  * Response:
#  * [
#       [http://www.site.com.br/, http://www.site.com.br/],
#       [http://www.site.com.br/, http://www.site.com.br/]
#    ]
#  * @return An array of all the urls from _id param
#  */
@app.route('/api/urls/<id>', methods=['GET'])
def get_url(id=None):
    url_dict = []
    doc = db.get_document(id)
        
    if doc is None:
        return jsonify(False)

    for url in doc['url_list']:
        data = _url_collector(url)

        if data is not None:
            url_dict.append(data['url_list'])

    return jsonify(url_dict)


# /* Endpoint to greet and add a new url to database.
# * Send a POST request to localhost:8000/api/urls with body
# * {
# *     "url": "http://www.site.com.br/"
# * }
# */
@app.route('/api/urls', methods=['POST'])
def put_url():
    params = request.get_json()
    url = params.get('url')

    if url is None:
        return jsonify([])
    
    data = _url_collector(url)

    if data is None:
        return jsonify("Error collecting URLs: {}".format(url))
    
    return jsonify(data)


# /* Method to get URL's from the entry URL's html. # */
def _url_collector(entry_url):
    url = Url(entry_url)
    url_list = url.get_urls_from_entry_url()
    
    if url_list is None:
        return None

    data = {'entry_url': url.url, 'url_list':url_list}
    data = db.create_document(data)

    return data


@atexit.register
def shutdown():
    db.close_connection()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
