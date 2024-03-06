import overpy
import math


def calc(x):
    x=float(x)
    x=5000*x/60
    print(x)
    return x

def rev_calc(x):
    x=x/(5000/60)
    return x

def input_():
    enter_data=[]
    for i in range(0, 6):
        enter_data.append(str(input()))
    return enter_data


def query_gen(enter_data):
    dst1=calc(enter_data[0])
    h1=enter_data[1]
    dst2=calc(enter_data[2])
    h2=enter_data[3]
    dst3=calc(enter_data[4])
    h3=enter_data[5]
    ask="(nwr[building=apartments](around:" + str(float(dst1)*1.1) +","+ h1 + ");-nwr[building=apartments](around:" +  str(float(dst1)*0.5) +","+ h1 + "); )->.a;(nwr[building=apartments](around:"+  str(float(dst2)*1.1) +", "+ h2 + ");-nwr[building=apartments](around:"+  str(float(dst2)*0.5) +", "+ h2 + "); )->.b;(nwr[building=apartments](around:"+  str(float(dst3)*1.1) +", "+ h3 + ");-nwr[building=apartments](around:"+  str(float(dst3)*0.5) +", "+ h3 + "); )->.c;nwr.a.b.c;out center;"
    return ask

def query(ask):
    api = overpy.Overpass()
    Data = api.query(ask)
    centers=[]
    for i in range (-1, len(Data.ways)-1):
        centers.append(Data.ways[i].center_lat)
        centers.append(Data.ways[i].center_lon)
    return centers

def query_way_gen(s1, s2, n):
    ask = "nwr[highway](around:" + str(n) + "," + str(s1) + "," + str(s2) + "); >; out skel qt;"
    return ask


def DST(s1, s2, d1, d2):
    s1 = s1 * math.pi / 180
    d1 = d1 * math.pi / 180
    s2 = s2 * math.pi / 180
    d2 = d2 * math.pi / 180
    distance = 2 * math.asin(
        math.sqrt((math.sin((d1 - s1) / 2) ** 2) + math.cos(d1) * math.cos(s1) * (math.sin((d2 - s2) / 2) ** 2)))
    distance *= 6372795
    return distance


def query_way(s1, s2, d1, d2, SUM, n, flag):
    if flag == 0:
        n = 30
    s1 = float(s1)
    d1 = float(d1)
    s2 = float(s2)
    d2 = float(d2)
    distance = DST(s1, s2, d1, d2)
    if distance >= 50:
        send1 = s1
        send2 = s2
        D_const = distance
        ask = query_way_gen(s1, s2, n)
        api = overpy.Overpass()
        Data = api.query(ask)
        min_distance = distance
        for i in range(-1, len(Data.nodes) - 1):

            lon = float(Data.nodes[i].lon)
            lat = float(Data.nodes[i].lat)
            distance = DST(lat, lon, d1, d2)
            if distance < min_distance:
                min_distance = distance
                send1 = lat
                send2 = lon
        if D_const == min_distance:
            n += 10
            flag = 1
        else:
            flag = 0
        SUM += DST(send1, send2, s1, s2)
        print("--------------------", SUM)
        return query_way(send1, send2, d1, d2, SUM, n, flag)
    else:
        return SUM

def iter_2():
    enter=input_()
    ask=query_gen(enter)
    circle=query(ask)
    count_buld=len(circle)
    i=0
    for i in range(0, count_buld):
        print(i/count_buld*100, "%")
        print(i)
        if (i==count_buld):
            break
        if(i%2!=0):
            i=i-1
        d1 = str(float(circle[i]))
        d2 = str(float(circle[i+1]))
        s11 , s12 = enter[1].split(",")
        print(s11, s12, "/////", d1, d2)
        s21, s22 = enter[3].split(",")
        s31, s32 = enter[5].split(",")
        way1=(rev_calc(query_way(s11,s12,d1,d2,0,10,0)))
        way2=(rev_calc(query_way(s21,s22,d1,d2,0,10,0)))
        way3=(rev_calc(query_way(s31,s32,d1,d2,0,10,0)))
        if not (((way1>float(enter[0])*0.8)and (way1<float(enter[0])*1.1)) and ((way2>float(enter[2])*0.8)and(way2<float(enter[2])*1.1)) and ((way3>float(enter[4])*0.8)and(way3)<float(enter[4])*1.1)):
            circle.pop(i)
            circle.pop(i)
            print(circle)
            print(len(circle))
            count_buld = len(circle)
            if i==count_buld:
                break
            print(i, count_buld)
    print("READY_____________________")
    for i in range (len(circle)-1):
        print(float(circle[i]), float(circle[i+1]))
iter_2()