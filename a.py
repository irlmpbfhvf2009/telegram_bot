
from src.sql._sql import DBHP

a = DBHP().getAdvertiseContent('-1001700543954')
b=[]
for i in a:
    b.append(i[0])
    print(i[0])
print(b)