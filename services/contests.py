import os
import re

import requests
from dotenv import load_dotenv

from helpers.colors import bcolors

load_dotenv()

Sites = [
    {"platform": "leetcode", "api_url": "https://kontests.net/api/v1/leet_code"},
    {"platform": "codeforces", "api_url": "https://kontests.net/api/v1/codeforces"},
    {"platform": "codeforcesGym", "api_url": "https://kontests.net/api/v1/codeforces_gym"},
    {"platform": "atcoder", "api_url": "https://kontests.net/api/v1/at_coder"},
    {"platform": "codechef", "api_url": "https://kontests.net/api/v1/code_chef"},
    {"platform": "topcoder", "api_url": "https://kontests.net/api/v1/top_coder"},
    {"platform": "hackerrank", "api_url": "https://kontests.net/api/v1/hacker_rank"},
]

colors = {
    "leetcode": bcolors.gold,
    "codeforces": bcolors.blue,
    "atcoder": bcolors.white,
    "hackerrank": bcolors.green,
    "kickstart": bcolors.red,
    "codechef": bcolors.brown,
    "topcoder": bcolors.magenta,
    "codeforcesGym": bcolors.cyan
}


def convert_time(contest):
    contest["start_time"] = contest["start_time"].replace(" ", "T")
    contest["start_time"] = contest["start_time"].replace("TUTC", ".000Z")
    contest["end_time"] = contest["end_time"].replace(" ", "T")
    contest["end_time"] = contest["end_time"].replace("TUTC", ".000Z")
    return contest


def make_contest_id(contests, platform):
    for contest in contests:
        if platform == "leetcode":
            contest["ID"] = contest["name"].replace(" ", "").lower()
        else:
            contest["ID"] = platform + contest["url"].split("/")[-1].lower()
        contest["ID"] = re.sub("[wxyz]+", "rep", contest["ID"])
        if len(contest["duration"]) > 5:
            contest["end_time"] = contest["start_time"]


def get_contests_from_api(url):
    try:
        req = requests.get(url, timeout=2)
        return req
    except requests.exceptions.Timeout:
        return get_contests_from_api(url)


def get_contests():
    contests = []
    for site in Sites:
        site_contest = get_contests_from_api(site["api_url"]).json()
        make_contest_id(site_contest, site["platform"])
        if os.getenv(site["platform"]).lower() != "true":
            continue
        print(site)
        print(
            f"{colors[site['platform']]}Contests from {site['platform']} fetched successfully 💯{bcolors.reset}"
        )
        for contest in site_contest:
            contest = convert_time(contest)
            contests.append(contest)
    return contests
