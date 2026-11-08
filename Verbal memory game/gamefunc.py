# Game functions
import random

# DATA: Create dictionary data (for words)
# Indices much match respective translation
en_file = open("engd.txt", "r", encoding="utf-8")
fr_file = open("frd.txt", "r", encoding="utf-8")
es_file = open("espd.txt", "r", encoding="utf-8")

en_d = []
fr_d = []
es_d = []

for line in en_file.readlines():
    en_d.append(line.strip())

for line in fr_file.readlines():
    fr_d.append(line.strip())

for line in es_file.readlines():
    es_d.append(line.strip())

dictionary_length = len(en_d)

# GAME DATA
def lang_check(en, fr, es):
    game_data = []
    if en.get() == 1:
        game_data.append(en_d)
    if fr.get() == 1:
        game_data.append(fr_d)
    if es.get() == 1:
        game_data.append(es_d)
    return game_data

def length_check(length, gamedata):
    play_data = []
    total = dictionary_length
    indices = []

    i = random.randint(0, total-1)
    indices.append(i)
    while len(indices) < length:
        i = random.randint(0, total-1)
        while (i in indices):
            i = random.randint(0, total-1)
        indices.append(i)
    
    for num in indices:
        words = []
        for lst in gamedata:
            words.append(lst[num])
        play_data.append(words)
    
    return play_data

# Generate problem
def generate_problem(length, en, fr, es):
    return length_check(length, lang_check(en, fr, es))

# Memorization time given
def memo_time(words):
    inner_length = len(words[0])
    length = len(words)
    return (inner_length*length*2)

# Give random words added to a list
def random_add(lst, en, fr, es):
    if en.get() == 1:
        lst_w_random_words = random_add_helper(lst, en_d)
        lst = lst_w_random_words
    if fr.get() == 1:
        lst_w_random_words = random_add_helper(lst, fr_d)
        lst = lst_w_random_words
    if es.get() == 1:
        lst_w_random_words = random_add_helper(lst, es_d)
        lst = lst_w_random_words
    return lst

def random_add_helper(lst, lang):
    r_lst = lst
    r_index = random.randint(0, len(lang)-1)
    while lang[r_index] in r_lst:
        r_index = random.randint(0, len(lang)-1)
    r_lst.append(lang[r_index])
    r_index = random.randint(0, len(lang)-1)
    while lang[r_index] in r_lst:
        r_index = random.randint(0, len(lang)-1)
    r_lst.append(lang[r_index])
    return r_lst
