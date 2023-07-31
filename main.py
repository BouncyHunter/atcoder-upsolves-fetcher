from prettytable import PrettyTable
import fetch


def getContestDuration(contestId):
    ok, contestInfo = fetch.fetchContestInfo()
    for contest in contestInfo:
        if contest['id'] == contestId:
            return contest['start_epoch_second'], contest['duration_second']
    return -1, -1

def getSubmissionsAt(usernames, contestId):
    startTime, duration = getContestDuration(contestId)
    if startTime < 0:
        print("Error: contest {} not found.".format(contestId))
        return {}
    raw = fetch.fetchMultipleUsersSubmissions(usernames, startTime)
    ret = {}
    for user, submissionList in raw.items():
        temp = []
        for submission in submissionList:
            if submission['contest_id'] == contestId:
                temp.append(submission)
        ret[user] = temp
    return ret

def getProblemIdToIndex(contestId):
    problems = fetch.fetchProblemIdFromContest()
    ret = {}
    for problem in problems:
        if problem['contest_id'] == contestId:
            ret[problem['problem_id']] = problem['problem_index']
    return ret

contestId = input()
users = list(input().split())

result = getSubmissionsAt(users, contestId)
problemIndex = getProblemIdToIndex(contestId)

resultTable = PrettyTable(['User'] + list(problemIndex.values()))
resultTable.align['User'] = 'l'

for user, submissions in result.items():
    ranklist = {}
    for problemId, index in problemIndex.items():
        ranklist[index] = 0
    
    for submission in submissions:
        if ranklist[problemIndex[submission['problem_id']]] <= 0:
            ranklist[problemIndex[submission['problem_id']]] -= 1
            if submission['result'] == 'AC':
                ranklist[problemIndex[submission['problem_id']]] *= -1
    
    resultRow = [user]
    for index, stat in ranklist.items():
        token = ('-' if stat <= 0 else '+') + str(-stat if stat <= 0 else stat-1)
        if token.endswith('0'):
            token = token[:-1]
        if token[0] == '+':
            token = '\033[32m' + token + '\033[0m'
        resultRow.append(token)
    resultTable.add_row(resultRow)

print(resultTable)