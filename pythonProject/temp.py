# txt = "apple#banana#cherry#orange"
#
# # setting the maxsplit parameter to 1, will return a list with 2 elements!
# x = txt.split("#")[-1]
#
# print(x)


list01=[1,2,2,3,2,5,4]
while list01:
    for x in list01:
        print(x)
        list01.remove(x)