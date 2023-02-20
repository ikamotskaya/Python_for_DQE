import re

str_var = """homEwork:

  tHis iz your homeWork, copy these Text to variable.

 

  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

 

  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.

 

  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""


def convert_str_to_list(inp_str):
    str_list_3 = []
    str_list_1 = inp_str.split('\n\n')      # split string variable by '\n.'. Create list of paragraph
    for row in str_list_1:
        str_list_2 = row.split('.')         # divide paragraphs to sentences
        str_list_3.append(str_list_2)       # combine paragraphs with sentences into one list

    return [i for i in str_list_3 if (i != [' '])]   # remove empty sentences and return result from function


inp_list = convert_str_to_list(str_var)

out_list = []
out_list_2 = []
list_last_words = []


def get_last_word(sentence: str):
    """
     Return
         word[0]: str --> return the last word from the input sentence
    """
    words = sentence.split()             # split by words to extract the last one
    words.reverse()                      # reverse list of words
    return words[0]


def process_first_paragraph(first_par: str):
    """
       Return:
           str -->  return a sentence with correct format (without point at the end)
    """
    return first_par.lower().capitalize()               # convert the first letter to upper case in first sentence


def process_sentences(inp_sent: str):
    """
        Return:
            out_sent: str -->  return a sentence with correct format
    """
    out_sent = inp_sent.strip().lower()                 # convert string in sentences into lower case
    out_sent = out_sent.capitalize() + '.'              # convert the first letter to upper case and add the '.' at the end of the sentence
    return out_sent


def insert_extra_sentence(inp_text: str, number_parag: int, list_words: list):
    """
        Return
            text_with_sent: str --> return a text with an additional sentence which inserted
                                    at the end of the paragraph with number =  number_parag
    """
    new_sent = ' '.join(list_words).capitalize() + '.'          # new sentence from the list words
    list1 = inp_text.split('\n')
    list1[number_parag] = list1[number_parag] + new_sent        # insert the new sentence into the end of
                                                                # paragraph with a number = number_parag
    text_with_sent = '\n'.join(list1)
    print('Text with the additional sentence:', text_with_sent, '\n')
    return text_with_sent


def correct_mistakes(inp_text: str, err: str, corr: str):
    """
        Print the inp_text with corrections. The 'err' is replaced by 'corr'
    """
    correct_text = inp_text.replace(err, corr)
    print(f'Text with corrections {err} to {corr}: {correct_text}  \n')


for parag in inp_list:                                      # iterate by paragraph
    for sent in parag:                                      # iterate by sentences
        if inp_list.index(parag) == 0:
            out_list.append(process_first_paragraph(sent))  # collect modified strings into list
        else:
            if sent not in ['', ' ']:
                out_sent = process_sentences(sent)              # call function
                out_list.append(out_sent)                       # collect modified strings into list
                list_last_words.append(get_last_word(sent))     # gather the last words from the sentence to one list
    out_list_2.append('\n' + ' '.join(out_list))
    out_list = []
normal_text = ' '.join(out_list_2)                                  # normalize text
print('Normalized text', normal_text, '\n')

insert_extra_sentence(normal_text, 3, list_last_words)              # call function

correct_mistakes(normal_text, ' iz ', ' is ')                       # call function

n = re.findall(r'[\s]', str_var)
print(f'Number of whitespaces is {len(n)}')


