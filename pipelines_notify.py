########################################
# Author: Saxon Jensen
########################################

import subprocess
import os
import requests
import sys
from unidiff import PatchSet

def getFolders(path):
    path = '.' + os.sep + os.path.normpath(path)
    return path.split(os.sep)

def makePath(folders, end):
    return os.sep.join(folders[0:end]) + (os.sep if len(folders[0:end]) else '') + 'OWNERS'

def getEnvironment():
    prId = os.environ['BITBUCKET_PR_ID']
    owner = os.environ['BITBUCKET_REPO_OWNER']
    repoSlug = os.environ['BITBUCKET_REPO_SLUG']
    username = os.environ['API_USERNAME']
    password = os.environ['API_APP_PASSWORD']

    return (prId, owner, repoSlug, username, password)

def makeAPIString():
    (prId, owner, repoSlug, username, password) = getEnvironment()
    return f'https://api.bitbucket.org/2.0/repositories/{owner}/{repoSlug}/pullrequests/{prId}'

def updatePR(toList, author, title, existingReviewers):
    (prId, owner, repoSlug, username, password) = getEnvironment()

    revers = [{'username': x.strip()} for x in toList if author != x.strip()]
    revers.extend(existingReviewers)

    resp = requests.put(makeAPIString(), json={'title': title, 'reviewers': revers}, auth=(username, password), allow_redirects=True)
    print(resp.request.body)
    print('=========')
    print(resp.text)

def inspectPR():
    (prId, owner, repoSlug, username, password) = getEnvironment()
    resp = requests.get(makeAPIString(), auth=(username, password), allow_redirects=True)

    return resp.json()


def main(argv):
    print('Changing to clone dir')
    os.chdir(os.environ['BITBUCKET_CLONE_DIR'])
    existing = inspectPR()
    if '[WIP]' in existing['title']:
        return
    

    (prId, owner, repoSlug, username, password) = getEnvironment()
    resp = requests.get(makeAPIString() + '/diff', auth=(username, password), allow_redirects=True)
    print('DIFF')
    print('========')
    print(resp.text)

    patches = PatchSet.from_string(resp.text)
    filePaths = [p.path for p in patches]

    users = set()
    for path in filePaths:
        folders = getFolders(path)
        print(folders)
        for idx, folder in enumerate(folders):
            ownersFile = makePath(folders, idx)
            print(f'Try {ownersFile}')
            if os.path.exists(ownersFile):
                with open(ownersFile) as f:
                    for line in f:
                        users.add(line)
    print(users)

    existingReviewers = [{'username': x['username']} for x in existing['reviewers']]
    updatePR(list(users), existing['author']['username'], existing['title'], existingReviewers)

if __name__ == "__main__":
   main(sys.argv[1:])
