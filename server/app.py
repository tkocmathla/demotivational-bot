from flask import Flask, jsonify, request
from flask_cors import CORS

import generator


app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})


@app.before_first_request
def init():
    # load the quotes used for fine-tuning
    with open('static/demotivational_posters.txt', 'r') as f:
        originals = f.readlines()
        originals = [originals[i].strip() for i in range(1, len(originals), 3)]
        app.config['originals'] = originals


@app.route('/generate', methods=['GET'])
def generate():
    quotes = generator.generate(request.args['prefix'],
                                app.config['originals'],
                                float(request.args['similarity_threshold']),
                                int(request.args['nsamples']),
                                int(request.args['length']),
                                float(request.args['temperature']),
                                int(request.args['top_k']))
    return jsonify(quotes)


if __name__ == '__main__':
    app.run(debug=True)
