from application_functions import *
import APIWrapper
import cookie
import time
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
print('\033[95m Logging in... \033[0m')
cookies = cookie.query('')
auth = cookie.getAuth('')
memberSeq = cookie.getMembSeq('')
try:
    try:
        attemptCount = readCfg()['loginAttempt']
    except:
        attemptCount = defaultCfg[5]
    for i in range(attemptCount):
        try:
            memberData = APIWrapper.userDetail(cookies,auth,memberSeq)
            classList = APIWrapper.classList(cookies,auth)
            break
        except KeyError:
            time.sleep(5)
            if i == 9:
                raise KeyError
            else:
                pass
except KeyError:
    print('\033[91m Login failed \033[0m')
    print('\033[91m Please manually input cookie data \033[0m')
    auth = input('access = ')
    host = input('host = ')
    memberSchoolCode = input('memberSchoolCode = ')
    memberSeq = input('memberSeq = ')
    memberTargetCode = input('memberTargetCode = ')
    schoolInfoYn = 'Y'
    WHATAP = input('WHATAP = ')
    cookie = f'access={auth} host={host}, memberSchoolCode={memberSchoolCode}, memberSeq={memberSeq}, '\
        f'memberTargetCode={memberTargetCode}, schoolInfoYn=Y, WHATAP={WHATAP}, '
    try:
        classList = APIWrapper.classList(cookies,auth)
        memberData = APIWrapper.userDetail(cookies,auth,memberSeq)
    except KeyError:
        print('\033[91m Login failed \033[0m')
        print('\033[91m Aborting... \033[0m')
        input()
        exit()
except:
    print('\033[91m login failed\033[0m')
print('\033[92m Login successful\033[0m')
print(f"\033[95m Logged in as {memberData['memberNm']}\033[0m")
msgdepth = []
while True:
    if msgdepth == []:
        printClassList(classList)
        classIndex = getIndex(classList)[0]
        if classIndex == 'f':
            msgdepth = []
        elif classIndex != 'b':
            lessonList = APIWrapper.lessonList(cookies,auth,classList[classIndex]['classUrlPath'])
            msgdepth.append(['lessonList',{}])
        clear()
    elif len(msgdepth) == 1:
        printLessonList(lessonList)
        lessonIndex = getIndex(lessonList)[0]
        if lessonIndex == 'f':
            msgdepth = []
        elif lessonIndex == 'b':
            msgdepth.pop(0)
        else:
            lectureList = APIWrapper.lectureList(cookies,auth,classList[classIndex]['classUrlPath'],lessonList[lessonIndex]['lessonSeq'])
            msgdepth.append(['lectureList',{}])
        clear()
    elif len(msgdepth) == 2:
        printLectureList(lectureList)
        lectureIndex = getIndex(lectureList)
        if lectureIndex == 'front':
            msgdepth = []
        elif lectureIndex == 'back':
            msgdepth.pop(1)
        else:
            msgdepth.append(['learn',{}])
        clear()
    elif len(msgdepth) == 3:
        for i in lectureIndex:
            learn(lectureList[i],cookies,auth,memberSeq)
        msgdepth.pop(2)
        lectureList = APIWrapper.lectureList(cookies,auth,classList[classIndex]['classUrlPath'],lessonList[lessonIndex]['lessonSeq'])
        input()
        clear()
