# AWS Lambda GitLab Issues manager
This program supports you to manage issues on GitLab.

# Execute
There are 2 patterns.

1. Installs AWS Lambda and invokes it.
2. Execute on your local.

# Prepare
Sets following contents in serverless.yml

| No | Name | Contents |
| ---: | :--- | :--- |
|1|PERSONAL_ACCESS_TOKEN|Personal Access Token generated in GitLab|
|2|TARGET_URL|GitLab issues URL|
|3|MILE_STONE|Milestone (optional)|


## For AWS Lambda

```sh
$ sls deploy
```

After that you can install API Gateway or execute Lambda API on AWS Console.

## For executing on your local

No need any special environment, needs just Python 3 execute environment.

With sls command, below.

```sh
$ sls invoke local -f issues_manager
```



