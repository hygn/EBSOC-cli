import sys
import json
import requests
platform = sys.platform
#authToken ='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJPbmxpbmUgQ2xhc3MiLCJtZW1iZXJOYW1lIjoi7J6l7Iuc7JiBIiwibWVtYmVyU2Nob29sQ29kZSI6IkgwOTE1OCIsImV4cCI6MTYxNTA4MjAwNiwiaWF0IjoxNjE0ODIyODA2LCJtZW1iZXJJZCI6ImthQDEyNjgwOTk3In0.3xFHhJbJdFRkVKTW44HNVWYmUX7JngH3u-jdLUt-iBM'
userAgent = f'EBSErrorSolver(AKA.Etiquette Injector)/0.1 ({platform};) Python Requests'
def classList(cookies,AuthToken):
    headers = {'User-Agent':userAgent,
               'X-AUTH-TOKEN':AuthToken,
               'Cookie':cookies,
               'Content-Type': 'application/json;charset=UTF-8',
               'Origin' : 'https://cln.ebsoc.co.kr',
               'Referer':'https://cln.ebsoc.co.kr/class'}
    payload = {'schoolAffairsYear':2021,'tabType':'ALL','searchType':'NONE','searchWord':'','orderType':'DESC'}
    data = requests.post('https://cln.ebsoc.co.kr/common_domain/cls/api/v1/mypage/myClassListByTabType/',headers=headers,
                          json=payload).content.decode('utf-8')
    jsonData = json.loads(data)
    return jsonData['data']['list']
def lectureList(cookies,AuthToken,classUrlPath,lessonSeq):
    headers = {'User-Agent':userAgent,
               'X-AUTH-TOKEN':AuthToken,
               'Cookie':cookies}
    data = requests.get(f'https://cln.ebsoc.co.kr/common_domain/lecture/api/v1/{classUrlPath}/lesson/lecture/attend/list/{lessonSeq}',
                        headers=headers).content.decode('utf-8')
    jsonData = json.loads(data)
    return jsonData['data']['list']
def lessonList(cookies,AuthToken,classUrlPath):
    headers = {'User-Agent':userAgent,
               'X-AUTH-TOKEN':AuthToken,
               'Cookie':cookies}
    data = requests.get(f'https://cln.ebsoc.co.kr/common_domain/lecture/api/v1/{classUrlPath}/lesson/list',
                        headers=headers).content.decode('utf-8')
    jsonData = json.loads(data)
    return jsonData['data']['list']
def lectureDetail(cookies,AuthToken,lessonSeq):
    headers = {'User-Agent':userAgent,
               'X-AUTH-TOKEN':AuthToken,
               'Cookie':cookies}
    data = requests.get(f'https://cln.ebsoc.co.kr/common_domain/common/api/v1/lecture/detail/lesson/{lessonSeq}',
                        headers=headers).content.decode('utf-8')
    jsonData = json.loads(data)
    return jsonData['data']
def userDetail(cookies,AuthToken,memberSeq):
    headers = {'User-Agent':userAgent,
               'X-AUTH-TOKEN':AuthToken,
               'Cookie':cookies}
    data = requests.get(f'https://cln.ebsoc.co.kr/auth_domain/auth/api/v1/member/detail/{memberSeq}',
                        headers=headers).content.decode('utf-8')
    jsonData = json.loads(data)
    return jsonData['data']
def createAPICheck(cookies,AuthToken,contentsSeq,contentsTypeCode,lectureSeq,lessonAttSeq,lessonSeq,officeEduCode,schoolCode,lectureLearningSeq):
    headers = {'User-Agent':userAgent,
               'X-AUTH-TOKEN':AuthToken,
               'Cookie':cookies,
               'Content-Type': 'application/json;charset=UTF-8'}
    payload = {'contentsSeq':contentsSeq,
               'contentsTypeCode':contentsTypeCode,
               'lectureSeq':lectureSeq,
               'lessonAttendanceSeq':lessonAttSeq,
               'lessonSeq':lessonSeq,
               'officeEduCode': officeEduCode,
               'schoolCode': schoolCode}
    payload = json.dumps(payload)
    if lectureLearningSeq == None:
        data = requests.post(f'https://cln.ebsoc.co.kr/common_domain/lecture/api/v1/lesson/lecture/attend/',
                             headers=headers,data=payload)
    jsonData = json.loads(data.content.decode('utf-8'))
    try:
        if jsonData['code'] != 'OK' :
            return jsonData['data']
        else:
            return  jsonData
    except KeyError:
        return jsonData
def learnAPI(AuthToken,progress,memberSeq,lectureLearningSeq,key,IV):
    import AEScrypt
    assembledData = AEScrypt.dataAssembly(str(memberSeq),str(lectureLearningSeq),str(progress))
    cryptData = AEScrypt.encrypt(key,IV,assembledData)
    headers = {'User-Agent':userAgent,
               'X-AUTH-TOKEN':AuthToken,
               'Content-Type': 'application/json;charset=UTF-8'}
    payload = {'encriptedProgressRate':cryptData,}
    payload = json.dumps(payload)
    data = requests.post(f'https://cln.ebsoc.co.kr/lecture/api/v1/student/learning/{lectureLearningSeq}/progress',
                         headers=headers,data=payload)
    jsonData = json.loads(data.content.decode('utf-8'))
    return jsonData