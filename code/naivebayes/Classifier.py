import json
from decimal import Decimal as dec
import os

#Imports vocabulary with stored probabilities for our classifier
# vocabulary = json.load(open("../../both_words.bayes"))

with open("../../both_words_sorted.bayes", "r", encoding="utf8") as file:
    vocabulary = json.load(file)

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


# Class probabilities (prior(c))


def make_prediction(document):
    prob_positive = dec(0.5)
    prob_negative = dec(0.5)
    sum = 1
    document = divide_and_conquer(document)
    for word in document:
        if word in vocabulary:
            #Add P(w | y={0,1})
            prob_positive = dec(prob_positive * dec(vocabulary[word]["posprob"]))
            prob_negative = dec(prob_negative * dec(vocabulary[word]["negprob"]))
        #else:
            #Laplace smoothing when word unknown
            #"prob_positive = dec(prob_positive * (1/(vocabulary["total_words"]["unique"] + vocabulary["pos:class"]["count"])))
            #prob_negative = dec(prob_negative * (1/(vocabulary["total_words"]["unique"] + vocabulary["neg:class"]["count"])))

    if prob_positive > prob_negative:
        return "positive"
    else:
        return "negative"


poscount = 0
path = "E:/Markus/Skule/UiB/V18/INFO284/Oblig/7zip/train/neg"
for filename in os.listdir(path):
    f = path + "/" + filename
    with open(f, "r", encoding="utf8") as doc:
        poscount += 1 if (make_prediction(doc.read()) == "negative") else 0

print(poscount)


#   posProb *= list[classPosProb]
#   negProb *= list[classNegProb]
