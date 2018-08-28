from torrequest import TorRequest
from UserAgentList import user_agent_list
import random
from bs4 import BeautifulSoup
from time import sleep

tr = TorRequest()
baseUrl = "http://www.amazon.com/dp/"
data = []


def reset_my_identity(url):
    tr.reset_identity()
    # tr.ctrl.signal('CLEARDNSCACHE')  # see Stem docs for the full API
    #
    # print(type(tr.session))  # a requests.Session object
    # c = cookielib.CookieJar()
    # tr.session.cookies.update(c)
    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent': user_agent}
    page = tr.get(url, headers=headers)
    return page


def get_feature(soup):
    feature_list = [];
    features = soup.find(id="feature-bullets")
    if features is None:
        return "None"
    for feature in features.find_all(class_="a-list-item"):
        feature_list.append(feature.getText().strip())

    return feature_list


def get_description(soup):
    des = soup.find(id="productDescription")
    if des is None:
        return "None"
    return des.getText().strip()


def get_price(soup):
    if soup.find(id="priceblock_ourprice") is not None:
        price_str = soup.find(id="priceblock_ourprice").getText().strip()
        price_str = price_str.replace("$", "")
        try:
            price = float(price_str)
            price = price * 100.0
            return price
        except Exception as e:
            return price_str
    elif soup.find(id="price_inside_buybox") is not None:
        price_str = soup.find(id="price_inside_buybox").getText().strip()
        price_str = price_str.replace("$", "")
        try:
            price = float(price_str)
            price = price * 100.0
            return price
        except Exception as e:
            return price_str
    else:
        prices = soup.find_all(class_="a-color-price")
        price_str = prices[1].getText().strip()
        try:
            price_str2 = price_str.replace("$", "")
            price = float(price_str2)
            price = price * 100.0
            return price
        except Exception as e:
            return price_str


def get_dimension(soup):
    product_details = soup.find(id="prodDetails")
    if product_details is None:
        return "None"
    else:
        curr_dimension = {};
        curr = ""
        counter = 0
        for detail in product_details.find_all(class_="a-size-base"):
            if curr == "Dimension":
                dimension = detail.getText().split()
                curr_dimension['length'] = dimension[0] + " " + dimension[5];
                curr_dimension['width'] = dimension[2] + " " + dimension[5];
                curr_dimension['height'] = dimension[4] + " " + dimension[5];
                counter += 1
                curr = "";
            elif curr == "Weight":
                curr_dimension['weight'] = detail.getText().strip();
                counter += 1
                curr = ""

            if detail.getText().strip() == "Product Dimensions":
                curr = "Dimension"
            elif detail.getText().strip() == "Item Weight":
                curr = "Weight"

            if counter == 2:
                break

        return curr_dimension


def get_images(soup):
    images = []
    image_div = soup.find(id="altImages")
    if image_div is None:
        image_div = soup.find(id="imageBlockThumbs")
    if image_div is None:
        return None;

    for image in image_div.find_all("img"):
        if image["src"].endswith(".jpg"):
            image_src = image["src"].split(".")
            image_src[len(image_src)-2] = "_UL900_"
            images.append(".".join(image_src))

    return images


def get_attr(soup):
    attributes = []
    attribute_div = soup.find(id="twister")

    if attribute_div is None:
        return None
    for attribute in attribute_div.find_all(class_="a-row"):
        try:
            attr = {}
            attr["name"] = attribute.find(class_="a-form-label").getText().strip()
            attr["value"] = attribute.find(class_="selection").getText().strip()
            attributes.append(attr)
        except Exception as e:
            e = 1+2
            # print("Exception in attr ", e)

    return attributes


def get_categories(soup):
    category_list = []
    category_div = soup.find(id="wayfinding-breadcrumbs_feature_div")
    if category_div is None:
        return None
    for category in category_div.find_all(class_="a-color-tertiary"):
        try:
            now_cat = {}
            url = category["href"]
            url_list = url.split("node=")
            now_cat["node"] = url_list[-1]
            now_cat["title"] = category.getText().strip()
            category_list.append(now_cat)
        except Exception as e:
            e = 1+2

    return category_list


def get_similar_items(soup):
    similar_items = []
    for item in soup.find_all(class_="a-carousel-card"):
        try:
            similar_asin = item.find("div")['data-asin'].strip()
            similar_items.append(similar_asin)
        except Exception as e:
            e = 1+2

    return similar_items


def get_rating(soup):
    review_div = soup.find(id="reviewSummary")
    if review_div is None:
        return None
    else:
        rating_str = review_div.find(class_="a-icon-alt")
        if rating_str is None:
            return float(0.0)
        rating_str = rating_str.getText().strip()
        rating_list = rating_str.split(" ");
        rating = float(rating_list[0])
        return rating


def parse(asin):
    url = baseUrl + asin

    try:
        for iteration in range(20):
            sleep(random.randint(1,4))
            page = reset_my_identity(url)
            soup = BeautifulSoup(page.content, 'html.parser')

            if soup.find(id="bylineInfo") is None:
                raise ValueError('Not available')

            if soup.find(id="productTitle") is None:
                raise ValueError('Captcha Strikes :\'(')


            current_product = {}
            current_product['asin'] = asin
            current_product['title'] = soup.find(id="productTitle").getText().strip()
            current_product['brand'] = soup.find(id="bylineInfo").getText().strip()

            current_product['feature'] = get_feature(soup)
            current_product['description'] = get_description(soup)
            current_product['price'] = get_price(soup)
            current_product['dimension'] = get_dimension(soup)
            current_product['images'] = get_images(soup)
            current_product['attributes'] = get_attr(soup)
            current_product['categories'] = get_categories(soup)
            current_product['rating'] = get_rating(soup)
            current_product['similar'] = get_similar_items(soup)

            # print(json.dumps(current_product, indent=4, sort_keys=False))
            data.append(current_product)
            return current_product

    except Exception as e:
        print("Exception on " + asin + ": ")
        print(e)
        return None


# def solve():
#     asins = [
#         "B074H48L3X",
#         "B073XVPX83",
#         "B004CNH98C",
#         "B077Y3QTTS",
#         "B00BTD9QDO"
#     ]
#     for asin in asins:
#         product = parse(asin);
#         if product is not None:
#             data.append(product)
#
#     json_data = json.dumps(data, indent=4, sort_keys=True)
#     print(json_data)


# current_milli_time = lambda: int(round(time.time() * 1000))
# if __name__ == "__main__":
#     starting = current_milli_time()
#     solve()
#     ending = current_milli_time()
#     print(ending - starting)
