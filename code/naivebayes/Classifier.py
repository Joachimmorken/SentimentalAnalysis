import json
import math

vocabulary = json.load(open("../../both_words_sorted_fix.bayes"))


def divide_and_conquer(doc):
    exclude = [".", ",", "!", "?", "_", "=", "-", "<br>", "<br/>", "\\", "/", "(", ")", "<br", "br>", "<p>", "<>", "<",
               ">"]
    new = []

    for w in doc.split():
        for e in exclude:
            w = w.replace(e, "")
        if w is not "":
            new.append(w)
    return new


document = "i truly loved this movie it was great"

# Class probabilities (prior(c))


def make_prediction(document):
    prob_positive = 0.5
    prob_negative = 0.5
    sum = 1
    document = divide_and_conquer(document)
    for word in document:
        if word in vocabulary:
            prob_positive *= (vocabulary["word"]["posprob"])
            prob_negative *= (vocabulary["word"]["negprob"])
        if word not in vocabulary:
            continue
    if prob_positive > prob_negative:
        print("Positive")
    else:
        print("Negative")

make_prediction(document)

#   posProb *= list[classPosProb]
#   negProb *= list[classNegProb]
