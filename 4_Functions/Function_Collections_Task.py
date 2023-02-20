import random
import string

def generate_list(inp_size_list: int, inp_size_dict: int):
    """
        Return:
            out_list: list -->  return the list of dictionaries.
                                List size = inp_size_list, dict size = inp_size_dict
    """
    out_list = []
    global dic
    for d in range(inp_size_list):
        for k in range(inp_size_dict):
            key = random.choice(string.ascii_lowercase)     # generate random letter for key
            val = random.randint(0, 100)                    # generate random number for value
            dic[key] = val                                 # populate dict
        out_list.append(dic)                               # add dict to the end of list
        dic = {}                                           # reset the dict
    return out_list


def get_sorted_list(list1: list):
    """
       Return:
           sorted_list: list -->  return a sorted list of all unique keys from dictionaries
    """
    keys_set = set()                        # define a variable as a set to remove duplicates
    for d in list1:
        for k, v in d.items():
            keys_set.add(k)                 # populate set with keys for result dict
    sorted_list = sorted(list(keys_set))    # create a list with ordered result keys
    return sorted_list


def get_generated_dict(inp_keys: list, inp_list1: list):
    """
       Return:
           out_dict1: dict -->  return dict with keys = inp_keys and
                                values = as max value from all dictionaries
    """
    global dic
    out_dict1 = {}                      # return dict
    for k_out in inp_keys:              # iterate by list
        for d in inp_list1:             # iterate by dict
            for k, v in d.items():      # get key, value from dict
                if k == k_out:          # check the current key with key in result set
                    dic[v] = inp_list1.index(d)  # populate a temporary dict: key = value, value = number of the dict
        if len(dic) == 1:               # if key is only in one dict - take it as is
            out_dict1[k_out] = list(dic.keys())[0]
        else:                           # if dicts have same keys
            m = max(list(dic.keys()))   # take max value
            ind = dic[m]
            out_dict1[k_out + '_' + str(ind + 1)] = m  # rename key with dict number with max value
        dic = {}                        # reset the dict
    return out_dict1


dic = {}   # global dict created according to the rule: key = value from dictionary, value = number of the dict in the list

size_list = random.randint(2,10)                            # set length of list
size_dict = random.randint(2,10)                            # set length of dict
inp_list = generate_list(size_list, size_dict)
print(inp_list)

keys_list = get_sorted_list(inp_list)                       # list of keys for out_dict
out_dict = get_generated_dict(keys_list, inp_list)
print(out_dict)                                             # print result dict
