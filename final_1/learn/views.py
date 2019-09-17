from django.shortcuts import render,redirect,reverse
from django.db import connection
import pymongo
import os
from pyecharts import options as opts
from final_1.test2 import getNextValue1 #导入自增函数
from final_1.test2 import getNextValue2 #导入自增函数
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from pyecharts.charts import Bar,Page,Geo,Line
import json
# 构造MongoDB client
client = pymongo.MongoClient("mongodb://localhost:27017/test:123")
# 连接house_price数据库
# db = client['house_price']
# # 连接beike集合
# mycol = db['beike']

#数据库总体
#房价数据库
db = client['house_price']
mycol = db['ershoufang_pirce']
#空气质量aqi
db2 = client['weather']
mycol2 = db2['pm_all_sorted_avg']

 # 温度
mycol3 = db2['tianqi_avg']

mycol4 = db['rent']

# 新房
mycol5 = db['xinfang_show']




global city_name
city_name = []

# 各区县对应的均价
# 二手房地址对应的价格

global ershoufang_num
ershoufang_num = []

global weather_aqis_num
weather_aqis_num = []


# 买房：buy_house
        # 租房：renting
        # 空气质量aqi：aqi
        # 温度： temperature
        # 工作数量： job_number
        # 工资：salary
global buy_house_num
buy_house_num = []

global buy_house_num_sorted
buy_house_num_sorted = []

global renting_num
renting_num = []
global renting_num_sorted
renting_num_sorted = []

global aqi_num
aqi_num = []
global aqi_num_sorted
aqi_num_sorted = []

global temperature_num
temperature_num = []
global temperature_num_sorted
temperature_num_sorted = []


global job_number_num
job_number_num = []
global job_number_num_sorted
job_number_num_sorted = []


global salary_num
salary_num = []
global salary_num_sorted
salary_num_sorted = []

# allindex


global series
series = []






def a_ren(request):
    render(request, 'a_ren.html')
def b_ren(request):
    render(request, 'b_ren.html')
def ab_ren(request):
    render(request, 'ab_ren.html')
# 买房：buy_house
        # 租房：renting
        # 空气质量aqi：aqi
        # 温度： temperature
        # 工作数量： job_number
        # 工资：salary
#二手房的表格
def showBuyhouse():
    # 对新房的num进行排序

    # 排名图
    a = []
    b = []
    for i in mycol5.find():
        a.append(i['_id'])
        b.append(i['per_price'])
    x = (
        Bar()
            .add_xaxis(a)
            .add_yaxis("新房价格", b)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="新房价格柱状排名图"),
            datazoom_opts=opts.DataZoomOpts(range_start=0, range_end=10),
            toolbox_opts=opts.ToolboxOpts(),
            visualmap_opts=opts.VisualMapOpts(min_=5000, max_=65000)
        )
    )
    page.add(x)


    #对二手房的num进行排序
    for row in mycol.find().sort("name", -1):
        # print(row)
        # print("二手房的num name")

        ershoufang_num.append(row['num'])
        # print(row['num'])
        city_name.append(row['name'])
        # print(row['name'])



    # 排名图
    a = []
    b = []
    for i in mycol.find():
        a.append(i['name'])
        b.append(i['pricec'])
    c = (
        Bar()
            .add_xaxis(a)
            .add_yaxis("二手房", b)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="二手房价格柱状排名图"),
            datazoom_opts=opts.DataZoomOpts(range_start=0,range_end=10),
            toolbox_opts=opts.ToolboxOpts(),
            visualmap_opts=opts.VisualMapOpts(min_=5000, max_=65000)
        )
    )
    page.add(c)

    districts = []
    value = []

    for i in mycol.find():
        districts.append(i['name'])
        value.append(i['pricec'])

    dis = tuple(districts)
    val = tuple(value)

    data = []

    for i in range(len(dis)):
        q = (dis[i], val[i])
        data.append(q)
    print(data)

    d = (
        Geo()
            .add_schema(maptype="china", itemstyle_opts=opts.ItemStyleOpts(color="#7EC0EE", border_color="yellow"), )
            # .add("geo",districts,value)
            .add("geo", [list(z) for z in zip(dis, val)])
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(max_=20000, min_=5000, is_piecewise=True),
            title_opts=opts.TitleOpts(title="二手房价格-地图"),
            toolbox_opts=opts.ToolboxOpts(is_show=True)
        )
    )

    page.add(d)






def showRenting():
    # 对空气质量renting，进行排序
    for row in mycol4.find().sort("_id", -1):
        # print("空气质量")
        # print(row)
        # print(row['num'])
        renting_num.append(row['num'])

    a = []
    b = []
    for i in mycol4.find():
        a.append(i['_id'])
        b.append(i['price'])
    c = (
        Bar()
            .add_xaxis(a)
            .add_yaxis("fj", b)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="租房价格柱状排名图"),
            datazoom_opts=opts.DataZoomOpts(range_start=0, range_end=10),
            toolbox_opts=opts.ToolboxOpts(),
            visualmap_opts=opts.VisualMapOpts(min_=50, max_=100)
        )
    )
    page.add(c)





def showAqi():
    # 对空气质量aqi，进行排序
    for row in mycol2.find().sort("name", -1):
        # print("空气质量")
        # print(row)
        # print(row['num'])
        weather_aqis_num.append(row['num'])

    a = []
    b = []
    for i in mycol2.find():
        a.append(i['name'])
        b.append(i['aqi'])
    c = (
        Bar()
            .add_xaxis(a)
            .add_yaxis("AQI", b)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="空气质量AQI柱状排名图"),
            datazoom_opts=opts.DataZoomOpts(range_start=0, range_end=10),
            toolbox_opts=opts.ToolboxOpts(),
            visualmap_opts=opts.VisualMapOpts(min_=50, max_=100)
        )
    )
    page.add(c)


    # 展示折线图，空气质量的各种因素

    name = []
    aqi = []
    co = []
    no2 = []
    o3 = []
    pm10 = []
    pm2_5 = []

    so2 = []
    for i in mycol2.find():
        # print(i['name'])
        name.append(i['name'])
        aqi.append(i['aqi'])

        co.append(i['co'])
        no2.append(i['no2'])
        o3.append(i['o3'])
        pm10.append(i['pm10'])
        pm2_5.append(i['pm2_5'])

        so2.append(i['so2'])

    data = []
    for i in range(len(name)):
        t = [aqi[i], co[i], no2[i]]
        data.append(t)
        print(t)

    c = (
        Line()
            .add_xaxis(name)
            .add_yaxis("aqi(空气质量指数)", aqi)
            .add_yaxis("co", co)
            .add_yaxis("no2", no2)
            .add_yaxis("o3", o3)
            .add_yaxis("pm10", pm10)
            .add_yaxis("pm2_5", pm2_5)
            .add_yaxis("so2", so2)

            .set_global_opts(title_opts=opts.TitleOpts(title="空气质量"),
                             datazoom_opts=opts.DataZoomOpts(is_show=True, range_start=0, range_end=3))
    )
    page.add(c)




def showTemperature():
    # 对空气质量温度，进行排序
    for row in mycol3.find().sort("_id", -1):
        # print("空气质量")
        # print(row)
        # print(row['num'])
        temperature_num.append(row['num'])

    a = []
    b = []
    for i in mycol3.find():
        a.append(i['_id'])
        b.append(i['temp_avg'])
    c = (
        Bar()
            .add_xaxis(a)
            .add_yaxis("fj", b)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="天气温度柱状排名图"),
            datazoom_opts=opts.DataZoomOpts(range_start=0, range_end=10),
            toolbox_opts=opts.ToolboxOpts(),
            visualmap_opts=opts.VisualMapOpts(min_=50, max_=100)
        )
    )
    page.add(c)
def showJobnumber():
    pass
def showSalary():
    pass





def index(request):


    if request.method == "GET":
        return render(request, 'index.html')
    else:
        global page
        page = Page()

        city_name = []
        buy_house_num = []
        buy_house_num_sorted = []
        renting_num = []
        renting_num_sorted = []
        temperature_num = []
        temperature_num_sorted = []
        aqi_num = []
        aqi_num_sorted = []
        salary_num = []

        job_number_num = []

        # 买房：buy_house
        # 租房：renting
        # 空气质量aqi：aqi
        # 温度： temperature
        # 工作数量： job_number
        # 工资：salary
        buy_house = request.POST.get("buy_house")
        buy_house_value = request.POST.get("buy_house_value")

        renting = request.POST.get("renting")
        renting_value = request.POST.get("renting_value")

        aqi = request.POST.get("aqi")
        aqi_value = request.POST.get("aqi_value")

        temperature = request.POST.get("temperature")
        temperature_value = request.POST.get("temperature_value")

        job_number = request.POST.get("job_number")
        job_number_value = request.POST.get("job_number_value")

        salary = request.POST.get("salary")
        salary_value = request.POST.get("salary_value")

        sum = 0
        sum = float(sum)
        rev = ""
        # 买房：buy_house
        # 租房：renting
        # 空气质量aqi：aqi
        # 温度： temperature
        # 工作数量： job_number
        # 工资：salary


        series = []
        if(buy_house_value != ""):
            for row in mycol.find().sort("name", -1):
                # print(row)
                # print("二手房的num name")
                buy_house_num.append(row['num'])
            rev = rev + "buy_house_"

            for i in buy_house_num:
                qqq = round(float(i) * float(buy_house_value), 2)
                buy_house_num_sorted.append(qqq)

            t = {
                'name': '买房价格得分',
                'type': 'line',
                'stack': '总量',
                'smooth': 'true',

                'label': {
                    'normal': {
                        'show': 'true',
                        'position': 'top'
                    }
                },
                'areaStyle': {'normal': {}},

                'data': buy_house_num_sorted
            }
            series.append(t)


        if(renting_value != ""):
            rev = rev + "renting_"
            for row in mycol4.find().sort("_id", -1):
                # print(row)
                # print("二手房的num name")
               renting_num.append(row['num'])


            for i in renting_num:
                qqq = round(float(i) * float(renting_value), 2)
                renting_num_sorted.append(qqq)

            t = {
                'name': '租房价格得分',
                'type': 'line',
                'stack': '总量',
                'smooth': 'true',
                'label': {
                    'normal': {
                        'show': 'true',
                        'position': 'top'
                    }
                },
                'areaStyle': {'normal': {}},

                'data': renting_num_sorted
            }
            series.append(t)



        if(aqi_value != ""):
            rev = rev + "aqi_"

            for row in mycol2.find().sort("name", -1):
                # print(row)
                # print("二手房的num name")

                aqi_num.append(row['num'])
            # aqi_num_sorted = float(aqi_value) * float(aqi_num)

            for i in aqi_num:
                qqq = round(float(i) * float(aqi_value), 2)
                aqi_num_sorted.append(qqq)

            t = {
                'name': '空气质量aqi得分',
                'type': 'line',
                'stack': '总量',
                'smooth': 'true',
                'label': {
                    'normal': {
                        'show': 'true',
                        'position': 'top'
                    }
                },
                'areaStyle': {'normal': {}},

                'data': aqi_num_sorted
            }
            series.append(t)


        if(temperature_value != ""):
            rev = rev + "temperature_"
            for row in mycol3.find().sort("_id", -1):
                temperature_num.append(row['num'])
            # aqi_num_sorted = float(aqi_value) * float(aqi_num)

            for i in temperature_num:
                qqq = round(float(i) * float(temperature_value), 2)
                temperature_num_sorted.append(qqq)

            t = {
                'name': '温度舒适度得分',
                'type': 'line',
                'stack': '总量',
                'smooth': 'true',
                'label': {
                    'normal': {
                        'show': 'true',
                        'position': 'top'
                    }
                },
                'areaStyle': {'normal': {}},

                'data': temperature_num_sorted
            }
            series.append(t)

        if(job_number == "on"):
            rev = rev + "job_number_"

        if(salary == "on"):
            rev = rev + "salary_"





        print("rev_____________")
        print(rev)


        if(rev == "buy_house_"):
            showBuyhouse()
            page.render('./templates/%s_ren.html' % rev)
            return render(request, '%s_ren.html'%rev)
        elif(rev == "aqi_"):
            showAqi()
            page.render('./templates/%s_ren.html' % rev)
            return render(request, '%s_ren.html' % rev)
        elif(rev == "temperature_"):
            showTemperature()
            page.render('./templates/%s_ren.html' % rev)
            return render(request, '%s_ren.html' % rev)
        elif(rev == "renting_"):
            showRenting()
            page.render('./templates/%s_ren.html' % rev)
            return render(request, '%s_ren.html' % rev)
        else:
            for row in mycol.find().sort("name", -1):

                city_name.append(row['name'])

            all = series
            city = city_name

            all_len = len(all)

            if (all_len == 2):
                # print("对了")
                data0 = all[0]['data']
                data1 = all[1]['data']

                sum = []

                for i in range(len(data0)):
                    t = (city[i], float(data0[i]) + float(data1[i]), data0[i], data1[i])
                    sum.append(t)

                def takeSecond(elem):
                    return elem[1]

                sum.sort(key=takeSecond, reverse=True)

                sum_ed = sum
                city_ed = []
                dict_0_ed = []
                dict_1_ed = []
                # print(sum_ed)
                # print("8"*10)
                for i in range(len(data0)):
                    # print(i)
                    city_ed.append(sum_ed[i][0])
                    # print(city_ed)
                    dict_0_ed.append(sum_ed[i][2])
                    # print(dict_0_ed)
                    dict_1_ed.append(sum_ed[i][3])
                    # print(dict_1_ed)
                # print("*"*10)
                # print(city_ed)
                #
                # print(dict_0_ed)
                # print(dict_1_ed)

                city = city_ed

                all[0]['data'] = dict_0_ed
                all[1]['data'] = dict_1_ed
                #
                # print("*" * 20)
                # print(city)
                # print(all)

                series = all
                city_name = city


            if (all_len == 3):
                # print("对了")
                data0 = all[0]['data']
                data1 = all[1]['data']
                data2 = all[2]['data']

                sum = []

                for i in range(len(data0)):
                    t = (city[i], float(data0[i]) + float(data1[i]) + float(data2[i]), data0[i], data1[i], data2[i])
                    sum.append(t)

                def takeSecond(elem):
                    return elem[1]

                sum.sort(key=takeSecond, reverse=True)

                sum_ed = sum
                city_ed = []
                dict_0_ed = []
                dict_1_ed = []
                dict_2_ed = []
                # print(sum_ed)
                # print("8"*10)
                for i in range(len(data0)):
                    # print(i)
                    city_ed.append(sum_ed[i][0])
                    # print(city_ed)
                    dict_0_ed.append(sum_ed[i][2])
                    # print(dict_0_ed)
                    dict_1_ed.append(sum_ed[i][3])
                    dict_2_ed.append(sum_ed[i][4])
                    # print(dict_1_ed)
                # print("*"*10)
                # print(city_ed)
                #
                # print(dict_0_ed)
                # print(dict_1_ed)

                city = city_ed

                all[0]['data'] = dict_0_ed
                all[1]['data'] = dict_1_ed
                all[2]['data'] = dict_2_ed

                series = all
                city_name = city

            if (all_len == 4):
                # print("对了")
                data0 = all[0]['data']
                data1 = all[1]['data']
                data2 = all[2]['data']
                data3 = all[3]['data']

                sum = []

                for i in range(len(data0)):
                    t = (
                    city[i], float(data0[i]) + float(data1[i]) + float(data2[i]) + float(data3[i]), data0[i], data1[i],
                    data2[i], data3[i])
                    sum.append(t)

                def takeSecond(elem):
                    return elem[1]

                sum.sort(key=takeSecond, reverse=True)

                sum_ed = sum
                city_ed = []
                dict_0_ed = []
                dict_1_ed = []
                dict_2_ed = []
                dict_3_ed = []
                # print(sum_ed)
                # print("8"*10)
                for i in range(len(data0)):
                    # print(i)
                    city_ed.append(sum_ed[i][0])
                    # print(city_ed)
                    dict_0_ed.append(sum_ed[i][2])
                    # print(dict_0_ed)
                    dict_1_ed.append(sum_ed[i][3])
                    dict_2_ed.append(sum_ed[i][4])
                    dict_3_ed.append(sum_ed[i][5])
                    # print(dict_1_ed)
                # print("*"*10)
                # print(city_ed)
                #
                # print(dict_0_ed)
                # print(dict_1_ed)

                city = city_ed

                all[0]['data'] = dict_0_ed
                all[1]['data'] = dict_1_ed
                all[2]['data'] = dict_2_ed
                all[3]['data'] = dict_3_ed

                series = all
                city_name = city

            return render(request, 'render_test.html', {"series": json.dumps(series),"city_name":json.dumps(city_name)},)

        # 买房：buy_house
        # 租房：renting
        # 空气质量aqi：aqi
        # 温度： temperature
        # 工作数量： job_number
        # 工资：salary

