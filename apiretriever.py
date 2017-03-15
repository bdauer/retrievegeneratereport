import requests
from siteretriever import ListingsRetriever, SiteRetriever
from secure import PRIVATE_SETTINGS


def post_listings(url, listings):
    """
    Post a list of sites to an API.
    """
    with requests.Session() as s:
        payload = {"sites": listings }
        response = s.post(url, data=payload)
        return response


if __name__ == "__main__":

    lr = ListingsRetriever()
    listings = lr.get_listings()

    post_url = PRIVATE_SETTINGS["POST_SITES_LIST_URL"]
    response = post_listings(post_url, listings)
    print(response)
