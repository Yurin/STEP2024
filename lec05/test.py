def determin_kaibun(s):
    check = []
    s = s.lower() #大文字を小文字にする
    print(s)
    for i in range(len(s)):
        if(s[i] not in check):
            check.append(s[i])
            print(check)
        else:
            check.remove(s[i])
            print(check)
    if (len(check)) < 2:
        return print(True)
    return print(False)

if __name__ == "__main__":
    test_string = "dAd" 
    test_string2 = "aabbccssjjdkdvk"
    determin_kaibun(test_string)
    determin_kaibun(test_string2)
