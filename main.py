import overpy
import math

class Main:
    def calc(self, x):
        x = float(x)
        x = 5000*x/60
        return x

    def rev_calc(self, x):
        x = x/(5000/60)
        return x

    def input_(self):
        enter_data=[]
        for i in range(0, 6):
            enter_data.append(str(input()))
        return enter_data


    def query_gen(self, enter_data):
        dst1=self.calc(enter_data[0])
        h1=enter_data[1]
        dst2=self.calc(enter_data[2])
        h2=enter_data[3]
        dst3=self.calc(enter_data[4])
        h3=enter_data[5]
        ask="(nwr[building=apartments](around:" + str(float(dst1)*1.1) +","+ h1 + ");-nwr[building=apartments](around:" +  str(float(dst1)*0.5) +","+ h1 + "); )->.a;(nwr[building=apartments](around:"+  str(float(dst2)*1.1) +", "+ h2 + ");-nwr[building=apartments](around:"+  str(float(dst2)*0.5) +", "+ h2 + "); )->.b;(nwr[building=apartments](around:"+  str(float(dst3)*1.1) +", "+ h3 + ");-nwr[building=apartments](around:"+  str(float(dst3)*0.5) +", "+ h3 + "); )->.c;nwr.a.b.c->.d;nwr[entrance](around.d:1);out geom;"
        return ask

    def query(self, ask):
        api = overpy.Overpass()
        Data = api.query(ask)
        centers=[]
        for i in range (-1, len(Data.nodes)-1):
            if "1" == Data.nodes[i].tags.get("ref"):
                centers.append(Data.nodes[i].lat)
                centers.append(Data.nodes[i].lon)
        return centers

    def query_way_gen(self, s1, s2, n):
        ask = "nwr[highway=footway](around:" + str(n) + "," + str(s1) + "," + str(s2) + "); >; out skel qt;"
        return ask

    def DST(self, s1, s2, d1, d2):
        s1 = s1 * math.pi / 180
        d1 = d1 * math.pi / 180
        s2 = s2 * math.pi / 180
        d2 = d2 * math.pi / 180
        distance = 2 * math.asin(
            math.sqrt((math.sin((d1 - s1) / 2) ** 2) + math.cos(d1) * math.cos(s1) * (math.sin((d2 - s2) / 2) ** 2)))
        distance *= 6372795
        return distance

    def query_way(self, s1, s2, d1, d2, SUM, n, flag, N_c, step):
        if flag == 0:
            n = N_c
        s1 = float(s1)
        d1 = float(d1)
        s2 = float(s2)
        d2 = float(d2)
        distance = self.DST(s1, s2, d1, d2)
        if distance >= 0.1:
            send1 = s1
            send2 = s2
            D_const = distance
            ask = self.query_way_gen(s1, s2, n)
            api = overpy.Overpass()
            Data = api.query(ask)
            min_distance = distance
            for i in range(-1, len(Data.nodes) - 1):
                lon = float(Data.nodes[i].lon)
                lat = float(Data.nodes[i].lat)
                distance = self.DST(lat, lon, d1, d2)
                if distance < min_distance:
                    min_distance = distance
                    send1 = lat
                    send2 = lon
            if D_const == min_distance:
                n += step
                flag = 1
            else:
                flag = 0
            SUM += self.DST(send1, send2, s1, s2)
            return self.query_way(d1, d2, send1, send2, SUM, n, flag, N_c, step)
        else:
            return SUM

    def iter_2(self):
        enter=self.input_()
        ask=self.query_gen(enter)
        circle=self.query(ask)
        count_buld=len(circle)
        print("точность max -> min: 10 20 30 40 50")
        ac=int(input())
        print("доп. параметр точности max -> min: 10 20 30")
        step=int(input())
        i=0
        while i < count_buld:
            print(i/count_buld*100, "%")
            if (i==count_buld):
                break
            d1 = str(float(circle[i]))
            d2 = str(float(circle[i+1]))
            s11, s12 = enter[1].split(",")
            s21, s22 = enter[3].split(",")
            s31, s32 = enter[5].split(",")
            way1=(self.rev_calc(self.query_way(s11,s12,d1,d2,0,10,0, ac, step)))
            way2=(self.rev_calc(self.query_way(s21,s22,d1,d2,0,10,0,ac, step)))
            way3=(self.rev_calc(self.query_way(s31,s32,d1,d2,0,10,0,ac, step)))
            if not (((way1>float(enter[0])*0.8)and (way1<float(enter[0])*1.2)) and ((way2>float(enter[2])*0.8)and(way2<float(enter[2])*1.2)) and ((way3>float(enter[4])*0.8)and(way3)<float(enter[4])*1.2)):
                circle.pop(i)
                circle.pop(i)
                count_buld = len(circle)
                if i==count_buld:
                    break
            else:
                i+=2
        print("READY_____________________")
        return circle

    def conv_res(self, results):
        for i in range(0, len(results), 2):
            ask = "nwr[building](around:10," + str(float(results[i])) + "," + str(float(results[i])) + "); out geom;"
            api = overpy.Overpass()
            Data = api.query(ask)
            if len(Data.ways)>=1:
                print(Data.ways[0].tags.get("addr:street"), Data.ways[0].tags.get("addr:housenumber"))

    iter_2()


if __name__ == '__main__':
    pass
