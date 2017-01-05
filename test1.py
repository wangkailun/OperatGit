import sys
import os
s = sys.argv[0]

s1 = os.path.dirname(s)
s1 = s1+r"\password.txt"
print(s1)



f = open(s1, "w")
f.writelines(["kellen"+"\n", "wys01142399\n"])
f.close()

f = open(s1 , "r")
user = f.readline()
print(user)
f.close()