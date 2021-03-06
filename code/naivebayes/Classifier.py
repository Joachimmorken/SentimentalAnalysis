import json
from decimal import Decimal as dec
import os
import math


#Imports vocabulary with stored probabilities for our classifier
vocabulary = json.load(open("../../both_words_sorted_log.bayes"))

total_documents = vocabulary["pos:class"]["total_files"] + vocabulary["neg:class"]["total_files"]
prob_negative = dec(vocabulary["neg:class"]["total_files"] / total_documents)
prob_positive = dec(vocabulary["pos:class"]["total_files"] / total_documents)

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


stopwords = [
    "a"
    "about",
    "above",
    "after",
    "again",
    "against",
    "all",
    "am",
    "an",
    "and",
    "any",
    "are",
    "aren't",
    "as",
    "at",
    "be",
    "because",
    "been",
    "before",
    "being",
    "below",
    "between",
    "both",
    "but",
    "by",
    "can't",
    "cannot",
    "could",
    "couldn't",
    "did",
    "didn't",
    "do",
    "does",
    "doesn't",
    "doing",
    "don't",
    "down",
    "during",
    "each",
    "few",
    "for",
    "from",
    "further",
    "had",
    "hadn't",
    "has",
    "hasn't",
    "have",
    "haven't",
    "having",
    "he",
    "he'd",
    "he'll",
    "he's",
    "her",
    "here",
    "here's",
    "hers",
    "herself",
    "him",
    "himself",
    "his",
    "how",
    "how's",
    "i",
    "i'd",
    "i'll",
    "i'm",
    "i've",
    "if",
    "in",
    "into",
    "is",
    "isn't",
    "it",
    "it's",
    "its",
    "itself",
    "let's",
    "me",
    "more",
    "most",
    "mustn't",
    "my",
    "myself",
    "no",
    "nor",
    "not",
    "of",
    "off",
    "on",
    "once",
    "only",
    "or",
    "other",
    "ought",
    "our",
    "ours"
    "ourselves",
    "out",
    "over",
    "own",
    "same",
    "shan't",
    "she",
    "she'd",
    "she'll",
    "she's",
    "should",
    "shouldn't",
    "so",
    "some",
    "such",
    "than",
    "that",
    "that's",
    "the",
    "their",
    "theirs",
    "them",
    "themselves",
    "then",
    "there",
    "there's",
    "these",
    "they",
    "they'd",
    "they'll",
    "they're",
    "they've",
    "this",
    "those",
    "through",
    "to",
    "too",
    "under",
    "until",
    "up",
    "very",
    "was",
    "wasn't",
    "we",
    "we'd",
    "we'll",
    "we're",
    "we've",
    "were",
    "weren't",
    "what",
    "what's",
    "when",
    "when's",
    "where",
    "where's",
    "which",
    "while",
    "who",
    "who's",
    "whom",
    "why",
    "why's",
    "with",
    "won't",
    "would",
    "wouldn't",
    "you",
    "you'd",
    "you'll",
    "you're",
    "you've",
    "your",
    "yours",
    "yourself",
    "yourselves"]

def classifier(document, prob_negative, prob_positive, vocabulary):
    document = divide_and_conquer(document)
    for word in document:
        if word in vocabulary:
            if word not in stopwords:
                prob_positive *= prob_positive + dec(vocabulary[word]["posprob"])
                prob_negative *= prob_negative + dec(vocabulary[word]["negprob"])
        #else:
            #Laplace smoothing when word unknown
            #"prob_positive = dec(prob_positive * (1/(vocabulary["total_words"]["unique"] + vocabulary["pos:class"]["count"])))
            #prob_negative = dec(prob_negative * (1/(vocabulary["total_words"]["unique"] + vocabulary["neg:class"]["count"])))

    if prob_positive > prob_negative:
        return "positive"
    else:
        return "negative"



def accuracy ():
    accuracy = 0
    path = "../../../Data/test/pos"
    for filename in os.listdir(path):
        f = path + "/" + filename
        with open(f, "r", encoding="utf8", errors="ignore") as doc:
            accuracy += 0.008 if (classifier(doc.read(), prob_positive, prob_negative, vocabulary) == "positive") else 0
    print(accuracy)



document = ""
def make_prediction(document):
    print(classifier(document, prob_negative, prob_positive, vocabulary))

make_prediction(document)