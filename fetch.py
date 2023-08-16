import requests
import json
import sys

import time

from tqdm import tqdm

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def fetchSingleUserSubmissions(username, epoch):
    targetURL = "https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user={}&from_second={}".format(username, str(epoch))
    response = requests.get(targetURL)
    time.sleep(0.5) # 降低API服务器压力
    if response.ok:
        return True, json.loads(response.text)
    return False, []

def fetchMultipleUsersSubmissions(usernames, epoch):
    ret = {}
    for user in tqdm(usernames):
        _, ret[user] = fetchSingleUserSubmissions(user, epoch)
    return ret

staticContestInfo = []

def fetchContestInfo():
    global staticContestInfo

    if len(staticContestInfo) == 0:
        eprint("Fetching Contest Info...", end='')
        targetURL = "https://kenkoooo.com/atcoder/resources/contests.json"
        response = requests.get(targetURL)

        if response.ok:
            staticContestInfo = json.loads(response.text)
            eprint("\tDone.")
    
    if len(staticContestInfo) == 0:
        return False, []
    return True, staticContestInfo

staticContestProblemInfo = []

def fetchProblemIdFromContest():
    global staticContestProblemInfo
    if len(staticContestProblemInfo) == 0:
        eprint("Fetching Problem Info...", end='')
        targetURL = "https://kenkoooo.com/atcoder/resources/contest-problem.json"
        response = requests.get(targetURL)
        if response.ok:
            staticContestProblemInfo = json.loads(response.text)
            eprint("\tDone.")
    
    if len(staticContestProblemInfo) == 0:
        eprint('Error: Failed to fetch problem ids.')
    
    return staticContestProblemInfo
    
