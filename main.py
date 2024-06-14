import json

def handler(event, context):
 
    # Run the Scrapy spider
    import subprocess

    subprocess.run(["scrapy", "crawl", "webspider", '-O /tmp/result.jsonl'])

    #Prepare the response_body
    with open('/tmp/result.jsonl') as f:
        data = [json.loads(line) for line in f]
        
    #Prepare the http_response
    http_resp = {}
    http_resp['statusCode'] = 200
    http_resp['headers'] = {
        'Content-Type': 'application/json'
    }
    http_resp['body'] = {
        'count': len(data),
        'conferences': data
        }

    return http_resp
    
    