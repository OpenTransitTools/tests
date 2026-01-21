"""
server stress / performance testing
ws-st.trimet.org/geoserver

https://api.mapbox.com/mapbox-gl-js/v2.6.1/mapbox-gl.css
"""
import time
import random
import requests
from ..utils.threads import Threads


def wms():
    x = -122.52
    y = 45.52
    for n in range(1, 1000):
        k = 0.0000000004 * n
        x += k; y += k;
        print(x, y)


class PatternThreads(Threads):
    @classmethod
    def make_urls(cls):
        """
        build pattern urls to geoserver
        https://ws-st.trimet.org/geoserver/wfs?request=GetFeature&typeName=ott%3Acurrent_patterns&outputFormat=json&cql_filter=id=%27TRIMET:16199747%27

        note: need to edit this file and keep the trip 's' and 'e' ids up-to-date
        """
        #import pdb; pdb.set_trace()
        s = 16199747
        e = 16258754
        urls = []
        base = "https://ws-st.trimet.org/geoserver/wfs?request=GetFeature&typeName=ott%3Acurrent_patterns&outputFormat=json"
        for trip_id in range(s, e):
            u = f"{base}&cql_filter=id=%27TRIMET:{trip_id}%27"
            urls.append(u)
        return urls

    def runner(self):
        with self.lock:
            urls = self.make_urls()

        while not self.exit_flag.is_set():
            with self.lock:
                url = random.choice(urls)
            self.get(url)

    @classmethod
    def run_stress_test(self):
        t = PatternThreads(num_threads=20)
        t.run()
        t.print()


class VectorThreads(Threads):
    @classmethod
    def make_urls(cls):
        """
        create map overlay urls near downtown:
        https://ws-st.trimet.org/geoserver/gwc/service/tms/1.0.0/ott:current@EPSG:900913@pbf/15/5218/21047.pbf?timestamp=1768932767160
        zoom 15: [minx,miny,maxx,maxy] is [5088, 20482, 5452, 21514, 15], index [x,y,z] is [5218, 21047, 15]
        https://ws-st.trimet.org/geoserver/gwc/service/tms/1.0.0/ott:current@EPSG:900913@pbf/16/10436/42094.pbf?timestamp=1768932767160
        zoom 16: [minx,miny,maxx,maxy] is [10176, 40964, 10904, 43029, 16], index [x,y,z] is [10436, 42094, 16]
        https://ws.trimet.org/geoserver/gwc/service/tms/1.0.0/ott:current@EPSG:900913@pbf/17/20869/84189.pbf?timestamp=1768932767160
        zoom 17: [minx,miny,maxx,maxy]is [20352, 81929, 21808, 86058, 17], index [x,y,z] is [20869, 84189, 17]
        https://ws.trimet.org/geoserver/gwc/service/tms/1.0.0/ott:current@EPSG:900913@pbf/18/41740/168380.pbf?timestamp=1768932767160
        [minx,miny,maxx,maxy] is [40705, 163859, 43617, 172117, 18], index [x,y,z] is [41740, 168380, 18]
        https://ws.trimet.org/geoserver/gwc/service/tms/1.0.0/ott:current@EPSG:900913@pbf/19/83482/336760.pbf?timestamp=1768932767160
        [minx,miny,maxx,maxy] is [81410, 327718, 87235, 344235, 19], index [x,y,z] is [83482, 336760, 19]
        https://ws.trimet.org/geoserver/gwc/service/tms/1.0.0/ott:current@EPSG:900913@pbf/20/166963/673522.pbf?timestamp=1768932767160
        [minx,miny,maxx,maxy] is [162820, 655437, 174471, 688471, 20], index [x,y,z] is [166963, 673522, 20]
        """
        urls = []
        layer = "https://ws-st.trimet.org/geoserver/gwc/service/tms/1.0.0/ott:current@EPSG:900913@pbf"
        for x in range(5210, 5220):
            for y in range(21035, 21050):
                url = f"{layer}/15/{x}/{y}.pbf?timestamp={int(time.time())}"
                urls.append(url)

        for x in range(10430, 10440):
            for y in range(42085, 42100):
                url = f"{layer}/16/{x}/{y}.pbf?timestamp={int(time.time())}"
                urls.append(url)

        for x in range(20866, 20876):
            for y in range(84180, 84195):
                url = f"{layer}/17/{x}/{y}.pbf?timestamp={int(time.time())}"
                urls.append(url)

        for x in range(41735, 41745):
            for y in range(168373, 168388):
                url = f"{layer}/18/{x}/{y}.pbf?timestamp={int(time.time())}"
                urls.append(url)

        for x in range(83475, 83485):
            for y in range(336753, 336768):
                url = f"{layer}/19/{x}/{y}.pbf?timestamp={int(time.time())}"
                urls.append(url)

        for x in range(166960, 166970):
            for y in range(673515, 673530):
                url = f"{layer}/20/{x}/{y}.pbf?timestamp={int(time.time())}"
                urls.append(url)
        return urls

    def runner(self):
        with self.lock:
            urls = self.make_urls()
            #print(f"number of urls: {len(urls)}")

        while not self.exit_flag.is_set():
            with self.lock:
                url = random.choice(urls)
            self.get(url)

    @classmethod
    def run_stress_test(self):
        t = VectorThreads(num_threads=20)
        t.run()
        t.print()

