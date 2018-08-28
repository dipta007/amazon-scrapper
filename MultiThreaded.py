from ScrapeTor import parse
# from ScrapeProxy import parse
from GetAsin import get_asins
import threading
import time
import random
import json

outfile = open("JSON/Fjson.out", "w")
data = []
thread_lock = threading.Lock()


class ScrapingThread(threading.Thread):
    def __init__(self, asin):
        threading.Thread.__init__(self)
        self.asin = asin

    def run(self):
        get_data(self.asin)


def get_data(asin):
    current_product = parse(asin)
    if current_product:
        data.append(current_product)
        json_data = json.dumps(current_product, indent=4, sort_keys=False)

        thread_lock.acquire()
        outfile.write(json_data + ",\n")
        thread_lock.release()


def solve():
    outfile.write("[\n")

    asins = get_asins()
    # asins = [
    #     "1138010588", # test for asin \n
    #     "B01GA0JCCU", # categories null
    #     "B0779ML4G5", # unavailable
    #     "B002BXAMJS", # no brand
    #     "B073XVPX83"  # price
    # ]
    threads = []
    for asin in asins:
        thread = ScrapingThread(asin)
        threads.append(thread)

    ind = 0
    while ind < len(threads):
        if threading.active_count() < 96:
            try:
                threads[ind].start()
                print("Completed Thread no ", ind)
                ind += 1
            except Exception as e:
                print("Thread Exception: ")
                print(e)
        else:
            time.sleep(random.randint(1, 4))

    for thread in threads:
        thread.join()

    outfile.write("]\n")
    outfile.close()
    print(len(data))


def current_milli_time():
    return int(round(time.time() * 1000))


if __name__ == "__main__":
    starting = current_milli_time()
    solve()
    ending = current_milli_time()
    print(ending - starting)
    print("Exiting Main")
