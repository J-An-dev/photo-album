import boto3
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import json
import requests

def build_response(code, body):
    return {
        'statusCode': code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': body
    }


def lambda_handler(event, context):
    print(event)
    
    # Auth
    region = 'us-east-1'
    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

    # From queue body fetch keywords
    keywords_dic = event
    # keywords_dic = json.loads(keywords_body)
    print(keywords_dic)
    
    # Search by keywords
    photo_list = []
    headers = {"Content-Type": "application/json"}
    for key, value in keywords_dic.items():
        if value != None:
            es_url = 'https://vpc-photo-album-demo-boli5szfzjsw6ibw6yil7idcbe.us-east-1.es.amazonaws.com/photos/_search?q=' + value
            response = requests.get(es_url, headers=headers, auth=awsauth)
            data = response.json()
            for res in data["hits"]["hits"]:
                photo_name = str(res["_source"]["objectKey"])
                photo_url = 'https://photo-album-demo.s3.amazonaws.com/' + photo_name
                if photo_url not in photo_list:
                    photo_list.append(photo_url)
    print(photo_list)
    
    if photo_list:
        return build_response(200, photo_list)
    else:
        return build_response(200, "Can not find the photos you want.")
