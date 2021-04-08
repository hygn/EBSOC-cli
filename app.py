from application_functions import *
from cfg import *
import APIWrapper
import cookie
import time
import os
try:
    os.mkdir('downloads')
except FileExistsError:
    pass
debug = readCfg()['debug']
if debug == 'yes': print(readCfg())
if readCfg()['cfgLock'] != 'yes':
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
print('\033[95m Logging in... \033[0m')
try:
    cookies = cookie.query('')
    if debug == 'yes': print(cookies)
    auth = cookie.getAuth('')
    if debug == 'yes': print(auth)
    memberSeq = cookie.getMembSeq('')
    if debug == 'yes': print(memberSeq)
except:
    print('\033[91m cookie not detected \033[0m')
    cookies = None
try:
    if cookies == None:
        raise KeyError
    try:
        attemptCount = readCfg()['loginAttempt']
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
            memberData = APIWrapper.userDetail(cookies,auth,memberSeq)
            classList = APIWrapper.classList(cookies,auth)
            print('\033[92m Login successful\033[0m')
            print(f"\033[95m Logged in as {memberData['memberNm']}\033[0m")
            break
        except:
            time.sleep(5)
            if i == readCfg()['loginAttempt']:
                raise
            else:
                pass
except:
    print('\033[91m Login failed \033[0m')
    print('\033[91m Please manually input cookie data \033[0m')
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
        classList = APIWrapper.classList(cookies,auth)
        memberData = APIWrapper.userDetail(cookies,auth,memberSeq)
    except:
        print('\033[91m Login failed \033[0m')
        print('\033[91m Aborting... \033[0m')
        input()
        exit()
msgdepth = []
while True:
    if msgdepth == []:
        finLessonList = APIWrapper.finLessonList(cookies,auth)
        classList = APIWrapper.classList(cookies,auth)
        memberData = APIWrapper.userDetail(cookies,auth,memberSeq)
        if debug == 'yes': 
            print(classList)
            print(finLessonList)
        printClassList(classList)
        printFinLessonList(finLessonList)
        classIndex = getIndex(classList)[0]
        if classIndex == 'f':
            msgdepth = []
        elif classIndex != 'b':
            try:
                lessonList = APIWrapper.lessonList(cookies,auth,classList[classIndex]['classUrlPath'])
                if debug == 'yes': print(lessonList)
                msgdepth.append(['lessonList',{}])
            except IndexError:
                pass
        if debug != 'yes': clear()
    elif len(msgdepth) == 1:
        printLessonList(lessonList)
        lessonIndex = getIndex(lessonList)[0]
        if lessonIndex == 'f':
            msgdepth = []
        elif lessonIndex == 'b':
            msgdepth.pop(0)
        else:
            try:
                lectureList = APIWrapper.lectureList(cookies,auth,classList[classIndex]['classUrlPath'],lessonList[lessonIndex]['lessonSeq'])
                if debug == 'yes': print(lectureList)
                msgdepth.append(['lectureList',{}])
            except IndexError:
                pass
        if debug != 'yes': clear()
    elif len(msgdepth) == 2:
        printLectureList(lectureList)
        lectureIndex = getIndex(lectureList)
        if lectureIndex == 'front':
            msgdepth = []
        elif lectureIndex == 'back':
            msgdepth.pop(1)
        else:
            msgdepth.append(['learn',{}])
        if debug != 'yes': clear()
    elif len(msgdepth) == 3:
        for i in lectureIndex:
            learn(lectureList[i],cookies,auth,memberSeq)
        msgdepth.pop(2)
        try:
            lectureList = APIWrapper.lectureList(cookies,auth,classList[classIndex]['classUrlPath'],lessonList[lessonIndex]['lessonSeq'])
            input()
        except IndexError:
            pass
        if debug != 'yes': clear()
