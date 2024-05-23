def read_file(file_name): #ファイルの読み取り
    words = []
    try:
        with open(file_name, "r") as file:
            #ファイルを行ごとに読み込み、改行文字を削除して単語リストに追加
            words = file.read().splitlines()
    except FileNotFoundError:
        print("ファイルが見つかりません")
    return words

def calculate_score(word_list): #スコアの計算
    scores = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4] #文字コードを使う #読みやすさ的にhashの方が良いかも 
    score = 0
    for i in range(26):
        #各文字のスコアを計算して合計
        score += scores[i] * word_list[i]
    return score

def word_counter(word, i): #アルファベットの個数を数える   #ここが紛らわしいからよくする
    cnt = [0] * 29 #なぜ29かを説明する
    for char in word:
        #アルファベットごとに出現回数をカウントし、ビットフラグを設定
        cnt[ord(char) - ord('a')] += 1
        cnt[-1] = cnt[-1] | 1 << (ord(char) - ord('a')) #OR 左シフト
    score = calculate_score(cnt)
    #スコアとインデックスをリストの末尾に追加
    cnt[-2] = score
    cnt[-3] = i
    return cnt

def find_max(random_word, new_dictionary): #最大のアナグラムを検索
    target_word_list = word_counter(random_word, 0)
    alphabets = target_word_list[-1]
    max_anagram_index = -1
    for n in new_dictionary:
        #ターゲットの単語と辞書内の単語がアナグラムかどうかをチェック
        if n[-1] & alphabets != n[-1]:
            continue
        is_anagram = True
        for i in range(26):
            if target_word_list[i] < n[i]:
                is_anagram = False
                break
        if is_anagram:
            max_anagram_index = n[-3]
            return max_anagram_index
    return max_anagram_index

def output_max(target_words, dictionary, output_file): # 最大のアナグラムを出力
    new_dictionary = []
    for i, word in enumerate(dictionary):
        #辞書の各単語に対して、アルファベットの個数をカウントし、スコアとインデックスを追加 
        cnt = word_counter(word, i)
        new_dictionary.append(cnt)
    #スコアに基づいて新しい辞書を降順にソート
    new_dictionary = sorted(new_dictionary, key=lambda x: x[-2], reverse=True)#ここもいい書き方がある気がする
    
    with open(output_file, 'w') as file:#defでわける
        for random_word in target_words:
            #各ターゲット単語に対して最大のアナグラムを探し、ファイルに書き込む
            max_anagram_index = find_max(random_word, new_dictionary)
            if max_anagram_index != -1:
                max_anagram = dictionary[max_anagram_index]
                file.write(f"{max_anagram}\n")
            else:
                file.write("見つかりません\n")

dictionary = read_file("words.txt")
small = read_file("small.txt")
medium = read_file("medium.txt")
large = read_file("large.txt")

output_max(small, dictionary, "small_answer.txt")
print("small_answer.txtの作成が完了")
output_max(medium, dictionary, "medium_answer.txt")
print("medium_answer.txtの作成が完了")
output_max(large, dictionary, "large_answer.txt")
print("large_answer.txtの作成が完了")
#分割して