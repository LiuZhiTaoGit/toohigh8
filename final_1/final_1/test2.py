#coding:utf-8
import pymongo

client=pymongo.MongoClient('localhost',27017)#链接数据库


#创建dbdb数据库
db =client['house_price']

#创建username_id集合
avg_id = db['avg_id']
value_id=db['see_id']
#自增函数
def getNextValue1(avg):
    ret = avg_id.find_and_modify({"_id": avg}, {"$inc": {"sequence_value": 1}}, safe=True, new=True)
    new = ret["sequence_value"]
    return new
def getNextValue2(value):
    ret = avg_id.find_and_modify({"_id": value}, {"$inc": {"sequence_value2": 1}}, safe=True, new=True)
    new = ret["sequence_value2"]
    return new
if __name__=='__main__':
    #插入username_id
    avg_id.insert_one(({'_id': "num", 'sequence_value': 0}))
    value_id.insert_one(({'_id': "num", 'sequence_value2': 0}))