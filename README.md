# Repo Owners Notifier
A simple python3 script to send an email to owners specified in an OWNERS file
places in the repository subdirectories.

# How to use it?
Add a pipelines step in your projects `bitbucket-pipelines.yml` calling
`python /pipelines-notify/pipelines_notify.py`. Like so:

```
    - step:
        name: Pipelines notifier
        image: saxonj/pipelines-notify:develop
        script:
        - python /pipelines-notify/pipelines_notify.py
```

The script needs the following environment variables to be set in the pipeline:
* *API_USERNAME* - The username of a bitbucket user with permissions to view/edit
  pull requests in your project.
* *API_APP_PASSWORD* - An app password to authenticate with. It's best to
  restrict the permissions on this app password.
