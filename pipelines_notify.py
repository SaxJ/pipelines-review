########################################
# Author: Saxon Jensen
########################################

import subprocess
import os
import requests
import sys
from unidiff import PatchSet

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
    print('Changing to clone dir')
    os.chdir(os.environ['BITBUCKET_CLONE_DIR'])

    prId = os.environ['BITBUCKET_PR_ID']
    owner = os.environ['BITBUCKET_REPO_OWNER']
    repoSlug = os.environ['BITBUCKET_REPO_SLUG']
    username = os.environ['API_USERNAME']
    password = os.environ['API_APP_PASSWORD']
    resp = requests.get('https://api.bitbucket.org/2.0/repositories/{}/{}/pullrequests/{}/diff'.format(owner, repoSlug, prId), auth=(username, password))

    print('Git diff')
    print('=============================')
    print(resp.text)
    patches = PatchSet(resp.text)
    filePaths = [p.source_file for p in patches]

    print('File paths')
    print(filePaths)
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
