
# coding: utf-8

# In[4]:


import csv, sqlite3

con = sqlite3.connect("shenzhen.db")
con.text_factory = str
cur = con.cursor()


cur.execute('drop table if exists ways')

ways_table = '''
create table ways
(
id Integer primary key,
user Text,
uid Integer,
version Text,
changeset Integer,
timestamp Text
);
'''

cur.execute(ways_table)

with open('ways.csv','rb') as fin:
    dr = csv.DictReader(fin)
    n = 0
    for row in dr:
        if n < 10:
            print row['id'], row['user'], row['uid'], row['version'], row['changeset'], row['timestamp']
            n += 1

        id_value = int(row['id'])
        user_value = str(row['user'])
        uid_value = int(row['uid'])
        version_value = str(row['version'])
        changeset_value = int(row['changeset'])
        timestamp_value = str(row['timestamp'])

        cur.execute('INSERT INTO ways VALUES (?,?,?,?,?,?)',(id_value,user_value,uid_value,version_value,changeset_value,timestamp_value))

con.commit()
con.close()

