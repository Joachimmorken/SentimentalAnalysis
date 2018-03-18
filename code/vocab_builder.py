import os
import json
import simplejson
from collections import OrderedDict
import math
from decimal import Decimal as Dec
import pandas as pd

exclude = [".", ",", "!", "?", "_", "-", "<br>", "<br/>", "\\", "/", "(", ")", "<br", "br>", "<p>", "<>", "<", ">",
           "\"", " "]
base = "E:/Markus/Skule/UiB/V18/INFO284/Oblig/7zip/train"
pos = base + "/pos"
neg = base + "/neg"
both = "E:/Markus/Skule/UiB/V18/INFO284/Oblig/284 gruppeprosjekt/both_words_sorted.bayes"


def merge_lists(paths):
    words = {}
    unique = 0
    count = 0

    for path in paths:
        class_name = path[-3:]
        class_count = 0
        class_unique = 0
        class_files = 0

        for filename in os.listdir(path):
            class_files += 1
            f = path + "/" + filename
            with open(f, encoding="utf8") as file:
                for w in file.read().split():
                    for e in exclude:
                        w = w.replace(e, "")
                    w = w.lower()
                    if w in words:
                        if class_name == "pos":
                            words[w]["poscount"] += 1
                            words[w]["totalcount"] += 1
                        if class_name == "neg":
                            words[w]["negcount"] += 1
                            words[w]["totalcount"] += 1
                    if w not in words:
                        words[w] = {"poscount": 0, "negcount": 0, "posprob": 0, "negprob": 0, "totalcount": 1}
                        if class_name is "pos":
                            words[w]["poscount"] += 1
                        if class_name is "neg":
                            words[w]["negcount"] += 1
                        unique += 1
                        class_unique += 1
                    count += 1
                    class_count += 1
                words["total_words_count"] = {"unique": unique, "count": count, "totalcount": count}
        words[class_name + ":class"] = {"unique": class_unique, "count": class_count, "prob": 0, "totalcount": class_count}
        total_class_files = class_name + "_total_words"
    words[class_name + "_meta"] = {total_class_files: class_files, "totalcount": class_files}

    with open("both_words.bayes", "w", encoding="utf8") as jsonFile:
        json.dump(words, jsonFile)

    with open("both_words.bayes", "r", encoding="utf8") as file:
        data = json.load(file)
    ordered = OrderedDict(sorted(data.items(), key=lambda word: word[1]['totalcount'], reverse=True))

    with open("both_words_sorted.bayes", "w", encoding="utf8") as file:
        json.dump(ordered, file)

    with open("both_words_sorted.bayes", "r", encoding="utf8") as data_file:
        loaded_dictionaries = json.loads(data_file.read())

    total_pos_prob = Dec(1)
    total_neg_prob = Dec(1)
    for w in loaded_dictionaries:
        pos_unique = loaded_dictionaries["pos:class"]["unique"]
        neg_unique = loaded_dictionaries["neg:class"]["unique"]

        if w == "pos:class" or w == "neg:class":
            total = loaded_dictionaries["total_words_count"]["count"]
            prob = Dec((loaded_dictionaries[w]["count"] + 1) / (total))
            loaded_dictionaries[w]["prob"] = prob

        if "poscount" in loaded_dictionaries[w]:
            pos_count = loaded_dictionaries["pos:class"]["count"]
            word_neg_count = loaded_dictionaries[w]["negcount"]
            word_pos_count = loaded_dictionaries[w]["poscount"]
            if loaded_dictionaries[w]["poscount"] > 0:
                pos_prob = Dec((loaded_dictionaries[w]["poscount"] + 1) / (pos_count + (pos_unique + neg_unique)))
                loaded_dictionaries[w]["posprob"] = pos_prob
                total_pos_prob *= pos_prob

        if "negcount" in loaded_dictionaries[w]:
            neg_count = loaded_dictionaries["neg:class"]["count"]
            word_neg_count = loaded_dictionaries[w]["negcount"]
            word_pos_count = loaded_dictionaries[w]["poscount"]
            if loaded_dictionaries[w]["negcount"] > 0:
                neg_prob = Dec((loaded_dictionaries[w]["negcount"] + 1) / (neg_count + (pos_unique + neg_unique)))
                loaded_dictionaries[w]["negprob"] = neg_prob
                total_neg_prob *= neg_prob

        if total_pos_prob == float(0) or total_neg_prob == float(0):
            print("{} : {}".format(w, loaded_dictionaries[w]))
            break

    loaded_dictionaries["pos:class"]["prob"] = total_pos_prob
    loaded_dictionaries["neg:class"]["prob"] = total_neg_prob

    with open("both_words_sorted.bayes", "w", encoding="utf8") as data_file:
        simplejson.dump(loaded_dictionaries, data_file)


def check_prob():
    with open("both_words_sorted.bayes", "r", encoding="utf8") as file:
        data = json.load(file)

    total_pos_prob = 0
    total_neg_prob = 0
    for d in data:
        if ":class" not in d and "total_words" not in d and "_meta" not in d:
            total_pos_prob += data[d]["posprob"]
            total_neg_prob += data[d]["negprob"]

    print("Total positive: {}\nTotal negative: {}".format(total_pos_prob, total_neg_prob))


posneg = [pos, neg]

merge_lists(posneg)

check_prob()
