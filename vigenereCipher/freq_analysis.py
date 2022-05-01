import string

englishLetterFreq = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 
    'O': 7.51, 'I': 6.97, 'N': 6.75, 
    'S': 6.33, 'H': 6.09, 'R': 5.99, 
    'D': 4.25, 'L': 4.03, 'C': 2.78, 
    'U': 2.76, 'M': 2.41, 'W': 2.36, 
    'F': 2.23, 'G': 2.02, 'Y': 1.97, 
    'P': 1.93, 'B': 1.29, 'V': 0.98, 
    'K': 0.77, 'J': 0.15, 'X': 0.15, 
    'Q': 0.10, 'Z': 0.07
}

ETAOIN = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'

LETTERS = string.ascii_letters.upper()

def get_letter_count(message):
    letter_count = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}
    for letter in message.upper():
        if letter in LETTERS:
            letter_count[letter] += 1
    return letter_count

def get_item_zero(x):
    return x[0]

def get_freq_order(message):
    letter_2_freq = get_letter_count(message)
    freq_2_letter = {}
    for letter in LETTERS:
        if letter_2_freq[letter.upper()] not in freq_2_letter:
            freq_2_letter[letter_2_freq[letter.upper()]] = [letter.upper()]
        else:
             freq_2_letter[letter_2_freq[letter.upper()]].append(letter.upper())

    for freq in freq_2_letter:
        freq_2_letter[freq].sort(key=ETAOIN.find, reverse=True)
        freq_2_letter[freq] = ''.join(freq_2_letter[freq])


    freq_pairs = list(freq_2_letter.items())

    freq_pairs.sort(key=get_item_zero, reverse=True)

    freq_order = []

    for freq_pair in freq_pairs:
        freq_order.append(freq_pair[1])

    return ''.join(freq_order)

def eng_freq_match_score(message):
    freq_order = get_freq_order(message)
    match_score = 0
    for common_letter in ETAOIN[:6]:
        if common_letter in freq_order[:6]:
            match_score += 1
    for uncommon_letter in ETAOIN[-6:]:
        if uncommon_letter in freq_order[-6:]:
            match_score += 1

    return match_score
