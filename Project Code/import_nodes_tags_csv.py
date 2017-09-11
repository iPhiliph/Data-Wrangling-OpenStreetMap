
# coding: utf-8

# In[4]:


import csv, sqlite3

con = sqlite3.connect("shenzhen.db")
con.text_factory = str
cur = con.cursor()


cur.execute('drop table if exists nodes_tags')

nodes_tags = '''
create table nodes_tags
(
id Integer,
key Text,
value Text,
type Text,
FOREIGN KEY (id) REFERENCES nodes(id)
);
'''



cur.execute(nodes_tags)

with open('nodes_tags.csv','rb') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    n = 0
    for row in dr:
        if n == 0:
            print (row['id'], row['key'], row['value'], row['type'])
            print type(row['id'])                , type(row['key']),                 type(row['value']), type(row['type'])
            n += 1

        id_value = int(row['id'])
        key_value = str(row['key'])
        value_value = str(row['value'])
        type_value = str(row['type'])

        cur.execute('INSERT INTO nodes_tags VALUES (?,?,?,?)',(id_value,key_value,value_value,type_value))

con.commit()
con.close()

