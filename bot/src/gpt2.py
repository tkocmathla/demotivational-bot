import gpt_2_simple as gpt2s

from util import similar


def generate(prefix, input_file, similarity_threshold, nsamples, length, temperature, k):
    # load the quotes used for fine-tuning
    with open(input_file, 'r') as f:
        originals = f.readlines()
        original_quotes = [originals[i].strip() for i in range(1, len(originals), 3)]

    # generate a batch of quotes
    sess = gpt2s.start_tf_sess()
    gpt2s.load_gpt2(sess)
    samples = gpt2s.generate(sess,
                             nsamples=nsamples,
                             length=length,
                             temperature=temperature,
                             top_k=k,
                             prefix=prefix + '\n',
                             return_as_list=True)

    # filter the samples
    quotes = []
    for s in samples:
        title, body = s.split('\n')[:2]
        is_long = len(body.split(' ')) > 3
        is_novel = all(similar(body, x) < similarity_threshold for x in original_quotes)

        if is_long and is_novel:
            quotes.append(body)

    return quotes
