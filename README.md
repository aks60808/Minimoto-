# minimoto
## Background
Animoto is a web service producing videos from photos, video clips and music. The service is quite well-known as one of Amazon Web Services's (AWS) cloud computing success stories showing the power of scaling infrastructure.

They had 25,000 members on Monday, 50,000 on Tuesday, and 250,000 on Thursday. Their EC2 usage grew as well. For the last month or so they had been using between 50 and 100 instances. On Tuesday their usage peaked at around 400, Wednesday it was 900, and then 3400 instances as of Friday morning.
## Introduction
Minimoto is a low-budget start-up similar as Animoto hosting on AWS offering a transcoding web service converting a series of images into an MP4 video.

## Setup
All the AWS resources (EC2 instances, SQS queue, S3 buckets, AMIs, security groups, etc.) needed to run a solution must be created and initialised using a minimoto_setup program. The usage of the program is as follows (with sample output):
```
$ ./minimoto_setup keyfile aws_access_key_id aws_secret_access_key aws_session_token
```
