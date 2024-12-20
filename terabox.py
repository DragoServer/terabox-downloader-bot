import re
from pprint import pp
from urllib.parse import parse_qs, urlparse

import requests

from tools import get_formatted_size


def check_url_patterns(url):
    patterns = [
        r"ww\.mirrobox\.com",
        r"www\.nephobox\.com",
        r"freeterabox\.com",
        r"www\.freeterabox\.com",
        r"1024tera\.com",
        r"www\.1024tera\.com",
        r"4funbox\.co",
        r"1024terabox\.com",
        r"www\.1024terabox\.com",
        r"www\.4funbox\.com",
        r"mirrobox\.com",
        r"nephobox\.com",
        r"terabox\.app",
        r"terabox\.com",
        r"www\.terabox\.ap",
        r"www\.terabox\.com",
        r"www\.1024tera\.co",
        r"www\.momerybox\.com",
        r"teraboxapp\.com",
        r"momerybox\.com",
        r"tibibox\.com",
        r"www\.tibibox\.com",
        r"www\.teraboxapp\.com",
        r"www\.funpavo\.com",
        r"www\.teraboxshare\.com",
        r"www\.terafileshare\.com",
        r"terafileshare\.com",
        r"www\.teraboxlink\.com",
        r"teraboxshare\.com",
        r"www\.teraboxlink\.com",
        r"teraboxshare\.com",
        r"teraboxapp\.xyz",
        r"www\.teraboxapp\.xyz",
        r"teraboxlink\.com",
        r"terasharelink\.com",
        r"www\.terasharelink\.com",
        r"funpavo\.com",
    ]

    for pattern in patterns:
        if re.search(pattern, url):
            return True

    return False


def get_urls_from_string(string: str) -> list[str]:
    """
    Extracts URLs from a given string.

    Args:
        string (str): The input string from which to extract URLs.

    Returns:
        list[str]: A list of URLs extracted from the input string. If no URLs are found, an empty list is returned.
    """
    pattern = r"(https?://\S+)"
    urls = re.findall(pattern, string)
    urls = [url for url in urls if check_url_patterns(url)]
    if not urls:
        return []
    return urls[0]


def find_between(data: str, first: str, last: str) -> str | None:
    """
    Searches for the first occurrence of the `first` string in `data`,
    and returns the text between the two strings.

    Args:
        data (str): The input string.
        first (str): The first string to search for.
        last (str): The last string to search for.

    Returns:
        str | None: The text between the two strings, or None if the
            `first` string was not found in `data`.
    """
    try:
        start = data.index(first) + len(first)
        end = data.index(last, start)
        return data[start:end]
    except ValueError:
        return None


def extract_surl_from_url(url: str) -> str | None:
    """
    Extracts the surl parameter from a given URL.

    Args:
        url (str): The URL from which to extract the surl parameter.

    Returns:
        str: The surl parameter, or False if the parameter could not be found.
    """
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    surl = query_params.get("surl", [])

    if surl:
        return surl[0]
    else:
        return False

def get_data(url: str):
    r = requests.Session()
    headersList = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
        "Connection": "keep-alive",
        "Cookie": "TSID=pUt9K27Yeuqv9CslGlNQNPxzQYgJoRLL; browserid=J3sH4Ue97lNR9YjmcBJMjndE6CJOlJ_tAbxp7l0LR_-knQAWy4QOultORag=; lang=en; __bid_n=190a842d4d29e758004207; csrfToken=4bl8zhHwApiHdTG7B3FEOD5s; PANWEB=1; ndus=YfeaA3pteHuiNdFqXZT22UGKbwZruG7AhLriNU1H; ndut_fmt=67CA9B854E436314998352C0EE88F2A5374FF6C4AE780B9D3D44D0B1B5A08EDB",
        "DNT": "1",
        "Host": "www.terabox1024.com",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    payload = ""

    response = r.get(url, data=payload, headers=headersList)
    response = r.get(response.url, data=payload, headers=headersList)
    default_thumbnail = find_between(response.text, 'og:image" content="', '"')
    logid = find_between(response.text, "dp-logid=", "&")
    jsToken = find_between(response.text, "fn%28%22", "%22%29")
    bdstoken = find_between(response.text, 'bdstoken":"', '"')
    shorturl = extract_surl_from_url(response.url)
    if not shorturl:
        return False

    reqUrl = f"https://www.terabox1024.com/share/list?app_id=250528&web=1&channel=dubox&jsToken={jsToken}&page=1&num=20&by=name&order=asc&site_referer=&shorturl={shorturl}&root=1"

    headersList = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
        "Connection": "keep-alive",
        "Cookie": "TSID=pUt9K27Yeuqv9CslGlNQNPxzQYgJoRLL; browserid=J3sH4Ue97lNR9YjmcBJMjndE6CJOlJ_tAbxp7l0LR_-knQAWy4QOultORag=; lang=en; __bid_n=190a842d4d29e758004207; csrfToken=4bl8zhHwApiHdTG7B3FEOD5s; PANWEB=1; ndus=YfeaA3pteHuiNdFqXZT22UGKbwZruG7AhLriNU1H; ndut_fmt=67CA9B854E436314998352C0EE88F2A5374FF6C4AE780B9D3D44D0B1B5A08EDB",
        "DNT": "1",
        "Host": "www.terabox1024.com",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    payload = ""
    response = r.get(
        reqUrl,
        data=payload,
        headers=headersList,
    )
    if not response.status_code == 200:
        return False
    r_j = response.json()
    if r_j["errno"]:
        return False
    if "list" not in r_j and not r_j["list"]:
        return False
    list = r_j.get("list", [])[0]
    response = r.head(r_j["list"][0]["dlink"], headers=headersList)
    #print(list)

    direct_link = response.headers.get("location")
    data = {
        "file_name": list.get("server_filename"),
        "link": list.get("dlink"),
        "direct_link": direct_link,
        "thumb": list.get("thumbs", {}).get("url3") or default_thumbnail,
        "size": get_formatted_size(int(list["size"])),
        "sizebytes": int(list["size"]),
    }

    return data
