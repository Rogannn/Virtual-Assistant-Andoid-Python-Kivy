def word_splitter(words):
    word_limit = 6
    split_words = words.split()
    new_text = ""
    word_count = 0
    for word in split_words:
        new_text += word + " "
        word_count += 1
        if word_count > word_limit or "|" in word:
            new_text += "\n"
            word_count = 0
    return new_text.replace("|", "")
