import re

str_var = """homEwork:

  tHis iz your homeWork, copy these Text to variable.

 

  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

 

  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.

 

  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""

str_list_3 = []
str_list_1 = str_var.split('\n\n')                          # split string variable by '\n.'. Create list of paragraph
for row in str_list_1:
    str_list_2 = row.split('.')                             # divide paragraphs to sentences
    str_list_3.append(str_list_2)                           # combine paragraphs with sentences into one list

str_list_3 = [i for i in str_list_3 if (i != [' '])]        # remove empty sentences

out_list = []
out_list_2 = []
list_last_words = []
words = []

for parag in str_list_3:                                    # iterate by paragraph
    for sent in parag:
        a = parag.index(sent)                                   # iterate by sentences
        if sent.upper() == 'HOMEWORK:':                         # why this doesn't work 'parag.index(sent) == 0:' ???
            sent = sent.lower().capitalize()                    # convert the first letter to upper case in first sentence
            out_list.append(sent)                               # collect modified strings into list
        else:
            if sent not in ['', ' ']:
                sent = sent.strip().lower()                         # convert string in sentences into lower case
                words = sent.split()                                # split by words to extract the last one
                words.reverse()                                     # reverse list of words
                list_last_words.append(words[0])                    # gather the last word from the sentence to one list
                sent = sent.capitalize() + '.'                      # convert the first letter to upper case and add the '.' at the end of the sentence
                out_list.append(sent)                               # collect modified strings into list
    out_list_2.append('\n' + ' '.join(out_list))
    out_list = []
normal_text = ' '.join(out_list_2)                                  # normalize text
print('Normalized text',normal_text, '\n')

new_sent = ' '.join(list_last_words).capitalize()+'.'                               # new sentence from the last words
text_with_sent = normal_text.replace('aragraph.', 'aragraph. ' + new_sent)          # add the sentence into end of paragraph into normalized text
print('Text with additional sentence', text_with_sent, '\n')

text_with_correct_is = text_with_sent.replace(' iz ', ' is ')
print('Text with corrections "iz" to  "is"',text_with_correct_is, '\n')

n = re.findall(r'[\s]', str_var)
print(f'Number of whitespaces is {len(n)}')


