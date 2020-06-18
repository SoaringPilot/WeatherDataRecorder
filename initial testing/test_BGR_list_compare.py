file = open("./mapConfig.txt")

while True:
    result = file.readline()
    if result == "":
        break
    if result.split()[0] == "BGR":
        print(str(result.count("(")) + " " + result.split("List:")[1] )

# There are multiple types of starts:
# 255,  70,  0  -> 13,0,92 Size: 23
# 255,  0,   148
# 255,  127, 191
# 255,  0,   127

# Sizes 5, 7, 11, 14, 18, 22, 23
# 23 Start: 255,70,0
# 22 Start: 204,204,204 (all start this way except the single one below
    # 22 Wrong End Start: 255,127,191
# 18 Start: 204,204,204 :TODO This needs to be extended
# 14 Start: 191,191,191
# 11 Start: 255,0,148
# 7 Start:  255,0,127
# 5 Start:  255,0,127