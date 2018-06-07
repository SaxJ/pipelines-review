# Repo Owners Notifier
A simple python3 script to send an email to owners specified in an OWNERS file
places in the repository subdirectories.

# How to use it?
I wrote this for bitbucket pipelines originally, but however you want to trigger
this script it should work
* Place the `pipelines_notify.py` script in the root of the git project.
* Ensure `EMAIL_HOST`, `EMAIL_PASSWORD`, `EMAIL_USERNAME`, `EMAIL_PORT` are
  specified.
* Place a file called `OWNERS` in directories within the project that you want
  to specify owners for. OWNERS are inherited from parent directories.
* When a file has been modified, emails will be sent to those in the OWNERS
  files for that directory.
