import random                                   # import random module
rl = random.sample(range(0, 1001), 100)         # create list of 100 elements from 1 to 1000
print('Input list - ', rl)                      # print input list

####sort list from min to max (without using sort())#########
for i in range(len(rl)):                        # loop to access each element in the list
    for j in range(len(rl)-1-i):
        if rl[j] > rl[j+1]:                     # compare two elements in the list
            a = rl[j]                           # replace elements if condition for comparison is true
            rl[j] = rl[j+1]
            rl[j+1] = a
print('Sorted list - ', rl)                     # print sorted list

####calculate average for even and odd numbers (case 1)
even_list = []                                  # define list for even values
odd_list = []                                   # define list for odd values
for el in rl:                                   # loop access each element in the list
    if el % 2 == 0:                             # check if the element even or not
        even_list.append(el)                    # if the element even add element in even_list
    else:
        odd_list.append(el)                     # if the element odd add element in odd_list
even_avg = sum(even_list) / len(even_list)      # calculate average for even values
odd_avg = sum(odd_list) / len(odd_list)         # calculate average for odd values
print('Average for even ', even_avg)            # print result
print('Average for odd ', odd_avg)

####calculate average for even and odd numbers (case 2)
ever_sum = 0                                    # define the input variables
ever_count = 0
odd_sum = 0
odd_count = 0
for el in rl:
    if el % 2 == 0:                             # check if the element even or not
        ever_sum = ever_sum + el                # calculate sum of even elements
        ever_count += 1                         # calculate count of even elements
    else:
        odd_sum = odd_sum + el                  # calculate sum of odd elements
        odd_count += 1                          # calculate count of odd elements
print('Average for even ', ever_sum / ever_count)
print('Average for odd ', odd_sum / odd_count)
