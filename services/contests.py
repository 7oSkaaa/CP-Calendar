from datetime import datetime
import requests
import os
from dotenv import load_dotenv
from helpers.Colors import bcolors

load_dotenv()

Sites = [
    {'platfrom': 'leetcode', 'api_url': 'https://kontests.net/api/v1/leet_code'},
    {'platfrom': 'codeforces', 'api_url': 'https://kontests.net/api/v1/codeforces'},
    {'platfrom': 'atcoder', 'api_url': 'https://kontests.net/api/v1/at_coder'},
    {'platfrom': 'codechef', 'api_url': 'https://kontests.net/api/v1/code_chef'},
    {'platfrom': 'hackerrank', 'api_url': 'https://kontests.net/api/v1/hacker_rank'},
    {'platfrom': 'kickstart', 'api_url': 'https://kontests.net/api/v1/kick_start'}
]

colors = {
    'leetcode': bcolors.gold,
    'codeforces': bcolors.blue,
    'atcoder': bcolors.white,
    'hackerrank': bcolors.green,
    'kickstart': bcolors.red,
    'codechef': bcolors.brown,
}


def convert_time(contest):
    contest['start_time'] = contest['start_time'].replace(' ', 'T')
    contest['start_time'] = contest['start_time'].replace('TUTC', '.000Z')
    contest['end_time'] = contest['end_time'].replace(' ', 'T')
    contest['end_time'] = contest['end_time'].replace('TUTC', '.000Z')
    return contest


def make_contest_id(contests, platform):
    for contest in contests:
        contest['ID'] = platform + contest['url'].split('/')[-1].lower()
        if len(contest['duration']) > 5:
            contest['end_time'] = contest['start_time']


def get_contests_from_api(url):
    try:
        req = requests.get(url, timeout=2)
        return req
    except requests.exceptions.Timeout:
        return get_contests_from_api(url)    


def get_contests():
    contests = []
    for site in Sites:
        site_contest = get_contests_from_api(site['api_url']).json()
        make_contest_id(site_contest, site['platfrom'])
        if os.getenv(site['platfrom']).lower() != 'true':
            continue
        print(f"{colors[site['platfrom']]}Contests from {site['platfrom']} fetched successfully 💯{bcolors.reset}")
        for contest in site_contest:
            contest = convert_time(contest)
            contests.append(contest)
    return contests