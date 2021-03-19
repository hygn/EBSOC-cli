from cfg import *
import APIWrapper
import cookie
import time
import os
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
def printFinLessonList(finLessonList):
    print("\033[1m-----------미수강 목록------------\033[0m")
    for i in finLessonList:
        if i['rtpgsRt'] != 100:
            print(f"{i['classNm']} [{i['lsnNm']}] ({i['rtpgsRt']}%)")
    print("\033[1m----------------------------------\033[0m")
def learn(lectureData,cookies,auth,memberSeq):
    config = readCfg()
    import wget
    lectureDetail = APIWrapper.lectureDetail(cookies,auth,lectureData['lessonSeq'])
    print(f"\033[92m 강의 정보 받기에 성공했습니다.\033[0m")
    try:
        print(lectureDetail['lectureContentsDto']['lectureContentsTextDto']['textContents'])
    except:
        print(lectureDetail['lectureContentsDto']['contentsContents'])
    try:
        for i in lectureDetail['lectureContentsDto']['lectureContentsDocImageDtoList']['lectureContentsDocImageDtoList']:
            if config['saveFile'] == 'yes':
                try:
                    wget.download(i['fileleDto']['fileStoragePath'],out=i['fileleDto']['originalFileName'])
                    print('\n')
                except:
                    print('\033[95m Fall back to newFileDownloadAPI\033[0m')
                    print('Downloading...')
                    data = APIWrapper.newFileDownload(cookies,auth,i['fileleDto']['fileDetailId'])
                    if data == None:
                        print('\033[91m 강의 다운로드에 실패했습니다.\033[0m')
                    else:
                        open(i['fileleDto']['originalFileName'],'a')
                        open(i['fileleDto']['originalFileName'],'wb').write(data)
        playTime = None
        runcount = 1
    except:
        try:
            lecturl = lectureDetail['lectureContentsDto']['lectureContentsMvpDto']['mvpFileUrlPath']
            playTime = lectureDetail['lectureContentsDto']['lectureContentsMvpDto']['playTime']
            try:
                runcount = round(int(playTime/config['playSpd'])/30)
            except:
                runcount = 1
            if runcount == 0:
                runcount = 1
            if 'youtu' in lecturl and config['saveYTVideo'] == 'yes':
                import youtube_dl
                ydl_opts = {}
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    try:
                        ydl.download([lecturl])
                    except:
                        print('youtube-dl 오류가 발생했습니다')
            else:
                if config['saveEBSVideo'] == 'yes':
                    try:
                        wget.download(lecturl,out=f"{lectureDetail['lectureName']}.mp4")
                        print('\n')
                    except:
                        print('\033[91m 강의 다운로드에 실패했습니다.\033[0m')
        except TypeError:
            playTime = None
            runcount = 1
    if lectureData['lectureLearningSeq'] == None:
        try:
            createAPI = APIWrapper.createAPICheck(cookies,auth,lectureData['contentsSeq'],lectureData['contentsTypeCode'],lectureData['lectureSeq'],\
                lectureData['lessonAttendanceSeq'],lectureData['lessonSeq'],lectureData['officeEduCode'],lectureData['schoolCode'],lectureData['lectureLearningSeq'])
            lrnseq = createAPI['data']
        except:
            print('강의 정보 등록에 실패했습니다.')
    else:
        lrnseq = lectureData['lectureLearningSeq']
    if lectureData['rtpgsRt'] == 100:
        runcount = 1
    for i in range(runcount):
        if i == runcount - 1:
            print('진도율 100% 입니다')
            result = APIWrapper.learnAPI(auth,'100',memberSeq,lrnseq,'l40jsfljasln32uf','asjfknal3bafjl23')
        else:
            APIWrapper.learnAPI(auth,str(int(100*(i+1)/runcount)),memberSeq,lrnseq,'l40jsfljasln32uf','asjfknal3bafjl23')
            print(f"진도율이 저장되었습니다 ({i+1}/{runcount})")
            time.sleep(30)
    try: 
        if result['code'] == 'OK': 
            print('\n강의 수강이 완료되었습니다.')
        else:
            print('\n강의 수강에 실패했습니다.')
    except: 
        print('\n강의 수강에 실패했습니다.')
