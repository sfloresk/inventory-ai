"""
   Copyright 2023 Amazon.com, Inc. or its affiliates. All Rights Reserved.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import base64
import json
import boto3
import os
import logging
import sys
   
# Setup logging
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(stdout_handler)

## Init clients
bedrock = boto3.client("bedrock-runtime", 'us-east-1')

def lambda_handler(event, context):
    #logger.info(event)
    request_json = json.loads(event['body'])
    if "image_base64" not in request_json.keys():
        return {'statusCode':400}
    
    claude_request_body={
        'system': "Your task is take a food product picture and convert it into a well-organized JSON output. If the picture is not food, reply with an error message. Only identify the brand and name of the product",
        'messages': [{
            'role': 'user', 
            'content': [{
                'type': 'image', 
                'source': {
                        'type':'base64',
                        'media_type':'image/jpeg',
                        'data': request_json['image_base64']
                    }
                }]
            }], 
            'anthropic_version': 'bedrock-2023-05-31', 
            'max_tokens': 2000, 
            'temperature': 0, 
            'top_k': 250, 
            'top_p': 0.999, 
            'stop_sequences': ['\n\nHuman:']
        }
    logger.info(f"Sending message")
    response = bedrock.invoke_model(
        body=json.dumps(claude_request_body), 
        modelId='anthropic.claude-3-sonnet-20240229-v1:0')
    logger.info(f"Model replied - parsing result")
    response_body = json.loads(response.get('body').read())
    result = response_body['content'][0]['text']
    logger.info(f"Result: {result}")
    return {
        'statusCode':200,
        "isBase64Encoded":False,
        "headers": {"content-type":"application/json", "access-control-allow-origin":"*"},
        "body":f"{result}"
        }