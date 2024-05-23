#!/usr/bin/python3

import sys

# 使い方:
#
# $ python3 score_checker.py データファイル 回答ファイル
#

# 各文字のスコア:
# ----------------------------------------
# | 1ポイント  | a, e, h, i, n, o, r, s, t |
# | 2ポイント  | c, d, l, m, u             |
# | 3ポイント  | b, f, g, p, v, w, y       |
# | 4ポイント  | j, k, q, x, z             |
# ----------------------------------------
SCORES = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]

WORDS_FILE = "words.txt"

def calculate_score(word):
    score = 0
    for character in list(word):
        score += SCORES[ord(character) - ord('a')]
    return score

def read_words(word_file):
    words = []
    with open(word_file) as f:
        for line in f:
            line = line.rstrip('\n')
            words.append(line)
    return words

def is_anagram(anagram, data):
    data_table = [0] * 26
    for character in data:
        data_table[ord(character) - ord('a')] += 1
    for character in anagram:
        if data_table[ord(character) - ord('a')] == 0:
            return False
        data_table[ord(character) - ord('a')] -= 1
    return True

def main(data_file, answer_file):
    valid_words = read_words(WORDS_FILE)
    data_words = read_words(data_file)
    answer_words = read_words(answer_file)
    
    if len(data_words) != len(answer_words):
        print(f"{data_file}と{answer_file}の単語数が一致しません。")
        exit(1)
    
    total_score = 0
    highest_score = 0
    highest_scoring_word = ""
    
    for i in range(len(data_words)):
        if not is_anagram(answer_words[i], data_words[i]):
            print(f"'{answer_words[i]}'は'{data_words[i]}'のアナグラムではありません。")
            exit(1)
        if answer_words[i] not in valid_words:
            print(f"'{answer_words[i]}'は有効な単語ではありません。")
            exit(1)
        
        word_score = calculate_score(answer_words[i])
        total_score += word_score
        
        if word_score > highest_score:
            highest_score = word_score
            highest_scoring_word = answer_words[i]
    
    print(f"あなたの回答は正しいです！ 総スコアは{total_score}です。")
    print(f"最高スコアの単語は'{highest_scoring_word}'で、スコアは{highest_score}です。")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"使い方: {sys.argv[0]} データファイル 回答ファイル")
        exit(1)
    main(sys.argv[1], sys.argv[2])
