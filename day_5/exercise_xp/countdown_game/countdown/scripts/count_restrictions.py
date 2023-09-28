def is_user_input_valid(host_word, user_input):
    letters_dict = {}
    for letter in host_word:
        if letter in letters_dict:
            letters_dict[letter] += 1
        else:
            letters_dict[letter] = 1
    for user_letter in user_input:
        try:
            letters_dict[user_letter] -= 1
        except:
            return False
    return True


