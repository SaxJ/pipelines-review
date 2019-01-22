# Bitbucket Pipelines Notifier
A simple python script (all dockerised) to automagically add reviews to a PR
based on the files modified in the PR.

To do this, an `OWNERS` file containing one username per line is placed in a directory.
If any files in that directory or any sub-directories are modified, the usernames in that 
OWNERS file are added to the pull request as reviewers.

# What does it do?
* Add reviewers to PR's based on the files in the diff
* Mark PR's as [WIP] to avoid adding reviewers

# How to use it?
Add a pipelines step in your projects `bitbucket-pipelines.yml` calling
`python /pipelines_notify.py`. Like so:

```
    - step:
        name: Pipelines notifier
        image: saxonj/pipelines-notify:develop
        script:
        - python /pipelines_notify.py
```

The script needs the following environment variables to be set in the pipeline:
* *API_USERNAME* - The username of a bitbucket user with permissions to view/edit
  pull requests in your project.
* *API_APP_PASSWORD* - An app password to authenticate with. It's best to
  restrict the permissions on this app password.
