"""
server stress / performance testing
ws-st.trimet.org/pelias
"""
import time
import random
import requests
from ..utils.threads import Threads


class AutocompleteThreads(Threads):
    @classmethod
    def make_urls(cls, domain="https://ws-st.trimet.org", rtp="/rtp"):
        """
        build progressive urls to pelias
        https://ws-st.trimet.org/
        """
        #urls = [f"{domain}/peliaswrap/v1{rtp}/autocomplete?text=2112"]; return urls
        urls = []

        #import pdb; pdb.set_trace()
        search_terms = [
            "pdx",
            "zoo",
            "834 SE Lambert Street",
            "888 SE Malden Street",
            "2112 Sandy Boulevard",
            "14222",
            "2112"
        ]
        base = f"{domain}/peliaswrap/v1{rtp}/autocomplete"
        for term in search_terms:
            t = ""
            for c in term:
                t += c
                if c != ' ':
                    u = f"{base}?text={t}"
                    urls.append(u)

        return urls

    def runner(self):
        with self.lock:
            u1 = AutocompleteThreads.make_urls()
            u2 = AutocompleteThreads.make_urls(rtp="")
            urls = u1 + u2

        while not self.exit_flag.is_set():
            with self.lock:
                url = random.choice(urls)
            self.get_json(url, "features")

    @classmethod
    def run_stress_test(self):
        t = AutocompleteThreads(num_threads=20)
        t.run()
        t.print()


class ReverseThreads(Threads):
    @classmethod
    def make_urls(cls, domain="https://ws-st.trimet.org", rtp="/rtp"):
        """
        build progressive urls to pelias
        https://ws-st.trimet.org/peliaswrap/v1/rtp/reverse
        """
        urls = []
        base = f"{domain}/peliaswrap/v1{rtp}/reverse"
        x = -122.52
        y = 45.52
        for n in range(1, 1000):
            k = 0.0000000004 * n
            x += k; y += k;
            u = f"{base}?layers=address&point.lat={y}&point.lon={x}"
            urls.append(u)

        return urls

    def runner(self):
        with self.lock:
            u1 = AutocompleteThreads.make_urls()
            u2 = AutocompleteThreads.make_urls(rtp="")
            urls = u1 + u2

        while not self.exit_flag.is_set():
            with self.lock:
                url = random.choice(urls)
            self.get_json(url, "features")

    @classmethod
    def run_stress_test(self):
        t = AutocompleteThreads(num_threads=20)
        t.run()
        t.print()
