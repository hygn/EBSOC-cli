import APIWrapper
import cookie
def clear():
    import sys
    import os
    if 'win' in sys.platform.lower():
        os.system('cls')
    else:
        os.system('clear')
def printClassList(classList):
    print("\033[1m----------------------------------\033[0m")
    for i in classList:
        print(f"{str(classList.index(i))}. {i['className']} ({i['establishmentUserName']} 선생님)")
    print("\033[1m----------------------------------\033[0m")
def getIndex(List_):
    while True:
        ind = input('input index: ').strip()
        try:
            if int(ind) <= len(List_):
                return [int(ind)]
        except ValueError:
            if ',' in ind:
                return list(map(int,ind.split(',')))
            elif ind == 'all':
                return list(range(len(List_)))
            elif ind == 'back':
                return 'back'
            elif ind == 'front':
                return 'front'
            elif ind == 'quit':
                quit()
            else:
                raise Exception
        except:
            print('\033[91m값을 제대로 입력해주세요!\033[0m')
def printLessonList(lessonList):
    print("\033[1m----------------------------------\033[0m")
    for i in lessonList:
        print(f"{str(lessonList.index(i))}. {i['lessonName']} ({i['memberName']} 선생님) [{i['lessonIntroduce']}]")
    print("\033[1m----------------------------------\033[0m")
def printLectureList(lectureList):
    print("\033[1m----------------------------------\033[0m")
    for i in lectureList:
        print(f"{str(lectureList.index(i))}. {i['lessonName']} ({i['rtpgsRt']}%) del:{i['delYn']}")
    print("\033[1m----------------------------------\033[0m")
def learn(lectureData,cookies,auth,memberSeq):
    import wget
    lectureDetail = APIWrapper.lectureDetail(cookies,auth,lectureData['lessonSeq'])
    print(f"강의 정보 받기에 성공했습니다.")
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
                    try:
                        ydl.download([lecturl])
                    except:
                        print('youtube-dl 오류가 발생했습니다')
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
