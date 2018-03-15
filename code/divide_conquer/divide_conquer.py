def divide_and_conquer(doc):
    exclude = [".", ",", "!", "?", "_", "=", "-", "<br>", "<br/>", "\\", "/", "(", ")", "<br", "br>", "<p>", "<>", "<", ">"]
    new = []

    for w in doc.split():
        for e in exclude:
            w = w.replace(e, "")
        if w is not "":
            new.append(w)

    return new
