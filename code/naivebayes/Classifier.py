import json
from decimal import Decimal as dec

#Imports vocabulary with stored probabilities for our classifier
vocabulary = json.load(open("../../both_words_sorted_fix.bayes"))

#Splits reviews up into an array of processable words
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
            #Add P(w | y={0,1})
            prob_positive = dec(prob_positive * vocabulary[word]["posprob"])
            prob_negative = dec(prob_negative * vocabulary[word]["negprob"])
        else:
            #Laplace smoothing when word unknown
            prob_positive = dec(prob_positive * (1/(vocabulary["total_words"]["unique"] + vocabulary["pos:class"]["count"])))
            prob_negative = dec(prob_negative * (1/(vocabulary["total_words"]["unique"] + vocabulary["neg:class"]["count"])))
    if prob_positive > prob_negative:
        return "positive"
    else:
        return "negative"

make_prediction(document)

#   posProb *= list[classPosProb]
#   negProb *= list[classNegProb]
