import random
import string

inp_list = []
size_list = random.randint(2,10)                            # set length of list
dic = {}
size_dict = random.randint(2,10)                            # set length of dict

for d in range(size_list):
    for k in range(size_dict):
        key = random.choice(string.ascii_lowercase)         # generate random letter for key
        val = random.randint(0,100)                         # generate random number for value
        dic[key] = val                                      # populate dict
    inp_list.append(dic)                                    # add dict to the end of list
    dic = {}                                                # reset the dict

print(inp_list)

keys_set = set()                                            # define a variable as a set to remove duplicates
for d in inp_list:
    for k, v in d.items():
        keys_set.add(k)                                     # populate set with keys for result dict
keys_list = sorted(list(keys_set))                          # create a list with ordered result keys

out_dict = {}                                               # result dict

for k_out in keys_list:                                     # iterate by list
    for d in inp_list:                                      # iterate by dict
        for k, v in d.items():                              # get key, value from dict
            if k == k_out:                                  # check the current key with key in result set
                dic[v] = inp_list.index(d)                  # populate a temporary dict: key = value, value = number of the dict
    if len(dic) == 1:                                       # if key is only in one dict - take it as is
        out_dict[k_out] = list(dic.keys())[0]
    else:                                                   # if dicts have same keys
        m = max(list(dic.keys()))                           # take max value
        ind = dic[m]
        out_dict[k_out+'_'+str(ind+1)] = m                  # rename key with dict number with max value
    dic = {}                                                # reset the dict

print(out_dict)                                             # print result dict
