from datetime import datetime
import requests
import os
from dotenv import load_dotenv

load_dotenv()

#Colors to use
red = '\033[38;5;196m'
green = '\033[38;5;40m'
blue = '\033[34m'
gold = '\033[38;5;220m'
white = '\33[37m'
magenta = '\033[35m'
brown = '\033[38;5;94m'
bold = '\033[01m'
reset = '\033[0m'

Sites = [
    {'platfrom': 'leetcode', 'api_url': 'https://kontests.net/api/v1/leet_code'},
    {'platfrom': 'codeforces', 'api_url': 'https://kontests.net/api/v1/codeforces'},
    {'platfrom': 'atcoder', 'api_url': 'https://kontests.net/api/v1/at_coder'},
    {'platfrom': 'codechef', 'api_url': 'https://kontests.net/api/v1/code_chef'},
    {'platfrom': 'hackerrank', 'api_url': 'https://kontests.net/api/v1/hacker_rank'},
    {'platfrom': 'kickstart', 'api_url': 'https://kontests.net/api/v1/kick_start'}
]

colors = {
    'leetcode': gold,
    'codeforces': blue,
    'atcoder': white,
    'hackerrank': green,
    'kickstart': red,
    'codechef': brown,
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
        print(f"{colors[site['platfrom']]}Contests from {site['platfrom']} fetched successfully 💯{reset}")
        for contest in site_contest:
            contest = convert_time(contest)
            contests.append(contest)
    return contests