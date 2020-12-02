import boto3
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import json

def lambda_handler(event, context):
    # Auth
    region = 'us-east-1'
    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

    # Fetch photo info from event
    print(event)
    s3_record = event["Records"][0]["s3"]
    bucket = s3_record["bucket"]["name"]
    image_key = s3_record["object"]["key"]
    print(image_key)
    
    s3 = boto3.client('s3')
    photo_res = s3.get_object(Bucket=bucket, Key=image_key)
    timestamp = photo_res['LastModified'].strftime('%Y-%m-%dT%H:%M:%S')
    photo_b = photo_res["Body"].read()

    # Fetch labels from Rekognition
    rekognition = boto3.client('rekognition')
    labels_res = rekognition.detect_labels(
        # Image={'S3Object': {'Bucket': bucket, 'Name': image_key}}
        Image={
            'Bytes': photo_b
        },
        MinConfidence=90.0
    )["Labels"]

    # Build JSON object
    labels = [label["Name"] for label in labels_res]
    print(labels)
    result = {
        "objectKey": image_key,
        "bucket": bucket,
        "createdTimestamp": timestamp,
        "labels": labels
    }
    result = json.dumps(result)

    # Store JSON object in ES
    host = "vpc-photos-otxykf3zrhb7byol7rz46an7u4.us-east-1.es.amazonaws.com"
    es = Elasticsearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )
    index_res = es.index(index="photos", doc_type="img", body=result)
    print(index_res)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
