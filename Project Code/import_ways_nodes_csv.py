
# coding: utf-8

# In[2]:


import csv, sqlite3

con = sqlite3.connect("shenzhen.db")
con.text_factory = str
cur = con.cursor()


cur.execute('drop table if exists ways_nodes')

ways_nodes = '''
create table ways_nodes
(
id Integer,
node_id Integer,
position Integer,
FOREIGN KEY (id) REFERENCES ways(id)
);
'''



cur.execute(ways_nodes)

with open('ways_nodes.csv','rb') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    n = 0
    for row in dr:
        if n == 0:
            print (row['id'], row['node_id'], row['position'])
            n += 1

        id_value = int(row['id'])
        node_id_value = str(row['node_id'])
        position_value = str(row['position'])

        cur.execute('INSERT INTO ways_nodes VALUES (?,?,?)',(id_value,node_id_value,position_value))

con.commit()
con.close()

