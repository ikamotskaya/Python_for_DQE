import csv
from collections import Counter


def read_file(path: str):
    """
    :return: str: text from a file with path = 'path'
    """
    with open(path) as inp_file:
        text = inp_file.read()
        return text


def create_word_count_dict(list_words: list):
    """
    :return: dict in the follow format {word: count in the list_words}
    """
    list_words = list(map(lambda x: x.lower(), list_words))
    set_words = set(list_words)
    dict_words = dict.fromkeys(set_words, 0)
    for i in list_words:
        dict_words[i] += 1
    return dict_words


def write_word_count_csv(path: str, dict_word_count: dict):
    """
    write dict_word_count in the csv file with delimiter = '-'
    """
    with open(path, 'w') as csv_word_count:
        writer = csv.writer(csv_word_count, delimiter='-', lineterminator='\n')
        for k, v in dict_word_count.items():
            writer.writerow([k, v])


def create_letter_dict(text: str):
    """
    :return:  dict in the follow format {letter: 'count letter in the text'}
    """
    text_lower = text.lower()
    res = {i: text.count(i) for i in text_lower if i.isalpha()}      # isalpha - to skip spaces/punctuations
    print(res)
    return res


def create_upper_letter_dict(text: str):
    """
    :return:  dict in the follow format {Upper letter: 'count Upper letter in the text'}
    """
    res = {i: text.count(i) for i in text if i.isupper()}
    print(res)
    return res


def write_letter_count_csv(path, let, up_let, header):
    """
    write csv file with follow format 'letter','count_all', 'count_uppercase', 'percentage'
    """
    with open(path, 'w') as csv_file:
        writer = csv.writer(csv_file, lineterminator='\n')
        writer.writerow(header)
        for k1, v1 in let.items():
            if k1.upper() not in up_let.keys():
                writer.writerow([k1, v1, 0, 0])
            for k2, v2 in up_let.items():
                if k1 == k2.lower():
                    writer.writerow([k1, v1, v2, f'{round(v2/v1,2)}%'])


def main():
    path = 'News feed.txt'
    text = read_file(path)

#  create word_count.csv file
    list_words = text.split()
    dict_word_count = create_word_count_dict(list_words)
    print(dict_word_count)
    write_word_count_csv('word_count.csv', dict_word_count)

#  create letter_count.csv file
    let = create_letter_dict(text)
    up_let = create_upper_letter_dict(text)
    header = ['letter', 'count_all', 'count_uppercase', 'percentage']
    write_letter_count_csv('letter_count.csv', let, up_let, header)


if __name__ == "__main__":
    main()
