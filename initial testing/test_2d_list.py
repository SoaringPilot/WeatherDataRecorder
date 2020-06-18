from array import *
my_test = [[0]*3 for i in range(4)]
list1 = [1,2,3]     # forecast for last_rev
list2 = [2,6,3]     # forecast for second to last rev
master = []
last_rev = 3


master.append(list1)
print(master)
list2[0] = 0
master.append(list2)
print(master)
print(my_test)
my_test[0][2] = 14
print(my_test)
