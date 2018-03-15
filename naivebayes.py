import os
import json
import simplejson
from collections import OrderedDict
import math
from decimal import Decimal as Dec
import pandas as pd

exclude = [".", ",", "!", "?", "_", "-", "<br>", "<br/>", "\\", "/", "(", ")", "<br", "br>", "<p>", "<>", "<", ">"]
base = "E:/Markus/Skule/UiB/V18/INFO284/Oblig/7zip/train"
pos = base + "/pos"
neg = base + "/neg"
both = "E:/Markus/Skule/UiB/V18/INFO284/Oblig/284 gruppeprosjekt/both_words_sorted.bayes"


def list_words(path):
    words = {}
    unique = 0
    count = 0
    class_name = path[-3:]

    for filename in os.listdir(path):
        f = path + "/" + filename
        with open(f, encoding="utf8") as file:
            for w in file.read().split():
                w = class_name + ":" + w
                for e in exclude:
                    w = w.replace(e, " ")
                if w.lower() in words:
                    words[w.lower()]["count"] += 1
                if w.lower() not in words:
                    words[w.lower()] = {"count": 1, "class": class_name}
                    unique += 1
                count += 1
            words["total_words_count"] = {"unique": unique, "count": count}

    new_file = class_name + "_words.bayes"
    with open(new_file, "w", encoding="utf8") as jsonFile:
        json.dump(words, jsonFile)


def sort_words(path):
    f = path[-3:]
    new_file = f + "_words.bayes"
    with open(new_file, "r", encoding="utf8") as file:
        data = json.load(file)
    ordered = OrderedDict(sorted(data.items(), key=lambda i: i[1]['count'], reverse=True))

    sorted_file = f + "_words_sorted.bayes"
    with open(sorted_file, "w", encoding="utf8") as file:
        json.dump(ordered, file)


def list_and_sort(path):
    list_words(path)
    sort_words(path)


def gen_prob(file):
    with open(file, "r", encoding="utf8") as data_file:
        loaded_dictionaries = json.loads(data_file.read())

    all_prob = []

    total_probability = Dec(1)
    for w in loaded_dictionaries:
        if w == "pos" or w == "neg":
            total = loaded_dictionaries["total_words_count"]["count"]
            unique = loaded_dictionaries["total_words_count"]["unique"]
            prob = Dec((loaded_dictionaries[w]["count"] + 1) / (total + unique))
            loaded_dictionaries[w]["prob"] = prob
        elif "class" in loaded_dictionaries[w]:
            class_name = loaded_dictionaries[w]["class"]
            total = (loaded_dictionaries[class_name]["count"])
            unique = (loaded_dictionaries[class_name]["unique"])
            prob = Dec((loaded_dictionaries[w]["count"] + 1) / (total+unique))
            loaded_dictionaries[w]["prob"] = prob
            total_probability *= Dec(prob)

        if total_probability == float(0):
            print("{} : {}".format(w, loaded_dictionaries[w]))
            break
        all_prob.append(total_probability)

    loaded_dictionaries["total_words_count"]["prob"] = total_probability

    with open("all_prob.bayes", "w", encoding="utf8") as file_test:
        file_test.write(str(all_prob))

    with open(file, "w", encoding="utf8") as data_file:
        simplejson.dump(loaded_dictionaries, data_file)


def merge_lists(paths):
    words = {}
    unique = 0
    count = 0

    for path in paths:
        class_name = path[-3:]
        class_count = 0
        class_unique = 0

        for filename in os.listdir(path):
            f = path + "/" + filename
            with open(f, encoding="utf8") as file:
                for w in file.read().split():
                    w = class_name + ":" + w
                    for e in exclude:
                        w = w.replace(e, " ")
                    if w.lower() in words:
                        words[w.lower()]["count"] += 1
                    if w.lower() not in words:
                        words[w.lower()] = {"count": 1, "class": class_name}
                        unique += 1
                        class_unique += 1
                    count += 1
                    class_count += 1
                words["total_words_count"] = {"unique": unique, "count": count}
        words[class_name] = {"unique": class_unique, "count": class_count, "prob": 0}

    with open("both_words.bayes", "w", encoding="utf8") as jsonFile:
        json.dump(words, jsonFile)

    with open("both_words.bayes", "r", encoding="utf8") as file:
        data = json.load(file)
    ordered = OrderedDict(sorted(data.items(), key=lambda i: i[1]['count'], reverse=True))

    with open("both_words_sorted.bayes", "w", encoding="utf8") as file:
        json.dump(ordered, file)


posneg = [pos, neg]
# merge_lists(posneg)

# merge_lists(posneg)
# gen_prob(both)

list_and_sort(pos)
list_and_sort(neg)
gen_prob("pos_words_sorted.bayes")
gen_prob("neg_words_sorted.bayes")

# gen_prob("both_words_sorted.bayes")

# list_and_sort(pos)

# gen_prob("neg_words_sorted.bayes")
# gen_prob("pos_words_sorted.bayes")


# loaded_dictionaries[w]["prob"] =((w["count"] + 1) / (loaded_dictionaries["total_words_count"]["count"] +
#                                                              loaded_dictionaries["total_words_count"]["unique"]))
