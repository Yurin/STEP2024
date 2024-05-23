def binary_search(target, sorted_list):
    low = 0
    high = len(sorted_list) - 1
    while low <= high:
        mid = (low + high) // 2
        guess = ''.join(sorted_list[mid][0])  #タプルの0番目を文字列に変換
        if guess == target:
            return mid
        elif guess < target:
            low = mid + 1
        else:
            high = mid - 1
    return None

def solution(random_word, dictionary):
    sorted_random_word = ''.join(sorted(random_word))  #入力された単語をアルファベット順にソート
    #辞書内の単語をアルファベット順にソートし、頭文字からアルファベット順に並び替え
    sorted_dictionary = [(sorted(word), word) for word in dictionary]
    sorted_dictionary.sort(key=lambda x: (''.join(x[0]), x[1]))  # タプルのリストをアルファベット順にソート
    #ソートしたランダムな単語に一致するものを探す
    index = binary_search(sorted_random_word, sorted_dictionary)
    if index is not None:
        return sorted_dictionary[index][1]  #元の単語を返す
    else:
        return "No anagram found"

input_word = input("Enter a word: ")
with open("words.txt", "r") as file:
    words = file.read().splitlines()
print(solution(input_word, words))
