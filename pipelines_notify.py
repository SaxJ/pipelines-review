########################################
# Author: Saxon Jensen
########################################

import subprocess
import os
import requests
import sys

def getFolders(path):
    path = os.path.normpath(path)
    return path.split(os.sep)

def makePath(folders, end):
    lead = '.' + os.sep
    return lead + os.sep.join(folders[0:end]) + (os.sep if len(folders[0:end]) else '') + 'OWNERS'

def updatePR(toList):
    prId = os.environ['BITBUCKET_PR_ID']
    owner = os.environ['BITBUCKET_REPO_OWNER']
    repoSlug = os.environ['BITBUCKET_REPO_SLUG']
    username = os.environ['API_USERNAME']
    password = os.environ['API_APP_PASSWORD']

    revers = [{'username': x} for x in toList]

    requests.put('https://api.bitbucket.org/2.0/repositories/{}/{}/pullrequests/{}'.format(owner, repoSlug, prId), data={'reviewers': revers}, auth=(username, password))


def main(argv):
    os.chdir(os.environ['BITBUCKET_CLONE_DIR'])

    destBranch = os.environ['BITBUCKET_PR_DESTINATION_BRANCH']

    subprocess.run(['git', 'fetch', 'origin', '{}:temp'.format(destBranch)])
    diffResult = subprocess.run(['git', 'diff', '--name-only', 'temp...HEAD'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    filePaths = diffResult.splitlines()

    users = set()
    for path in filePaths:
        folders = getFolders(path)
        for idx, folder in enumerate(folders[0:-1]):
            ownersFile = makePath(folders, idx)
            if os.path.exists(ownersFile):
                with open(ownersFile) as f:
                    for line in f:
                        users.add(line)

    updatePR(list(users))

if __name__ == "__main__":
   main(sys.argv[1:])
