def scramble_sentence(sentence: str) -> str:
    """
    Return the given sentence with each word scrambled, preserving ending punctuation and numbers.

    This function does not treat internal punctuation specially,
    and will replace non-space whitespace as space
    """
    if not sentence[len(sentence) - 1].isalnum():
        end_punct = sentence[len(sentence) - 1]
        sentence = sentence[:-1]
    else:
        end_punct = ""

    # this does not preserve indents!
    scrambled = [scramble_word(s) if not s.isnumeric() else s for s in sentence.split()]

    if end_punct:
        scrambled[len(scrambled) - 1] += end_punct

    return " ".join(scrambled)


def scramble_word(word: str) -> str:
    """
    Scramble internal letters of a given string, ie

    tomato -> totmao
    or
    1984 -> 1894
    """
    if len(word) <= 2:
        return word
    internal = word[1:-1]
    return word[0] + scramble_str(internal) + word[len(word) - 1]


def scramble_str(s: str) -> str:
    """Scrambles `s` except for the first and last letter."""
    from random import shuffle

    L = list(s)
    shuffle(L)
    return "".join(L)
