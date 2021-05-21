from cfg import readCfg
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
        try:
            ind = input('input index: ').strip()
        except KeyboardInterrupt:
            print('')
            quit()
        try:
            if int(ind) <= len(List_):
                return [int(ind)]
        except ValueError:
            if ',' in ind:
                return list(map(int,ind.split(',')))
            elif ind == 'all':
                return list(range(len(List_)))
            elif ind == 'alldoc':
                tmplst = []
                for i in list(range(len(List_))):
                    if List_[i]['contentsTypeCode'] in ['006','012','018']:
                        tmplst.append(i)
                return tmplst
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
        lsnInt = i['lessonIntroduce'].replace('\n',' ')
        print(f"{str(lessonList.index(i))}. {i['lessonName']} ({i['memberName']} 선생님) [{lsnInt}]")
    print("\033[1m----------------------------------\033[0m")
def printLectureList(lectureList):
    print("\033[1m----------------------------------\033[0m")
    for i in lectureList:
        print(f"{str(lectureList.index(i))}. {i['lessonName']} ({i['rtpgsRt']}%) del:{i['delYn']} open:{i['openYn']}")
        print(f"    [{i['learnBeginDate']} ~ {i['learnEndDate']}] 최초 입력일시: {i['firstRegistDate']} / 최종 수정일시: {i['lastUpdateDate']}\n")
    print("\033[1m----------------------------------\033[0m")
def printFinLessonList(finLessonList):
    print("\033[1m-----------미수강 목록------------\033[0m")
    for i in finLessonList:
        if i['rtpgsRt'] != 100:
            print(f"{i['classNm']} [{i['lsnNm']}] ({i['rtpgsRt']}%)")
    print("\033[1m----------------------------------\033[0m")
def learn(lectureData,cookies,auth,memberSeq,percent=0):
    import glob
    import shutil
    config = readCfg()
    if config['debug'] == 'yes': print(lectureData)
    import wget
    lectureDetail = APIWrapper.lectureDetail(cookies,auth,lectureData['lessonSeq'])
    schoolCode = lectureData['schoolCode']
    print(f"\033[92m 강의 정보 받기에 성공했습니다.\033[0m")
    try:
        print(lectureDetail['lectureContentsDto']['lectureContentsTextDto']['textContents'])
    except:
        try:
            print(lectureDetail['lectureContentsDto']['contentsContents'])
        except TypeError:
            pass
    try:
        for i in lectureDetail['lectureContentsDto']['lectureContentsDocImageDtoList']['lectureContentsDocImageDtoList']:
            if config['saveFile'] == 'yes':
                try:
                    wget.download(i['fileleDto']['fileStoragePath'],out=os.path.join(os.path.dirname(__file__),f"downloads/{i['fileleDto']['originalFileName'].replace('/','').replace('?','')}"))
                    print('\n')
                except:
                    #이렇게 예외처리 하라고 메일도 보냈는데 처리 대충대충하는건 EBS종특이냐?
                    print('\033[95m Fall back to newFileDownloadAPI\033[0m')
                    print('Downloading...')
                    data = APIWrapper.newFileDownload(cookies,auth,i['fileleDto']['fileDetailId'])
                    if data == None:
                        print('\033[91m 강의 다운로드에 실패했습니다.\033[0m')
                    else:
                        open(os.path.join(os.path.dirname(__file__),f"downloads/{i['fileleDto']['originalFileName'].replace('/','').replace('?','')}"),'a')
                        open(os.path.join(os.path.dirname(__file__),f"downloads/{i['fileleDto']['originalFileName'].replace('/','').replace('?','')}"),'wb').write(data)
        playTime = None
        runcount = 1
    except:
        try:
            lecturl = lectureDetail['lectureContentsDto']['lectureContentsMvpDto']['mvpFileUrlPath']
            playTime = lectureDetail['lectureContentsDto']['lectureContentsMvpDto']['playTime']
            try:
                runcount = round(int((playTime*(100 - percent)/100)/config['playSpd'])/30)
            except:
                runcount = 1
            if runcount == 0:
                runcount = 1
            try:
                os.mkdir(os.getcwd()+'/downloads')
            except FileExistsError:
                pass
            if 'youtu' in lecturl and config['saveYTVideo'] == 'yes':
                import youtube_dl
                ydl_opts = {
                    'format': 'best/best',
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    try:
                        ydl.download([lecturl])
                    except:
                        print('youtube-dl 오류가 발생했습니다')
                try: 
                    for f in glob.glob(os.getcwd()+r'/*.mp4'):
                        shutil.move(f,os.getcwd()+'/downloads')
                except:
                    print('shutil 오류가 발생했습니다 [대체로 심각한 문제가 아닙니다.]')
                    try:
                        for f in glob.glob(os.getcwd()+r'/*.mp4'):
                            os.remove(f)
                    except:
                        print('파일 핸들링 오류가 발생했습니다')
            else:
                if config['saveEBSVideo'] == 'yes':
                    try:
                        wget.download(lecturl,out=os.path.join(os.path.dirname(__file__),f"downloads/{lectureDetail['lectureName'].replace('/','').replace('?','')}.mp4"))
                        print('\n')
                    except:
                        print('\n\033[91m 강의 다운로드에 실패했습니다.\033[0m')
        except TypeError:
            playTime = None
            runcount = 1
    if lectureData['lectureLearningSeq'] == None:
        try:
            createAPI = APIWrapper.createAPICheck(cookies,auth,lectureData['contentsSeq'],lectureData['contentsTypeCode'],lectureData['lectureSeq'],\
                lectureData['lessonAttendanceSeq'],lectureData['lessonSeq'],lectureData['officeEduCode'],lectureData['schoolCode'],lectureData['lectureLearningSeq'])
            lrnseq = createAPI['data']
            if config['debug'] == 'yes': print(f"lectCrt: {createAPI}")
        except:
            print('강의 정보 등록에 실패했습니다.')
            if config['debug'] == 'yes': print(createAPI)
            return
    else:
        lrnseq = lectureData['lectureLearningSeq']
    if lectureData['rtpgsRt'] == 100:
        runcount = 1
    for i in range(runcount):
        if i == runcount - 1:
            print('진도율 100% 입니다')
            for p in range(10):
                p
                try:
                    result = APIWrapper.learnAPI(auth,'100',memberSeq,lrnseq,schoolCode,'l40jsfljasln32uf','asjfknal3bafjl23')
                    break
                except:
                    pass
        else:
            try:
                for p in range(10):
                    try:
                        if int(100*(i+1)/runcount)+percent >= 100:
                            progress = 99
                        else:
                            progress = int(100*(i+1)/runcount)+percent
                        APIWrapper.learnAPI(auth,str(progress),memberSeq,lrnseq,schoolCode,'l40jsfljasln32uf','asjfknal3bafjl23')
                        break
                    except APIWrapper.json.JSONDecodeError:
                        progress = 0
                        pass
                print(f"진도율이 저장되었습니다 ({i+1}/{runcount}) [{progress}%]")
                time.sleep(30)
            except KeyboardInterrupt:
                APIWrapper.learnAPI(auth,str(progress),memberSeq,lrnseq,schoolCode,'l40jsfljasln32uf','asjfknal3bafjl23')
                print('\n강의 수강이 중단되었습니다.')
                return
    try: 
        if result['code'] == 'OK': 
            print('\n강의 수강이 완료되었습니다.')
        else:
            print('\n강의 수강에 실패했습니다.')
    except: 
        print('\n강의 수강에 실패했습니다.')
