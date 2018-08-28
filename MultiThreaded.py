from ScrapeTor import parse, data
# from ScrapeProxy import parse, data
from GetAsin import get_asins
import threading
import time
import json


class ScrapingThread(threading.Thread):
    def __init__(self, asin):
        threading.Thread.__init__(self)
        # self.thread_id = tid
        self.asin = asin

    def run(self):
        parse(self.asin)


def solve():
    asins = get_asins()
    threads = []
    for asin in asins:
        thread = ScrapingThread(asin)
        threads.append(thread)

    ind = 0
    while ind < len(threads):
        try:
            threads[ind].start()
            threads[ind].join()
            print("Completed Thread no " + ind)
            ind += 1
        except Exception as e:
            time.sleep(10)

    # for thread in threads:
    #     thread.start()
    #
    # for thread in threads:
    #     thread.join()

    json_data = json.dumps(data, indent=4, sort_keys=True)

    outfile = open("json.out", "w")
    outfile.write(json_data)
    outfile.close()
    # print(json_data)
    print(len(data))


def current_milli_time():
    return int(round(time.time() * 1000))


if __name__ == "__main__":
    starting = current_milli_time()
    solve()
    ending = current_milli_time()
    print(ending - starting)
    print("Exiting Main")
