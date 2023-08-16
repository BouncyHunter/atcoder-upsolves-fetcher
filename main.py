from prettytable import PrettyTable
import fetch

printArgs = []

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

def getSingleContestInfo(contestId, users):
    result = getSubmissionsAt(users, contestId)
    problemIndex = getProblemIdToIndex(contestId)

    resultTable = PrettyTable(['User', 'Solved'] + list(problemIndex.values()))
    resultTable.align['User'] = 'l'

    solveCount = {}

    for user, submissions in result.items():
        ranklist = {}
        for problemId, index in problemIndex.items():
            ranklist[index] = 0
        
        for submission in submissions:
            if ranklist[problemIndex[submission['problem_id']]] <= 0:
                ranklist[problemIndex[submission['problem_id']]] -= 1
                if submission['result'] == 'AC':
                    ranklist[problemIndex[submission['problem_id']]] *= -1
        
        resultRow = [user, 0]
        for index, stat in ranklist.items():
            token = ('-' if stat <= 0 else '+') + str(-stat if stat <= 0 else stat-1)
            if token == '+0' or token == '-0':
                token = token[:-1]
            if token[0] == '+':
                if 'color' in printArgs:
                    token = '\033[32m' + token + '\033[0m'
                resultRow[1] += 1
            resultRow.append(token)
        resultTable.add_row(resultRow)
        solveCount[resultRow[0]] = resultRow[1]

    return solveCount, resultTable

def takeSecond(elem):
    return elem[1]

def formatPrint(table):
    print(table.get_string(title=id, sortby="Solved", reversesort=True)) if 'html' not in printArgs else print(table.get_html_string(title=id, sortby="Solved", reversesort=True))

if __name__ == '__main__':
    printArgs = list(input().split())
    contestIds = list(input().split())
    users = list(input().split())
    if len(contestIds) == 1:
        data, table = getSingleContestInfo(contestIds[0], users)
        formatPrint(table)
    else:
        overallSolves = {}
        for user in users:
            overallSolves[user] = 0
        
        for id in contestIds:
            data, table = getSingleContestInfo(id, users)
            formatPrint(table)
            for user, solveCount in data.items():
                overallSolves[user] += solveCount
        
        overallTable = PrettyTable(['User', 'Solved'])
        sortedList = []

        for user, solves in overallSolves.items():
            sortedList.append((user, solves))
        sortedList.sort(key=takeSecond, reverse=True)

        for user, solves in sortedList:
            overallTable.add_row([user, solves])
        
        print(overallTable) if 'html' not in printArgs else print(overallTable.get_html_string())