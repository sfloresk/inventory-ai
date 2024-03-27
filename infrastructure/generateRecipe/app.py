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
import json
import boto3
import random
import logging
import sys
from collections import defaultdict
from xml.etree import cElementTree as ET


# Setup logging
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(stdout_handler)

## Init clients
bedrock_us_east_1 = boto3.client("bedrock-runtime", 'us-east-1')




def etree_to_dict(t):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k: v[0] if len(v) == 1 else v
                     for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v)
                        for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d

def lambda_handler(event, context):

    logger.info(event)
    request_json = json.loads(event['body'])
    if "user_dish_context" not in request_json.keys():
        return {'statusCode':400}

    inputs = {"user_dish_context": request_json['user_dish_context']}

    # Ask claude to create a recipe
    claude_request_body= {
        'system': '''Your task is take a dish description, menu, ingredients or recipe and generate a new recipe with the same ingredients. Return a well formatted XML output using the following schema: <output> <name></name><image_description></image_description><recipe></recipe><ingredient_list><ingredient></ingredient></ingredient_list></output> ''',
        'messages': [{
            'role': 'user', 
            'content': [{
                'type': 'text', 
                'text': inputs['user_dish_context']
                }]
            }], 
            'anthropic_version': 'bedrock-2023-05-31', 
            'max_tokens': 2000, 
            'temperature': 1, 
            'top_k': 250, 
            'top_p': 0.999, 
            'stop_sequences': ['\n\nHuman:','</output>']
        }
    logger.info(f"Sending message")
    response = bedrock_us_east_1.invoke_model(
        body=json.dumps(claude_request_body), 
        modelId='anthropic.claude-3-sonnet-20240229-v1:0')
    logger.info(f"Model replied - parsing result")
    response_body = json.loads(response.get('body').read())
    logger.info(f"Claude generated description and ingredients: {response_body}")
    print(response_body['content'][0]['text'].split('<output>')[1])
    claude_xml_result = ET.XML(f"<output>{response_body['content'][0]['text'].split('<output>')[1]}</output>")
    claude_result = etree_to_dict(claude_xml_result)
    
    # Generating an image with titan
    
    titan_image_request_body={'textToImageParams': {'text': claude_result['output']['image_description']}, 'taskType': 'TEXT_IMAGE', 
                            'imageGenerationConfig': {'cfgScale': 8, 'seed': random.randrange(2147483646), 'width': 512, 'height': 512, 'numberOfImages': 1}}
    response = bedrock_us_east_1.invoke_model(
        body=json.dumps(titan_image_request_body), 
        modelId='amazon.titan-image-generator-v1', 
        accept='*/*',
        contentType="application/json")
    logger.info(f"Model replied - processing results")
    response_body = json.loads(response.get('body').read())
    if response_body['error'] is not None:
        lambda_response_body = json.dumps({
            'error': response_body['error']
        })  
        return {
            'statusCode':500,
            "isBase64Encoded":False,
            "headers": {"content-type":"application/json", "access-control-allow-origin":"*"},
            "body":f"{lambda_response_body}"
        }
    

    lambda_response_body = json.dumps({
        'image':response_body['images'][0],
        'ingredients':claude_result['output']['ingredient_list']['ingredient'],
        'recipe':claude_result['output']['recipe'],
        'name':claude_result['output']['name']
    })
        
    return {
        'statusCode':200,
        "isBase64Encoded":False,
        "headers": {"content-type":"application/json", "access-control-allow-origin":"*"},
        "body":f"{lambda_response_body}"
        }
    