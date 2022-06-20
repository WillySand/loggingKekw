from django.shortcuts import render, redirect
from datetime import datetime
import json
import requests
from requests.structures import CaseInsensitiveDict
from .constants import *
from .util import *

def get_all_logs(request):
    url = "https://39827838-5ea5-42af-935c-fed0a5e34deb-es.logit.io/log*/_search/?apikey=d4515982-e9d8-4416-9c3f-81acb7614a16"
    payload = """
        {
            "size":"""+LOGSIZE+""",
            "sort":[{
                "@timestamp":{
                    "order":"desc",
                    "unmapped_type":"boolean"
                }
            }],
            "query":{
                "bool":{
                    "must":[],
                    "filter": [
                        {
                          "match_all": {}
                        }
                    ]
                }
            }
        }"""
    res = requests.post(url=url, data=payload, headers={"content-type":"application/json"})
    log_json = json.loads(res.text)
    logs=[]
    try:
        if (not log_json['timed_out']):
            no_timestamp=0
            for i in log_json['hits']['hits']:
                try:
                    i['_source']['timestamp'] = corrected_datetime(i['_source'].pop('@timestamp'))
                    logs.append((i['_source']))
                except:
                    no_timestamp+=1
                    
            if(no_timestamp>0):
                url = "https://api.logit.io/v2"
                headers = CaseInsensitiveDict()
                headers["ApiKey"] = "55332b15-6d93-47d4-9846-cf4c1aa74b69"
                headers["Content-Type"] = "application/json"
                headers["LogType"] = "warning"
                data = '{"message": "There are '+str(no_timestamp)+' without timestamps","source":"Logging Service","function":"get_all_logs"}'
                resp = requests.post(url, headers=headers, data=data)
            return render(request,'logging.html',{
                'logs': logs,
            })

        else:
            url = "https://api.logit.io/v2"
            headers = CaseInsensitiveDict()
            headers["ApiKey"] = "55332b15-6d93-47d4-9846-cf4c1aa74b69"
            headers["Content-Type"] = "application/json"
            headers["LogType"] = "warning"
            data = '{"message": request to log server timed out,"source":"Logging Service","function":"get_all_logs"}'
            resp = requests.post(url, headers=headers, data=data)
            return redirect("get_all_logs")
            
    except Exception as e:
        url = "https://api.logit.io/v2"
        headers = CaseInsensitiveDict()
        headers["ApiKey"] = "55332b15-6d93-47d4-9846-cf4c1aa74b69"
        headers["Content-Type"] = "application/json"
        headers["LogType"] = "error"
        data = '{"message":"'+str(e)+'","source":"Logging Service","function":"get_all_logs"}'
        resp = requests.post(url, headers=headers, data=data)
        return redirect("get_all_logs")
    
def get_daily_logs(request):
    url = "https://39827838-5ea5-42af-935c-fed0a5e34deb-es.logit.io/log*/_search/?apikey=d4515982-e9d8-4416-9c3f-81acb7614a16"
    today,yesterday = daily_log_dates()
    payload = """
        {
            "size":"""+LOGSIZE+""",
            "sort":[{
                "@timestamp":{
                    "order":"desc",
                    "unmapped_type":"boolean"
                }
            }],
            "query":{
                "bool":{
                    "must":[],
                    "filter": [
                        {
                          "match_all": {}
                        },
                        {
                            "range": {
                                "@timestamp": {
                                    "gte": """+yesterday+""",
                                    "lte": """+today+""",
                                    "format": "strict_date_optional_time"
                                }
                            }
                        }
                    ]
                }
            }
        }"""
    res = requests.post(url=url, data=payload, headers={"content-type":"application/json"})
    log_json = json.loads(res.text)
    logs=[]
    try:
        if (not log_json['timed_out']):
            no_timestamp=0
            for i in log_json['hits']['hits']:
                try:
                    i['_source']['timestamp'] = corrected_datetime(i['_source'].pop('@timestamp'))
                    logs.append((i['_source']))
                except:
                    no_timestamp+=1
            if(no_timestamp>0):
                url = "https://api.logit.io/v2"
                headers = CaseInsensitiveDict()
                headers["ApiKey"] = "55332b15-6d93-47d4-9846-cf4c1aa74b69"
                headers["Content-Type"] = "application/json"
                headers["LogType"] = "warning"
                data = '{"message": "There are '+str(no_timestamp)+' without timestamps","source":"Logging Service","function":"get_daily_logs"}'
                resp = requests.post(url, headers=headers, data=data)
            return render(request,'logging.html',{
                'logs': logs,
            })
        else:
            url = "https://api.logit.io/v2"
            headers = CaseInsensitiveDict()
            headers["ApiKey"] = "55332b15-6d93-47d4-9846-cf4c1aa74b69"
            headers["Content-Type"] = "application/json"
            headers["LogType"] = "warning"
            data = '{"message": request to log server timed out,"source":"Logging Service","function":"get_daily_logs"}'
            resp = requests.post(url, headers=headers, data=data)
            return redirect("get_daily_logs")
            
    except Exception as e:
        url = "https://api.logit.io/v2"
        headers = CaseInsensitiveDict()
        headers["ApiKey"] = "55332b15-6d93-47d4-9846-cf4c1aa74b69"
        headers["Content-Type"] = "application/json"
        headers["LogType"] = "error"
        data = '{"message":"'+str(e)+'","source":"Logging Service","function":"get_daily_logs"}'
        resp = requests.post(url, headers=headers, data=data)
        return redirect("get_daily_logs")

def get_warning_logs(request):
    url = "https://39827838-5ea5-42af-935c-fed0a5e34deb-es.logit.io/log*/_search/?apikey=d4515982-e9d8-4416-9c3f-81acb7614a16"
    payload = """
        {
            "size":"""+LOGSIZE+""",
            "sort":[{
                "@timestamp":{
                    "order":"desc",
                    "unmapped_type":"boolean"
                }
            }],
            "query":{
                "bool":{
                    "must":[],
                    "filter": [
                        {
                          "match_all": {}
                        },
                        {
                            "match_phrase": {
                                "type": "warning"
                            }
                        }
                    ]
                }
            }
        }"""
    res = requests.post(url=url, data=payload, headers={"content-type":"application/json"})
    log_json = json.loads(res.text)
    logs=[]
    try:
        if (not log_json['timed_out']):
            no_timestamp=0
            for i in log_json['hits']['hits']:
                try:
                    i['_source']['timestamp'] = corrected_datetime(i['_source'].pop('@timestamp'))
                    logs.append((i['_source']))
                except:
                    no_timestamp+=1
            if(no_timestamp>0):
                url = "https://api.logit.io/v2"
                headers = CaseInsensitiveDict()
                headers["ApiKey"] = "55332b15-6d93-47d4-9846-cf4c1aa74b69"
                headers["Content-Type"] = "application/json"
                headers["LogType"] = "warning"
                data = '{"message": "There are '+str(no_timestamp)+' without timestamps","source":"Logging Service","function":"get_warning_logs"}'
                resp = requests.post(url, headers=headers, data=data)
            return render(request,'logging.html',{
                'logs': logs,
            })
        else:
            url = "https://api.logit.io/v2"
            headers = CaseInsensitiveDict()
            headers["ApiKey"] = "55332b15-6d93-47d4-9846-cf4c1aa74b69"
            headers["Content-Type"] = "application/json"
            headers["LogType"] = "warning"
            data = '{"message": request to log server timed out,"source":"Logging Service","function":"get_warning_logs"}'
            resp = requests.post(url, headers=headers, data=data)
            return redirect("get_all_logs")
            
    except Exception as e:
        url = "https://api.logit.io/v2"
        headers = CaseInsensitiveDict()
        headers["ApiKey"] = "55332b15-6d93-47d4-9846-cf4c1aa74b69"
        headers["Content-Type"] = "application/json"
        headers["LogType"] = "error"
        data = '{"message":"'+str(e)+'","source":"Logging Service","function":"get_warning_logs"}'
        resp = requests.post(url, headers=headers, data=data)
        return redirect("get_all_logs")

def get_error_logs(request):
    url = "https://39827838-5ea5-42af-935c-fed0a5e34deb-es.logit.io/log*/_search/?apikey=d4515982-e9d8-4416-9c3f-81acb7614a16"
    payload = """
        {
            "size":"""+LOGSIZE+""",
            "sort":[{
                "@timestamp":{
                    "order":"desc",
                    "unmapped_type":"boolean"
                }
            }],
            "query":{
                "bool":{
                    "must":[],
                    "filter": [
                        {
                          "match_all": {}
                        },
                        {
                            "match_phrase": {
                                "type": "error"
                            }
                        }
                    ]
                }
            }
        }"""
    res = requests.post(url=url, data=payload, headers={"content-type":"application/json"})
    log_json = json.loads(res.text)
    logs=[]
    try:
        if (not log_json['timed_out']):
            no_timestamp=0
            for i in log_json['hits']['hits']:
                try:
                    i['_source']['timestamp'] = corrected_datetime(i['_source'].pop('@timestamp'))
                    logs.append((i['_source']))
                except:
                    no_timestamp+=1
            if(no_timestamp > 0):
                url = "https://api.logit.io/v2"
                headers = CaseInsensitiveDict()
                headers["ApiKey"] = "55332b15-6d93-47d4-9846-cf4c1aa74b69"
                headers["Content-Type"] = "application/json"
                headers["LogType"] = "warning"
                data = '{"message": "There are '+str(no_timestamp)+' without timestamps","source":"Logging Service","function":"get_error_logs"}'
                resp = requests.post(url, headers=headers, data=data)
            return render(request,'logging.html',{
                'logs': logs,
            })
        else:
            url = "https://api.logit.io/v2"
            headers = CaseInsensitiveDict()
            headers["ApiKey"] = "55332b15-6d93-47d4-9846-cf4c1aa74b69"
            headers["Content-Type"] = "application/json"
            headers["LogType"] = "warning"
            data = '{"message": request to log server timed out,"source":"Logging Service","function":"get_error_logs"}'
            resp = requests.post(url, headers=headers, data=data)
            return redirect("get_all_logs")
            
    except Exception as e:
        url = "https://api.logit.io/v2"
        headers = CaseInsensitiveDict()
        headers["ApiKey"] = "55332b15-6d93-47d4-9846-cf4c1aa74b69"
        headers["Content-Type"] = "application/json"
        headers["LogType"] = "error"
        data = '{"message":"'+str(e)+'","source":"Logging Service","function":"get_error_logs"}'
        resp = requests.post(url, headers=headers, data=data)
        return redirect("get_all_logs")
    
def get_default_logs(request):
    url = "https://39827838-5ea5-42af-935c-fed0a5e34deb-es.logit.io/log*/_search/?apikey=d4515982-e9d8-4416-9c3f-81acb7614a16"
    payload = """
        {
            "size":"""+LOGSIZE+""",
            "sort":[{
                "@timestamp":{
                    "order":"desc",
                    "unmapped_type":"boolean"
                }
            }],
            "query":{
                "bool":{
                    "must":[],
                    "filter": [
                        {
                          "match_all": {}
                        },
                        {
                            "match_phrase": {
                                "type": "default"
                            }
                        }
                    ]
                }
            }
        }"""
    res = requests.post(url=url, data=payload, headers={"content-type":"application/json"})
    log_json = json.loads(res.text)
    logs=[]
    try:
        if (not log_json['timed_out']):
            no_timestamp=0
            for i in log_json['hits']['hits']:
                try:
                    i['_source']['timestamp'] = corrected_datetime(i['_source'].pop('@timestamp'))
                    logs.append((i['_source']))
                except:
                    no_timestamp+=1
            if(no_timestamp > 0):
                url = "https://api.logit.io/v2"
                headers = CaseInsensitiveDict()
                headers["ApiKey"] = "55332b15-6d93-47d4-9846-cf4c1aa74b69"
                headers["Content-Type"] = "application/json"
                headers["LogType"] = "warning"
                data = '{"message": "There are '+str(no_timestamp)+' without timestamps","source":"Logging Service","function":"get_error_logs"}'
                resp = requests.post(url, headers=headers, data=data)
            return render(request,'logging.html',{
                'logs': logs,
            })
        else:
            url = "https://api.logit.io/v2"
            headers = CaseInsensitiveDict()
            headers["ApiKey"] = "55332b15-6d93-47d4-9846-cf4c1aa74b69"
            headers["Content-Type"] = "application/json"
            headers["LogType"] = "warning"
            data = '{"message": request to log server timed out,"source":"Logging Service","function":"get_error_logs"}'
            resp = requests.post(url, headers=headers, data=data)
            return redirect("get_all_logs")
            
    except Exception as e:
        url = "https://api.logit.io/v2"
        headers = CaseInsensitiveDict()
        headers["ApiKey"] = "55332b15-6d93-47d4-9846-cf4c1aa74b69"
        headers["Content-Type"] = "application/json"
        headers["LogType"] = "error"
        data = '{"message":"'+str(e)+'","source":"Logging Service","function":"get_error_logs"}'
        resp = requests.post(url, headers=headers, data=data)
        return redirect("get_all_logs")
