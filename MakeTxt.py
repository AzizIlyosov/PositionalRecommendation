
import  pandas  as  pd

df=pd.read_csv('stuid_stuserid.csv',header=None,delim_whitespace=False)
#print('this is  df \n',df)
df.columns=['userid','itemid','one']
max=df.userid.max()
print(max)
# exit()
users=[[] for i in range(max)]


data=[]
with open('stuid_stuserid.csv', 'r') as f:
    for  line  in f:
        data= ([int(i) for i in line.split(',')])
        users[data[0]-1].append(data[1])
# print(users)


with open('one_company_data_new.txt','w') as f:
    for l,el in enumerate(users):
        #print(el)

        string = ' '.join(map(str,el))
        #print(str(el))
        #exit()
        #f.write(str(el))
        for item in string:
            f.write(item)
        f.write('\n')

#
#
# with open("one_company_data_new.txt", "a") as f:
#     for item in users:
#         f.write(str(item) + "\n")

#
# with open('one_company_data_new.txt', 'w') as f:
#     for item in users:
#         f.write("%s\n" % item)
#

