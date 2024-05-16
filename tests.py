list1 = [1, 335, 2, 32, 65]
 
str1 = "amritpal singh"

rev_str1 = ""

for i in range(len(str1)-1, -1, -1):
    rev_str1 += str1[i]

print(rev_str1)