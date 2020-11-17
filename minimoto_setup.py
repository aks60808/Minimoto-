#!/usr/bin/env python3
import os
import json
import sys

def create_sqs():
    ### create SQS ###
    create_sqs = "aws sqs create-queue --queue-name cs9243requestqueue.fifo --attributes FifoQueue=true --region us-east-1 > sqs.txt"
    os.system(create_sqs)

def create_S3():
    ### create S3 ###
    create_s3_input = "aws s3api create-bucket --bucket au.edu.unsw.transcode.input-bucket --region us-east-1 "
    os.system(create_s3_input)
    create_s3_output = "aws s3api create-bucket --bucket au.edu.unsw.transcode.output-bucket --region us-east-1"
    os.system(create_s3_output)

def client_instance(keyfile,group_id ):
    ### launch client instance ###
    run_instances = "aws ec2 run-instances --image-id ami-0f82752aa17ff8f5d --count 1 --instance-type t2.micro --key-name "+keyfile+" --security-group-ids "+group_id+" > run_instances.json"
    os.system(run_instances)
    ### get instance id ###
    with open('./run_instances.json') as ri:
        ri_data = json.load(ri)
    instance_id = ri_data["Instances"][0]["InstanceId"]
    ### get instance IPv4 ###
    describe_instances = "aws ec2 describe-instances --instance-ids "+instance_id+" --query 'Reservations[*].Instances[*].PublicIpAddress' --output text > ipv4.txt"
    os.system(describe_instances)
    ip_file = open("./ipv4.txt")
    ipv4 = ip_file.readline().rstrip('\n')
    ### scp transcode script to instance ###
    scp_srcipt = "scp -i "+keyfile+".pem ./minimoto_client.py  ubuntu@"+ipv4+":~/"
    os.system(scp_srcipt)

def service_instance(keyfile, group_id):
    ### aws launch service EC2 instance ###
    run_instances = "aws ec2 run-instances --image-id ami-0f82752aa17ff8f5d --count 1 --instance-type t2.micro --key-name "+keyfile+" --security-group-ids "+group_id+" > run_instances.json"
    os.system(run_instances)
    ### get instance id ###
    with open('./run_instances.json') as ri:
        ri_data = json.load(ri)
    instance_id = ri_data["Instances"][0]["InstanceId"]
    ### get instance IPv4 ###
    describe_instances = "aws ec2 describe-instances --instance-ids "+instance_id+" --query 'Reservations[*].Instances[*].PublicIpAddress' --output text > ipv4.txt"
    os.system(describe_instances)
    ip_file = open("./ipv4.txt")
    ipv4 = ip_file.readline().rstrip('\n')
    ### scp transcode script to instance ###
    scp_srcipt = "scp -i "+keyfile+".pem ./transcode.sh  ubuntu@"+ipv4+":~/"
    os.system(scp_srcipt)
    return ipv4

def create_security_group():
    ### aws create security group ###
    security_group = "aws ec2 create-security-group --group-name my-sg --description \"My security group\" > security_group.json"
    os.system(security_group)
    with open('./security_group.json') as sg:
        sg_data = json.load(sg)

    group_id = sg_data["GroupId"]
    authorize_security_group  = "aws ec2 authorize-security-group-ingress --group-id "+group_id+" --protocol tcp --port 22 --cidr 0.0.0.0/0"
    os.system(authorize_security_group)
    # group_id = "sg-0be3be2208ad4b129"
    return group_id

def aws_configure(argv):
    keyfile = sys.argv[1][:-4]
    aws_access_key_id = sys.argv[2]
    aws_secret_access_key = sys.argv[3]
    aws_session_token = sys.argv[4]

    os.system("echo [default] > ~/.aws/credentials")
    os.system("echo aws_access_key_id="+ aws_access_key_id +" >> ~/.aws/credentials")
    os.system("echo aws_secret_access_key="+ aws_secret_access_key +" >> ~/.aws/credentials")
    os.system("echo aws_session_token="+ aws_session_token +" >> ~/.aws/credentials")
    os.system("echo \"[default]\noutput = json\nregion = us-east-1\" > ~/.aws/config")
    # os.system("cat ~/.aws/credentials")
    return keyfile

def main():
    length = len(sys.argv)
    if length < 5:
        sys.exit("Usage: ./minimoto_setup keyfile aws_access_key_id aws_secret_access_key aws_session_token")

    keyfile = aws_configure(sys.argv)
    group_id = create_security_group()
    service_ip = service_instance(keyfile,group_id)
    client_ip = client_instance(keyfile,group_id)
    create_S3()
    create_sqs()

if __name__ == "__main__":
    main()







