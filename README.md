<!--
title: 'ec2-timeout'
description: 'This serverless project runs every 15 minutes and stops ec2s that have been idle longer then ec2-timeout-minutes specified tag value'
layout: Doc
framework: v3
platform: AWS
language: python
priority: 2
authorLink: 'https://github.com/spencer-dawson'
authorName: 'Spencer Dawson'
authorAvatar: 'https://avatars.githubusercontent.com/u/1687388?v=4'
-->


# Serverless Framework ec2-timeout

This Serverless project deploys a lambda function that shuts down idle instances(sub 10% max cpu utilization) after a timeout value specified in that ec2's ec2-timeout-minutes tag. The deployment of this lambda with serverless framework also schedules the lambda to run every 15 minutes. The practical value of this tool is as insurance to prevent accidentally leaving expensive ec2 instances running idle.

I chose serverless, lambda, boto3, and cloudwatch for this implementation mostly for practice reasons and because I may fork this later to add more functionality like memmory usage checking(currently relies only on CPU), network usage checking, slack notification integration, or an api to reboot stopped instances.

Alternative ways to implement this would be with autoscaling rules or cloudwatch alarm actions. Ostensibly those methods would be more efficient, but this method could be more easily ported to work with other cloud providers.

## Usage

### Development Environment Notes
Assumes you have an AWS account, npm 18, node, and serverless installed

### Deployment

With a propper environment setup you can deploy the project with the following command.

```
$ serverless deploy
```

This defaults to deploying in us-west-2. You can deploy to other regions with the --region argument

After running deploy, you should see output similar to:

```bash
Deploying ec2-timeout to stage dev (us-west-2)

✔ Service deployed to stack ec2-timeout-dev (112s)

functions:
  ec2-timeout: ec2-timeout-dev-ec2-timeout (1.5 kB)
```

### Invocation

After successful deployment, you can invoke the deployed function by using the following command:

```bash
serverless invoke --function ec2-timeout
```

Which should result in response similar to the following:

```json
{
    "statusCode": 200,
    "body": "{\"message\": \"ec2-timeout ran succesfully successfully!\", \"input\": {}}"
}
```

### Local development

You can invoke your function locally by using the following command:

```bash
serverless invoke local --function ec2-timeout
```

Which should result in response similar to the following:

```json
{
    "statusCode": 200,
    "body": "{\"message\": \"ec2-timeout ran succesfully successfully!\", \"input\": {}}"
}
```
