import boto3
import json

def build_response(code, body):
    return {
        'statusCode': code,
        'headers': {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,HEAD,OPTIONS,POST,PUT",
            "Access-Control-Allow-Headers": "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers"
        },
        'body': body
    }

def lambda_handler(event, context):
    # Trigger Lex and get back keywords
    # content_recieved = "thank you."
    print(event)
    content_recieved = event['q']
    lex = boto3.client('lex-runtime', 'us-east-1', verify=False)
    bot_response = lex.post_text(
        botName='PhotoSearch',
        botAlias='Jarvis',
        userId='8888',
        inputText=content_recieved
    )
    print(bot_response)
    
    if 'slots' in bot_response.keys() and len(bot_response['slots']) > 0:
        keywords = {}
        keywords['keyword_one'] = bot_response['slots']['keywordOne']
        keywords['keyword_two'] = bot_response['slots']['keywordTwo']
        
        return build_response(200, keywords)
        
    else:
        return build_response(200, "Can not understand your query.")
    
    
