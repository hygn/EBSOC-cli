import APIWrapper
import cookie
import time
import os
cfgList = [['saveFile',str],['saveYTVideo',str],['saveEBSVideo',str],['playSpd',float],['log',str],['loginAttempt',int],['cfgLock',str]]
defaultCfg = ['yes','yes','yes',0,'yes',10,'no']
def readCfg():
    try:
        cfg = open(os.path.join(os.path.dirname(__file__),'EBSOC-cli.cfg'),'r').read()
    except FileNotFoundError:
        print('설정 파일이 올바르지 않습니다')
        input()
        quit()
    cfgs = {}
    for i in cfg.split('\n'):
        try:
            arg = i.split('=')[0]
            dat = i.split('=')[1]
            cfgs.update({arg:dat})
        except IndexError:
            pass
    for i in cfgList:
        try:
            cfgs[i[0]] = i[1](cfgs[i[0]])
        except:
            cfgs.update({i[0]:None})
    return cfgs
def printCfg():
    print("\033[1m----------------------------------\033[0m")
    cfgs = readCfg()
    for i in cfgList:
        print(f"[ {i[0]} | {cfgs[i[0]]} | default:{defaultCfg[cfgList.index(i)]} | type:{str(i[1])} ]")
    print("\033[1m----------------------------------\033[0m")
def editCfg(arg,dat):
    config = readCfg()
    cfg = open(os.path.join(os.path.dirname(__file__),'EBSOC-cli.cfg'),'r').read()
    if config[arg] != None:
        cfg = cfg.replace(f"{arg}={config[arg]}",'').replace('\n\n','\n')
    open(os.path.join(os.path.dirname(__file__),'EBSOC-cli.cfg'),'w').write(f"{cfg}\n{arg}={dat}")
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
def learn(lectureData,cookies,auth,memberSeq):
    config = readCfg()
    import wget
    lectureDetail = APIWrapper.lectureDetail(cookies,auth,lectureData['lessonSeq'])
    print(f"강의 정보 받기에 성공했습니다.")
    try:
        print(lectureDetail['lectureContentsDto']['lectureContentsTextDto']['textContents'])
    except:
        print(lectureDetail['lectureContentsDto']['contentsContents'])
    try:
        for i in lectureDetail['lectureContentsDto']['lectureContentsDocImageDtoList']['lectureContentsDocImageDtoList']:
            if config['saveFile'] == 'yes':
                wget.download(i['fileleDto']['fileStoragePath'])
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
                    wget.download(lecturl,out=f"{lectureDetail['lectureName']}.mp4")
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