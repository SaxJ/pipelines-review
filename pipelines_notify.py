########################################
# Author: Saxon Jensen
########################################

import subprocess
import os
import requests

def getFolders(path):
    path = os.path.normpath(path)
    return path.split(os.sep)

def makePath(folders, end):
    lead = '.' + os.sep
    return lead + os.sep.join(folders[0:end]) + (os.sep if len(folders[0:end]) else '') + 'OWNERS'

def sendEmails(toList):
    host = os.environ['EMAIL_HOST']
    port = os.environ['EMAIL_PORT']
    password = os.environ['EMAIL_PASSWORD']
    username = os.environ['EMAIL_USERNAME']

    server = smtplib.SMTP(host, port)
    server.startttls()
    server.login(username, password)

    msg = '''
    Files you have ownership of are being modified in a current deployment!
    '''
    server.sendmail(username, toList, msg)
    server.quit()

# WIP
def updatePR(toList):
    prId = os.environ['BITBUCKET_PR_ID']
    owner = os.environ['BITBUCKET_REPO_OWNER']
    repoSlug = os.environ['BITBUCKET_REPO_SLUG']

    revers = [{'username': x} for x in toList]

    requests.put('https://api.bitbucket.org/2.0/repositories/{}/{}/pullrequests/{}'.format(owner, repoSlug, prId), data={'reviewers': revers})


diffResult = subprocess.run(['git', 'diff', '--name-only', 'master..develop'], stdout=subprocess.PIPE).stdout.decode('utf-8')
filePaths = diffResult.splitlines()

emails = set()
for path in filePaths:
    folders = getFolders(path)
    for idx, folder in enumerate(folders[0:-1]):
        ownersFile = makePath(folders, idx)
        if os.path.exists(ownersFile):
            with open(ownersFile) as f:
                for line in f:
                    emails.add(line)

sendEmails(list(emails))
