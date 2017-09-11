
# coding: utf-8

# In[2]:

#!/usr/bin/env python



import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET

#import cerberus





#from schema import Schema

OSM_PATH = "shenzhen_china.osm"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
lower = re.compile(r'^([a-z]|_)*$')  #表示仅包含小写字母且有效的标记

#SCHEMA = Schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']
#===============================================================================================#
#Audit & Clean


def key_type(element, keys):
    if element.tag == "tag":
        global error_attrib                                                  #设置  error_attrib 为全局变量
        k_attrib = element.attrib["k"]
                
        flag = 0                                                                          #前三个判断语句形式类似，利用flag=0作为前三个if语句若为false以外的条件判断
        if re.search(lower, element.attrib["k"]):
            keys["lower"] += 1
            flag = 1

        if re.search(LOWER_COLON, element.attrib["k"]):
            keys["lower_colon"] += 1
            flag = 1

        if re.search(PROBLEMCHARS, element.attrib["k"]):
            keys["problemchars"] += 1
            flag = 1
            error_attrib = k_attrib  # 单独为错误标签设置新变量
                        

        if flag == 0:
            keys["other"] += 1
        
    return keys

def process_map_2(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys

#========================================================================================#

def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    # YOUR CODE HERE
     
    #if element.tag == 'node':

    #elif element.tag == 'way':
    nd_count = 0
    
 #=================================================================#   
 
#keys = process_map_2('shenzhen_china.osm')
#print keys   
#print error_attrib
#temp_attrib  = error_attrib.split(" ") # 将 k_attrib按空格分开
#k_attrib_new = "_".join(temp_attrib).split(':')[1]
#print k_attrib_new

#filename = 'shenzhen_china.osm'

#def update_post_code(post_code):
  #  new_post_code = post_code.replace(' ', '')     #将字符串中的空格删除
  #  return new_post_code

#def  is_post_code(elem):                                                           #构建匹配邮政编码的函数
    #return(elem.attrib['k'] == "addr:postcode")                     #匹配元素中含有属性为k值为 "addr:postcode"的元素 

#for event, elem in ET.iterparse(filename, events=("start",)):                     #用iterparse 一次遍历所有层级的元素
    
    #if elem.tag == "node" or elem.tag == "way":                                               #遍历元素时如果 遇到标签为“node”和"way“”时，
       # for tag in elem.iter("tag"):                                                                            #遍历这些元素
            #if is_post_code(tag):                                                                                  #调用函数is_post_code，匹配属性为 k="addr:postcode"的元素，如果匹配成功；
              #  post_code = tag.attrib['v']                                                                     #获取所在元素属性为v的值；
                #if 'DD' in post_code:                                                               
                 #   new_post_code = post_code.replace(' ', '')[2:]
                  #  tag.attrib['v'] = new_post_code                                                                    #打印清洗结果

#================================================================================#





                    
    for x in element.iter():
        if x.tag == "node" or x.tag == "way":                                               #遍历元素时如果 遇到标签为“node”和"way“”时，
            for tag in x.iter("tag"):                                                                            #遍历这些元素
                if tag.attrib['k'] == "addr:postcode" :                                                           #调用函数is_post_code，匹配属性为 k="addr:postcode"的元素，如果匹配成功；
                    post_code = tag.attrib['v']                                                                     #获取所在元素属性为v的值；
                    if 'DD' in post_code:                                                               
                        new_post_code = post_code.replace(' ', '')[2:]
                        tag.attrib['v'] = new_post_code                                                     #将修改后的结果替换原来的值

        if x.tag == 'nd':                                    #找到标签为nd的元素
            way_nodes.append({'id' : element.attrib['id'],   #构造way_node列表。获取父级元素的属性为id的值；
                                'node_id': x.attrib['ref'],  #获取ref属性的值
                                'position': nd_count})       #每个每一个node下同一个id不同ref的值赋予不同的编号
            nd_count +=1
        elif x.tag == 'tag':                               #找到标签为tag的元素
            if re.search(problem_chars, x.attrib['k']):    #如果遇到问题的元素的属性含有特殊符号，忽略
                continue
            k = x.attrib['k'].split(':', 1)   #按照空格将k="addr:street:name"的属性值分割，同时仅分割一次。
            if len(k) > 1:                      #判定属性K的值是否已分割为[addr,street:name]
                tag_type = k[0]               #将列表K的第一个字符串addr赋予变量tag_type、
                tag_key = k[1]                #将列表K的第二个字符串street:name赋予变量tag_key                  
            else:
                tag_type = 'regular'          #如果“k”值中包含其他“:”，则应该忽略这些“:”并保留为标记键的一部分。
                tag_key = k[0]
            tags.append({'id': element.attrib['id'],  #获取父级元素属性id的值作为键为id的值
                        'key': tag_key,
                        'value': x.attrib['v'],
                        'type': tag_type})
    if element.tag == 'node':
        node_attribs = { x: element.attrib[x] for x in node_attr_fields }
        return {'node': node_attribs, 'node_tags': tags}
    elif element.tag == 'way':
        way_attribs = { x: element.attrib[x] for x in way_attr_fields }
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


#def validate_element(element, validator, schema=SCHEMA):
 #   """Raise ValidationError if element does not match schema"""
   # if validator.validate(element, schema) is not True:
      #  field, errors = next(validator.errors.iteritems())
      #  message_string = "\nElement of type '{0}' has the following errors:\n{1}"
      #  error_string = pprint.pformat(errors)
        
     #   raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file,          codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file,          codecs.open(WAYS_PATH, 'w') as ways_file,          codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file,          codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

     #   validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
              #  if validate is True:
             #       validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(OSM_PATH)


# In[ ]:



