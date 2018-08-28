asin_list = []


def get_asins():
    asin_file = open("asin.in");
    for line in asin_file:
        if len(line) > 0:
            asin_list.append(line)
    # for i in range(100):
    #     asin_list.append(asin_file.readline().replace("\n", ""))
    asin_file.close()
    return asin_list
