#!/usr/bin/env python3
import os
import json
import sys

def upload_image():
    upload = "aws s3 cp ./simple_image s3://au.edu.unsw.transcode.input-bucket/"
    os.system(upload)

def main():
    upload_image()

if __name__ == "__main__":
    main()