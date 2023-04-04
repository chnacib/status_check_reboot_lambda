import json
import boto3

ec2 = boto3.client('ec2')
waiter = ec2.get_waiter('instance_stopped')


def lambda_handler(event, context):
    response = ec2.describe_instances()

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_id = instance.get('InstanceId')
            response = ec2.describe_instance_status(InstanceIds=[instance_id])
            try:
                status_check = response['InstanceStatuses'][0]['InstanceStatus']['Details'][0].get('Status')
                if status_check == "failed":
                    ec2.stop_instances(InstanceIds=[instance_id])
                    waiter.wait(InstanceIds=[instance_id])
                    print(f'{instance_id} Stopped')
                    ec2.start_instances(InstanceIds=[instance_id])
                    print(f'{instance_id} Started')              
            except:
                pass
