import APIWrapper
import cookie
print('\033[95m Logging in... \033[0m')
cookies = cookie.query('')
auth = cookie.getAuth('')
memberSeq = cookie.getMembSeq('')
try:
    memberData = APIWrapper.userDetail(cookies,auth,memberSeq)
    classList = APIWrapper.classList(cookies,auth)
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
except:
    print('\033[91m login failed\033[0m')
print('\033[92m Login successful\033[0m')
print(f"\033[95m Logged in as {memberData['memberNm']}\033[0m")
def printClassList(classList):
    print("\033[1m----------------------------------\033[0m")
    for i in classList:
        print(f"{str(classList.index(i))}. {i['className']} ({i['establishmentUserName']} 선생님)")
    print("\033[1m----------------------------------\033[0m")
def getIndex(List_):
    while True:
        ind = input('input index: ')
        try:
            if int(ind) <= len(List_):
                return int(ind)
        except:
            pass
printClassList(classList)
classIndex = getIndex(classList)
lessonList = APIWrapper.lessonList(cookies,auth,classList[classIndex]['classUrlPath'])
def printLessonList(lessonList):
    print("\033[1m----------------------------------\033[0m")
    for i in lessonList:
        print(f"{str(lessonList.index(i))}. {i['lessonName']} ({i['memberName']} 선생님) [{i['lessonIntroduce']}]")
    print("\033[1m----------------------------------\033[0m")
printLessonList(lessonList)
lessonIndex = getIndex(lessonList)
lectureList = APIWrapper.lectureList(cookies,auth,classList[classIndex]['classUrlPath'],lessonList[lessonIndex]['lessonSeq'])
def printLectureList(lectureList):
    print("\033[1m----------------------------------\033[0m")
    for i in lectureList:
        print(f"{str(lectureList.index(i))}. {i['lessonName']}")
    print("\033[1m----------------------------------\033[0m")
printLectureList(lectureList)
lectureIndex = getIndex(lectureList)
def learn(lectureData):
    import wget
    lectureDetail = APIWrapper.lectureDetail(cookies,auth,lectureData['lessonSeq'])
    print(f"강의 정보 받기에 성공했습니다.")
    #print(lectureDetail)
    try:
        print(lectureDetail['lectureContentsDto']['lectureContentsTextDto']['textContents'])
    except:
        print(lectureDetail['lectureContentsDto']['contentsContents'])
    try:
        for i in lectureDetail['lectureContentsDto']['lectureContentsDocImageDtoList']['lectureContentsDocImageDtoList']:
            wget.download(i['fileleDto']['fileStoragePath'])
    except:
        try:
            lecturl = lectureDetail['lectureContentsDto']['lectureContentsMvpDto']['mvpFileUrlPath']
            if 'youtu' in lecturl:
                import youtube_dl
                ydl_opts = {}
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([lecturl])
            else:
                wget.download(lecturl,out=f"{lectureDetail['lectureName']}.mp4")
        except TypeError:
            pass
    if lectureData['lectureLearningSeq'] == None:
        print('\n강의 수강 실패')
        print('강의 정보 등록 후 다시 시도해 주세요.')
        result = {}
    else:
        result = APIWrapper.learnAPI(auth,'100',memberSeq,lectureData['lectureLearningSeq'],'l40jsfljasln32uf','asjfknal3bafjl23')
    try: 
        if result['code'] == 'OK': 
            print('\n강의 수강이 완료되었습니다.')
        else:
            print('\n강의 수강에 실패했습니다.')
    except: 
        print('\n강의 수강에 실패했습니다.')
learn(lectureList[lectureIndex])
