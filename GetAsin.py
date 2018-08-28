asin_file = open("asin.in");
asin_list = []


def get_asins():
    for i in range(100):
        asin_list.append(asin_file.readline().replace("\n", ""))
    return asin_list