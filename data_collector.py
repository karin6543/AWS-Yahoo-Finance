from datetime import date
import json
import boto3
import os
import subprocess
import sys
# 

subprocess.check_call([sys.executable, "-m", "pip", "install", "--target", "/tmp", 'yfinance'])
sys.path.append('/tmp')
import yfinance as yf


def lambda_handler(event, context):
    
    stocks=['FB','SHOP', 'BYND', 'NFLX', 'PINS', 'SQ' ,'TTD', 'OKTA' ,'SNAP', 'DDOG']
    

    def get_js(high,low,ts,name):
        return json.dumps({'high':high,'low':low,'ts':str(ts),'name':name})
        
    fh=boto3.client("firehose", "us-east-2")

    
    df=yf.download(tickers='FB SHOP BYND NFLX PINS SQ TTD OKTA SNAP DDOG',
    
    start="2020-05-14", end="2020-05-15",interval = "1m",group_by='tickers')
    
    df2=df.melt(value_vars =stocks,var_name=['Symbol'])
    
    df2=df.unstack().unstack(level=1).reset_index(level=1, drop=False).rename_axis('names').reset_index()
    
    df2['js']=df2.apply(lambda x:get_js(x['High'],x['Low'],x['Datetime'],x['names']),axis=1)

    for i in df2['js'].values:
        fh.put_record(DeliveryStreamName="test-delivery-stream", Record={"Data": i.encode('utf-8')})
    
    
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'Done!Check S3')
    }
