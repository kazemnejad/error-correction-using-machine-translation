import nltk


def read_dataset(ref_path, hyph_path):
    ref = []
    with open(ref_path, 'r', encoding='utf8') as f:
        for l in f:
            l = l[:-1]
            ref.append(nltk.word_tokenize(l))

    hyph = []
    with open(hyph_path, 'r', encoding='utf8') as f:
        for l in f:
            l = l[:-1]
            hyph.append(nltk.word_tokenize(l))

    return zip(ref, hyph)


def calculate_bleu(dataset):
    bleus = []
    for r, h in dataset:
        bleus.append(nltk.translate.bleu([r], h))

    return sum(bleus) * 1.0 / len(bleus)


if __name__ == '__main__':
    d = read_dataset('cor-val.txt', 'pred_30k.txt')
    print(calculate_bleu(list(d)))
