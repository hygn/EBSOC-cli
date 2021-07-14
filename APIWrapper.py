import sys
import json
import requests
from cfg import readCfg
platform = sys.platform
userAgent = f"EBSErrorSolver(AKA.Etiquette Injector)/0.1 ({platform};) Python Requests"
def classList(cookies,AuthToken,host):
    debug = readCfg()["debug"]
    attempt = readCfg()["attempt"]
    timeout = readCfg()["requestTimeout"]
    headers = {"User-Agent":userAgent,
               "X-AUTH-TOKEN":AuthToken,
               "Cookie":cookies,
               "Content-Type": "application/json;charset=UTF-8",
               "Origin" : "https://"+host+f".ebsoc.co.kr",
               "Referer":"https://"+host+f".ebsoc.co.kr/class"}
    payload = {"schoolAffairsYear":2021,"tabType":"ALL","searchType":"NONE","searchWord":"","orderType":"DESC"}
    for i in range(attempt):
        try:
            data = requests.post("https://"+host+f".ebsoc.co.kr/cls/api/v1/mypage/myClassListByTabType",headers=headers,
                          json=payload,timeout=timeout).content.decode("utf-8")
            break
        except requests.exceptions.ReadTimeout as e:
            if i - 1 == attempt:
                raise e
    if debug == "yes": print(data)
    jsonData = json.loads(data)
    return jsonData["data"]["list"]
def lectureList(cookies,AuthToken,classUrlPath,lessonSeq,host):
    debug = readCfg()["debug"]
    attempt = readCfg()["attempt"]
    timeout = readCfg()["requestTimeout"]
    headers = {"User-Agent":userAgent,
               "X-AUTH-TOKEN":AuthToken,
               "Cookie":cookies}
    for i in range(attempt):
        try:
            data = requests.get(f"https://"+host+f".ebsoc.co.kr/lecture/api/v1/{classUrlPath}/lesson/lecture/attend/list/{lessonSeq}",
                        headers=headers,timeout=timeout).content.decode("utf-8")
            break
        except requests.exceptions.ReadTimeout as e:
            if i - 1 == attempt:
                raise e
    if debug == "yes": print(data)
    jsonData = json.loads(data)
    return jsonData["data"]["list"]
def lessonList(cookies,AuthToken,classUrlPath,host):
    debug = readCfg()["debug"]
    attempt = readCfg()["attempt"]
    timeout = readCfg()["requestTimeout"]
    headers = {"User-Agent":userAgent,
               "X-AUTH-TOKEN":AuthToken,
               "Cookie":cookies}
    for i in range(attempt):
        try:
            data = requests.get(f"https://"+host+f".ebsoc.co.kr/lecture/api/v1/{classUrlPath}/lesson/list?atltStsCd=&orderBy=3&",
                        headers=headers,timeout=timeout)
            break
        except requests.exceptions.ReadTimeout as e:
            if i - 1 == attempt:
                raise e
    if debug == "yes": print(data.content.decode("utf-8"))
    print(data.url)
    jsonData = json.loads(data.content.decode("utf-8"))
    return jsonData["data"]["list"]
def finLessonList(cookies,AuthToken,host):
    debug = readCfg()["debug"]
    attempt = readCfg()["attempt"]
    timeout = readCfg()["requestTimeout"]
    headers = {"User-Agent":userAgent,
               "X-AUTH-TOKEN":AuthToken,
               "Cookie":cookies}
    for i in range(attempt):
        try:
            data = requests.get(f"https://"+host+f".ebsoc.co.kr/lecture/api/v1/student/learning",
                        headers=headers,timeout=timeout).content.decode("utf-8")
            break
        except requests.exceptions.ReadTimeout as e:
            if i - 1 == attempt:
                raise e
    if debug == "yes": print(data)
    jsonData = json.loads(data)
    return jsonData["data"]["list"]
def lectureDetail(cookies,AuthToken,lessonSeq,host):
    debug = readCfg()["debug"]
    attempt = readCfg()["attempt"]
    timeout = readCfg()["requestTimeout"]
    headers = {"User-Agent":userAgent,
               "X-AUTH-TOKEN":AuthToken,
               "Cookie":cookies}
    for i in range(attempt):
        try:
            data = requests.get(f"https://"+host+f".ebsoc.co.kr/common/api/v1/lecture/detail/lesson/{lessonSeq}",
                        headers=headers,timeout=timeout).content.decode("utf-8")
            break
        except requests.exceptions.ReadTimeout as e:
            if i - 1 == attempt:
                raise e
    if debug == "yes": print(data)
    jsonData = json.loads(data)
    return jsonData["data"]
def userDetail(cookies,AuthToken,memberSeq,host):
    debug = readCfg()["debug"]
    attempt = readCfg()["attempt"]
    timeout = readCfg()["requestTimeout"]
    headers = {"User-Agent":userAgent,
               "X-AUTH-TOKEN":AuthToken,
               "Cookie":cookies}
    for i in range(attempt):
        try:
            data = requests.get(f"https://ebsoc.co.kr/auth/api/v1/member/detail/{memberSeq}",
                        headers=headers,timeout=timeout).content.decode("utf-8")
            break
        except requests.exceptions.ReadTimeout as e:
            if i - 1 == attempt:
                raise e
    if debug == "yes": print(data)
    jsonData = json.loads(data)
    return jsonData["data"]
def newFileDownload(cookies,AuthToken,fileId,host):
    debug = readCfg()["debug"]
    headers = {"User-Agent":userAgent,
               "X-AUTH-TOKEN":AuthToken,
               "Cookie":cookies,
               "Content-Type": "application/json;charset=UTF-8"}
    #이걸 또 또 바꾸네
    req = requests.get(f"https://"+host+f".ebsoc.co.kr/common/api/v1/s3new/file/getDownLoadURL?fileId={fileId}",
                   headers=headers).json()
    return req['data']
def createAPICheck(cookies,AuthToken,contentsSeq,contentsTypeCode,lectureSeq,lessonAttSeq,lessonSeq,officeEduCode,schoolCode,lectureLearningSeq,host):
    debug = readCfg()["debug"]
    headers = {"User-Agent":userAgent,
               "X-AUTH-TOKEN":AuthToken,
               "Cookie":cookies.replace("<","")}
    payload = {"contentsSeq":int(contentsSeq),
               "contentsTypeCode":str(contentsTypeCode),
               "lectureSeq":str(lectureSeq),
               "lessonAttendanceSeq":lessonAttSeq,
               "lessonSeq":int(lessonSeq),
               "officeEduCode": str(officeEduCode),
               "schoolCode": str(schoolCode)}
    if lectureLearningSeq == None:
        data = requests.post(f"https://"+host+f".ebsoc.co.kr/lecture/api/v1/lesson/lecture/attend/create",
                             headers=headers,json=payload)
        if debug == "yes": 
            print(f"create: {data.content.decode('utf-8')}")
            print(f"create: {data.headers}")
    else:
        data = ""
    jsonData = json.loads(data.content.decode("utf-8"))
    try:
        if jsonData["code"] != "OK" :
            return jsonData["data"]
        else:
            return jsonData
    except KeyError:
        return jsonData
def learnAPI(AuthToken,progress,memberSeq,lectureLearningSeq,schoolCode,key,IV,host):
    debug = readCfg()["debug"]
    import AEScrypt
    assembledData = AEScrypt.dataAssembly(str(memberSeq),str(lectureLearningSeq),str(progress))
    cryptData = AEScrypt.encrypt(key,IV,assembledData)
    headers = {"User-Agent":userAgent,
               "X-AUTH-TOKEN":AuthToken,
               "Content-Type": "application/json;charset=UTF-8"}
    payload = {"encriptedProgressRate":cryptData,}
    payload = json.dumps(payload)
    data = requests.post(f"https://"+host+f".ebsoc.co.kr/lecture/api/v1/student/learning/{lectureLearningSeq}/{schoolCode}/progress",
                         headers=headers,data=payload)
    if debug == "yes": 
        print(data.content.decode("utf-8"))
        print(assembledData)
        print(cryptData)
    jsonData = json.loads(data.content.decode("utf-8"))
    return jsonData
