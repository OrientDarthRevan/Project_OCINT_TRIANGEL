import overpy
import math


def query_way_gen(s1, s2, n):
    ask = "nwr[highway=footway](around:" + str(n) + "," + str(s1) + "," + str(s2) + "); >; out skel qt;"
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
        n = 10
    s1 = float(s1)
    d1 = float(d1)
    s2 = float(s2)
    d2 = float(d2)
    distance = DST(s1, s2, d1, d2)
    if distance >= 40:
        send1 = s1
        send2 = s2
        D_const = distance
        print(distance)
        ask = query_way_gen(s1, s2, n)
        api = overpy.Overpass()
        Data = api.query(ask)
        min_distance = distance
        for i in range(-1, len(Data.nodes) - 1):

            lon = float(Data.nodes[i].lon)
            lat = float(Data.nodes[i].lat)
            distance = DST(lat, lon, d1, d2)
            print(distance, "______", min_distance)
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
        return query_way(d1, d2, send1, send2, SUM, n, flag)
    else:
        print(distance)
        print(SUM)
        return SUM

s1 = str(input())
s2 = str(input())
d1 = str(input())
d2 = str(input())
a=query_way(s1, s2, d1, d2, 0, 10, 0)
print("+=+", a)
