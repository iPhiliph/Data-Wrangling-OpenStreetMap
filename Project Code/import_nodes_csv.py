
# coding: utf-8

# In[2]:


import csv, sqlite3

con = sqlite3.connect("shenzhen.db")
con.text_factory = str
cur = con.cursor()


cur.execute('drop table if exists nodes')

nodes = '''
create table nodes
(
id Integer NOT NULL PRIMARY KEY,
lat float,
lon float,
user Text,
uid Integer,
version Text,
changeset Integer,
timestamp Text
);
'''

cur.execute(nodes) # use your column names here

with open('nodes.csv','rb') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    for row in dr:

        id_value = int(row['id'])
        lat_value = float(row['lat'])
        lon_value = float(row['lon'])
        user_value = str(row['user'])
        uid_value = int(row['uid'])
        version_value = str(row['version'])
        changeset_value = int(row['changeset'])
        timestamp_value = str(row['timestamp'])

        #insert = (id_value,lat_value,lon_value,user_value,uid_value,version_value,changeset_value,timestamp_value)
        cur.execute('INSERT INTO nodes VALUES (?,?,?,?,?,?,?,?)',(id_value,lat_value,lon_value,user_value,uid_value,version_value,changeset_value,timestamp_value))

con.commit()
con.close()

