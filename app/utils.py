import os
import re
import typing
import urllib.request
from app.models import today_added_words
 
WORDS_T = typing.List[str]
SRC_NAME = 'russian.txt'
SRC_5_NAME = 'russian-5.txt'
 
 
def load_src_file():
    page = urllib.request.urlopen(
        'https://raw.githubusercontent.com/Harrix/Russian-Nouns/main/dist/'
        'russian_nouns.txt',
    )
    with open(SRC_NAME, 'wb') as stream:
        stream.write(page.read())
 
 
def parse_src_file():
    with open(SRC_NAME, encoding='utf-8') as stream:
        data = stream.read()
    words = []
    for line in data.split('\n'):
        if len(line) != 5 or not line.isalpha():
            continue
        words.append(line)
    with open(SRC_5_NAME, 'w') as stream:
        stream.write('\n'.join(words))
 
 
def parse_words_5() -> WORDS_T:
    with open(SRC_5_NAME) as stream:
        data = stream.read()
    return sorted({line.lower() for line in data.split('\n')})
 
 
def remove_duplicated_letters(words: WORDS_T) -> WORDS_T:
    filtered = []
    for word in words:
        if len(set(word)) != len(word):
            continue
        filtered.append(word)
    return filtered
 
 
def filter_by_letters(
        words: WORDS_T,
        excluded_letters: typing.Iterable[str],
        required_letters: typing.Iterable[str],
) -> WORDS_T:
    filtered = []
    for word in words:
        flag = True
        for letter in excluded_letters:
            if letter in word:
                flag = False
                break
        if not flag:
            continue
        for letter in required_letters:
            if letter not in word:
                flag = False
                break
        if not flag:
            continue
        filtered.append(word)
    return filtered
 
 
def filter_by_mask(words: WORDS_T, mask: str = '\w\w\w\w\w') -> WORDS_T:
    filtered = []
    for word in words:
        if not re.search(mask, word):
            continue
        filtered.append(word)
    return filtered
 
 
def generate_words(exclude_letters: str, required_letters: str, regex_mask: str = '.....') -> WORDS_T:
    src_file = 'russian.txt'
    src_5_letters = 'russian-5.txt'
    if not os.path.isfile(src_5_letters):
        if not os.path.isfile(src_file):
            print('not found src file, loading from github')
            load_src_file()
            print('src file loaded:', SRC_NAME)
        print('not found 5-letters file, parsing')
        parse_src_file()
        print('5-letters file created:', SRC_5_NAME)
 
    words = parse_words_5()
    print(f'count of 5-letter words: {len(words)}')
    
    '''
    counter = collections.Counter(''.join(words))
    print('most common letters in specified words:')
    for key, value in sorted(
            counter.items(), key=lambda x: x[1], reverse=True,
    ):
        print(f'{key}: {value}')
    '''
 
    words = filter_by_mask(words, regex_mask)
    print(f'count of masked letter words: {len(words)}')
 
    words = filter_by_letters(words, exclude_letters, required_letters)
    print(f'count of excluded/required letter words: {len(words)}')
 
    return words


def calculate_variants(today_words):
    exclude_letters = set()
    required_letter = set()
    regex_mask = [[],[],[],[],[]]

    for word in today_words:
        for index, mask_sym in enumerate(word.mask):
            current_letter = word.body[index].lower()
            if mask_sym == '.':
                exclude_letters.add(current_letter)
            elif mask_sym == '!':
                required_letter.add(current_letter)
                regex_mask[index] = current_letter
            elif mask_sym == '^':
                required_letter.add(current_letter)

                if not regex_mask[index]:
                    regex_mask[index] = '^' + current_letter
                elif regex_mask[index][0] == '^' and current_letter not in regex_mask[index]:
                    regex_mask[index] = regex_mask[index] + current_letter

    exclude_letters = ''.join(exclude_letters)
    required_letters = ''.join(required_letter)

    regex_mask_str = ''
    for sym_mask in regex_mask:
        regex_sym_mask = ''
        if not sym_mask:
            regex_sym_mask = '.'
        elif sym_mask[0] == '^':
            regex_sym_mask = '[{}]'.format(sym_mask)
        else:
            regex_sym_mask = sym_mask
        regex_mask_str = regex_mask_str + regex_sym_mask

    variants = generate_words(exclude_letters=exclude_letters,
        required_letters=required_letters,
        regex_mask=regex_mask_str)
    
    return variants
