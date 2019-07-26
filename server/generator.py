import gpt_2_simple as gpt2s

from util import similar


# TODO generate & filter until nsamples reached
def generate(prefix, originals, similarity_threshold, nsamples, length, temperature, top_k):
    # generate a batch of quotes
    sess = gpt2s.start_tf_sess()
    gpt2s.load_gpt2(sess)
    samples = gpt2s.generate(sess,
                             nsamples=nsamples,
                             length=length,
                             temperature=temperature,
                             top_k=top_k,
                             prefix=prefix + '\n',
                             return_as_list=True)

    # filter the samples
    quotes = []
    for s in samples:
        title, body = s.split('\n')[:2]
        is_long = len(body.split(' ')) > 3
        is_novel = all(similar(body, x) < similarity_threshold for x in originals)

        if is_long and is_novel:
            quotes.append(body)

    return quotes
