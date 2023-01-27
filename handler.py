import json
import boto3
import logging
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# get list of ec2 instances with tag key: ec2-timeout-minutes
def get_ec2_timeout_instances():
    ec2 = boto3.resource('ec2')
    instances = ec2.instances.filter(
        Filters=[{'Name': 'tag:ec2-timeout-minutes'}])
    return instances

#pull out the tag value for the specified tag key
def get_ec2_tag_value(instance, tag_key):
    for tag in instance.tags:
        if tag['Key'] == tag_key:
            return tag['Value']
    return None

def ec2_cpu_is_idle(instance, idle_minutes):
    # check if instance is idle
    # if idle for idle_minutes, return true
    # otherwise return false
    cloudwatch = boto3.client('cloudwatch')
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': instance.id
            },
        ],
        StartTime=datetime.utcnow() - timedelta(minutes=idle_minutes),
        EndTime=datetime.utcnow(),
        Period=60*idle_minutes,
        Statistics=[
            'Maximum',
        ],
        Unit='Percent'
    )
    max_cpu = response['Datapoints'][0]['Maximum']
    if max_cpu < 10:# 10% cpu usage
        return True
    return false

# iterate through instances and stop them if they are idle longer than timeout_minutes
def stop_ec2_idle_instances():
    instances = get_ec2_timeout_instances()
    for instance in instances:
        timeout_minutes = get_ec2_tag_value(instance, 'ec2-timeout-minutes')
        if timeout_minutes is not None:
            timeout_minutes = int(timeout_minutes)
            if ec2_cpu_is_idle(instance, timeout_minutes):
                logger.info("Stopping idle instance ec2: " + instance.id)
                instance.stop()
            else:
                logger.debug("Instance ec2 is not idle: "+ instance.id)
        else:
            logger.debug("Instance ec2 does not have ec2-timeout-minutes tag: " + instance.id)

# lambda handler
def ec2_timeout_handler(event, context):
    stop_ec2_idle_instances()
    body = {
        "message": "ec2-timeout ran succesfully successfully!",
        "input": event,
    }

    return {"statusCode": 200, "body": json.dumps(body)}
