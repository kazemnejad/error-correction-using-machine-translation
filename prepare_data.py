import random
import xml.etree.ElementTree as ET
from xml.dom import minidom

import nltk
import os


def read_from_ns_child(ns, lookfor):
    text = ''

    for c in ns.childNodes:
        if c.nodeName == '#text':
            text += c.nodeValue
        elif c.nodeName == lookfor:
            text += read_from_ns_child(c, lookfor)
        elif c.nodeName == 'NS':
            text += read_from_ns_child(c, lookfor)
            # result = c.getElementsByTagName(lookfor)
            # if len(result) > 0:
            #     node = result[0]
            #     text += read_from_ns_child(node, lookfor)
            #     r_correct, r_incorrect = read_from_ns_child(incorrect[0])
            #     p_text_correct += r_correct
            #     p_text_incorrect += r_incorrect
            # else:
            #     p_text_incorrect += incorrect[0].firstChild.nodeValue

    return text


def read_doc(file_path):
    doc = minidom.parse(file_path)
    ps = doc.getElementsByTagName('p')

    result = []
    for p in ps:
        p_text_correct = ''
        p_text_incorrect = ''

        for c in p.childNodes:
            if c.nodeName == '#text':
                p_text_correct += c.nodeValue
                p_text_incorrect += c.nodeValue
            elif c.nodeName == 'NS':
                p_text_correct += read_from_ns_child(c, 'c')
                p_text_incorrect += read_from_ns_child(c, 'i')
                # for an in c.childNodes:
                #     if an.nodeName == 'c':
                #         p_text_correct += read_from_ns_child(an, 'c')

                # for an in c.childNodes:
                #     if an.nodeName == 'i':
                #         p_text_incorrect += read_from_ns_child(an, 'i')

        result.append((
            " ".join(nltk.word_tokenize(p_text_correct)),
            " ".join(nltk.word_tokenize(p_text_incorrect))
        ))

    return result


def read_all_docs(base):
    dataset = []
    for sub_path in os.listdir(base):
        for doc_file in os.listdir(os.path.join(base, sub_path)):
            dataset.extend(read_doc(os.path.join(base, sub_path, doc_file)))

    return dataset


def create_dataset(raw_data):
    for _ in range(10):
        random.shuffle(raw_data)

    cut_point = int(len(raw_data) * 0.9)

    train = raw_data[:cut_point]
    val = raw_data[cut_point:]

    return train, val


def save_dataset(ds, name):
    with open('cor-' + name, 'w', encoding='utf8') as src:
        with open('incor-' + name, 'w', encoding='utf8') as dst:
            for c, i in ds:
                src.write(c)
                src.write('\n')

                dst.write(i)
                dst.write('\n')


train, val = create_dataset(read_all_docs('fce-released-dataset/dataset'))
# train, val = read_doc('fce-released-dataset/dataset/0100_2000_12/doc1018.xml')

save_dataset(train, 'train.txt')
save_dataset(val, 'val.txt')
