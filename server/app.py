from difflib import SequenceMatcher

from flask import Flask, jsonify, request
from flask_cors import CORS
import gpt_2_simple as gpt2s


app = Flask(__name__)
app.config.from_object(__name__)

# TODO lock this down
CORS(app, resources={r'/*': {'origins': '*'}})


# https://stackoverflow.com/a/17388505
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


# TODO generate & filter until nsamples reached
def generate_samples(prefix, originals, similarity_threshold, nsamples, length, temperature, top_k):
    # generate a batch of quotes
    samples = gpt2s.generate(app.config['gpt2_sess'],
                             nsamples=nsamples,
                             length=length,
                             temperature=temperature,
                             top_k=top_k,
                             prefix=prefix + '\n',
                             return_as_list=True)

    # filter the samples
    quotes = []
    for s in samples:
        _, body = s.split('\n')[:2]
        body = body.split('.')[0]
        is_long = len(body.split(' ')) > 3
        is_novel = all(similar(body, x) < similarity_threshold for x in originals)

        if is_long and is_novel:
            quotes.append(body)

    return quotes


@app.before_first_request
def init():
    # load the quotes used for fine-tuning
    with open('static/demotivational_posters.txt', 'r') as f:
        originals = f.readlines()
        originals = [originals[i].strip() for i in range(1, len(originals), 3)]
        app.config['originals'] = originals

    # initialize gpt-2
    app.config['gpt2_sess'] = gpt2s.start_tf_sess()
    gpt2s.load_gpt2(app.config['gpt2_sess'])


@app.route('/generate', methods=['GET'])
def generate():
    quotes = generate_samples(request.args['prefix'],
                              app.config['originals'],
                              float(request.args['similarity_threshold']),
                              int(request.args['nsamples']),
                              int(request.args['length']),
                              float(request.args['temperature']),
                              int(request.args['top_k']))
    return jsonify(quotes)


if __name__ == '__main__':
    app.run(debug=True)
