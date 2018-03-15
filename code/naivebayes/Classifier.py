import json




positive_documents = 12500
negative_documents = 12500
total_documents = negative_documents + positive_documents
posSem = 1
negSem = 1

probability = json.load(open("../SentimentalAnalysis/both_words.json"))
vocabulary = json.load(open("../SentimentalAnalysis/both_words.json"))



classes = [0, 1]  # 0, negative, 1, positive

def divide_and_conquer(doc):
    exclude = [".", ",", "!", "?", "_", "=", "-", "<br>", "<br/>", "\\", "/", "(", ")", "<br", "br>", "<p>", "<>", "<", ">"]
    new = []

    for w in doc.split():
        for e in exclude:
            w = w.replace(e, "")
        if w is not "":
            new.append(w)

    return new



"""""""""
Eksempel data

class probability
posProb = 0.8
negProb = 0.2

document = "I fucking loved this movie, it was great"


"""""""""


def classifier (document, prior, likelihood):
    posProb = 1
    negProb = 1
    document = divide_and_conquer(document)

        #   sum = 0.5  # prior[c]
        for word in document:
            if word in vocabulary:
                posProb *= probability["word"]["posProb"]
                negProb *= probability["word"]["negProb"]
        posProb *= 0.5
        negProb *= 0.5

        if posProb > negProb:
            return 1
        else:
            return 0


    #   posProb *= list[classPosProb]
    #   negProb *= list[classNegProb]







