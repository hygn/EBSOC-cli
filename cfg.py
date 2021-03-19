import os
cfgList = [['saveFile',str],['saveYTVideo',str],['saveEBSVideo',str],['playSpd',float],['log',str],['loginAttempt',int],['cfgLock',str],\
    ['debug',str]]
defaultCfg = ['yes','yes','yes',0,'yes',10,'no','no']
def readCfg():
    try:
        cfg = open(os.path.join(os.path.dirname(__file__),'EBSOC-cli.cfg'),'r').read()
    except FileNotFoundError:
        print('설정 파일이 올바르지 않습니다.')
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