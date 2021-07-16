from application_functions import *
from cfg import *
import APIWrapper
import cookie
import time
import sys
import os
clear()
host = cookie.getHost('')
#https://www.youtube.com/watch?v=f4ZRK8YLmPc
#https://www.youtube.com/watch?v=aGuHixFujHE
#https://youtu.be/TiCEzvE0trc?t=922
#https://www.youtube.com/watch?v=ljmGSQvYeGo
#https://www.youtube.com/watch?v=TyHITBLVrEg
#https://www.youtube.com/watch?v=1QMfcLcH56o
#https://www.youtube.com/watch?v=6iseNlvH2_s
runOpt = None
try:
    if sys.argv[1] == 'all':
        runOpt = 'all'
    elif sys.argv[1] == 'alldoc':
        runOpt = 'alldoc'
except IndexError:
    pass
try:
    os.mkdir('downloads')
except FileExistsError:
    pass
debug = readCfg()['debug']
if debug == 'yes': print(readCfg())
if readCfg()['cfgLock'] != 'yes' and runOpt == None:
    decfg = input('edit config?(y)')
else:
    decfg = 'n'
if decfg == 'y':
    while True:
        printCfg()
        arg = input('cfgname = ')
        if arg == 'exit':
            break
        dat = input('value = ')
        if arg in [item[0] for item in cfgList]:
            editCfg(arg,dat)
        else:
            print('올바른 설정을 입력해주세요')
        input()
        clear()
debug = readCfg()['debug']
attempt = readCfg()['attempt']
print('\033[95mLogging in... \033[0m')
try:
    cookies = cookie.query('')
    if debug == 'yes': print(cookies)
    auth = cookie.getAuth('')
    if debug == 'yes': print(auth)
    memberSeq = cookie.getMembSeq('')
    if debug == 'yes': print(memberSeq)
except:
    print('\033[91mcookie not detected \033[0m')
    cookies = None
try:
    if cookies == None:
        raise KeyError
    try:
        attemptCount = readCfg()['attempt']
    except:
        attemptCount = defaultCfg[5]
    for i in range(attemptCount):
        try:
            cookies = cookie.query('')
            if debug == 'yes': print(cookies)
            auth = cookie.getAuth('')
            if debug == 'yes': print(auth)
            memberSeq = cookie.getMembSeq('')
            if debug == 'yes': print(memberSeq)
            print(f"\033[95mFetching user data\033[0m")
            memberData = APIWrapper.userDetail(cookies,auth,memberSeq,host)
            print('\033[92mLogin successful\033[0m')
            print(f"\033[95mLogged in as {memberData['memberNm']}\033[0m")
            break
        except:
            time.sleep(5)
            if i == readCfg()['loginAttempt']:
                raise
            else:
                pass
except:
    print('\033[91mLogin failed \033[0m')
    print('\033[91mPlease manually input cookie data \033[0m')
    auth = input('access = ')
    host = input('host = ')
    memberSchoolCode = input('memberSchoolCode = ')
    memberSeq = input('memberSeq = ')
    memberTargetCode = input('memberTargetCode = ')
    schoolInfoYn = 'Y'
    WHATAP = input('WHATAP = ')
    cookies = f'access={auth} host={host}, memberSchoolCode={memberSchoolCode}, memberSeq={memberSeq}, '\
        f'memberTargetCode={memberTargetCode}, schoolInfoYn=Y, WHATAP={WHATAP}, '
    try:
        classList = APIWrapper.classList(cookies,auth,host)
        print(f"\033[95mFetching user data\033[0m")
        memberData = APIWrapper.userDetail(cookies,auth,memberSeq,host)
    except:
        print('\033[91mLogin failed \033[0m')
        print('\033[91mAborting... \033[0m')
        input()
        exit()
msgdepth = []
while True:
    if msgdepth == []:
        print(f"\033[95mFetching class list\033[0m")
        classList = APIWrapper.classList(cookies,auth,host)
        time.sleep(1)
        print('\033[92mFetch successful\033[0m')
        print(f"\033[95mFetching lecture progress data\033[0m")
        finLessonList = APIWrapper.finLessonList(cookies,auth,host)
        print('\033[92mFetch successful\033[0m')
        if debug == 'yes': 
            print(classList)
            print(finLessonList)
        printClassList(classList)
        printFinLessonList(finLessonList)
        if runOpt == None:
            classIndex = getIndex(classList,len(msgdepth))[0]
        else:
            classIndex = runOpt
        if classIndex == 'front':
            msgdepth = []
        elif not isinstance(classIndex,str):
            try:
                lessonList = APIWrapper.lessonList(cookies,auth,classList[classIndex]['classUrlPath'],host)
                if debug == 'yes': print(lessonList)
                msgdepth.append(['lessonList',{}])
            except IndexError:
                pass
        elif classIndex[0:3] == 'all' or runOpt[0:3] == 'all':
            finLessonNameList = []
            for i in finLessonList:
                finLessonNameList.append(i['lsnNm'])
            for i in classList:
                classurl = i['classUrlPath']
                lessonList = APIWrapper.lessonList(cookies,auth,classurl,host)
                printLessonList(lessonList)
                for j in lessonList:
                    lectureList = APIWrapper.lectureList(cookies,auth,classurl,j['lessonSeq'],host)
                    printLectureList(lectureList)
                    for k in lectureList:
                        if k['contentsTypeCode'] in ['006','012','018'] or classIndex != 'alldoc' or runOpt != 'alldoc':
                            if k['rtpgsRt'] != 100 and k['lessonName'] in finLessonNameList:
                                try:
                                    learn(k,cookies,auth,memberSeq,percent=int(k['rtpgsRt']))
                                except ValueError:
                                    learn(k,cookies,auth,memberSeq)
        if runOpt != None:
            exit()
        if debug != 'yes': clear()
    elif len(msgdepth) == 1:
        printLessonList(lessonList)
        lessonIndex = getIndex(lessonList,len(msgdepth))[0]
        if lessonIndex == 'front':
            msgdepth = []
        elif lessonIndex == 'back':
            msgdepth.pop(0)
        elif lessonIndex == 'notice':
            msgdepth.append(['notice',{}])
        else:
            try:
                lectureList = APIWrapper.lectureList(cookies,auth,classList[classIndex]['classUrlPath'],lessonList[lessonIndex]['lessonSeq'],host)
                if debug == 'yes': print(lectureList)
                msgdepth.append(['lectureList',{}])
            except IndexError:
                pass
        if debug != 'yes': clear()
    elif len(msgdepth) == 2 and msgdepth[-1][0] == 'lectureList':
        printLectureList(lectureList)
        lectureIndex = getIndex(lectureList,len(msgdepth))
        if lectureIndex == ['front']:
            msgdepth = []
        elif lectureIndex == ['back']:
            msgdepth.pop(1)
        else:
            msgdepth.append(['learn',{}])
        if debug != 'yes': clear()
    elif len(msgdepth) == 2 and msgdepth[-1][0] == 'notice':
        print('notice - wip')
        lectureIndex = getIndex([],len(msgdepth))
        if lectureIndex == ['front']:
            msgdepth = []
        elif lectureIndex == ['back']:
            msgdepth.pop(1)
    elif len(msgdepth) == 3:
        for i in lectureIndex:
            try:
                learn(lectureList[i],cookies,auth,memberSeq,percent=int(lectureList[i]['rtpgsRt']))
            except ValueError:
                learn(lectureList[i],cookies,auth,memberSeq)
        msgdepth.pop(2)
        try:
            lectureList = APIWrapper.lectureList(cookies,auth,classList[classIndex]['classUrlPath'],lessonList[lessonIndex]['lessonSeq'],host)
            input()
        except IndexError:
            pass
        if debug != 'yes': clear()
