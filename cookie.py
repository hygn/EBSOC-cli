def query(hoc):
    import platform
    import browser_cookie3
    if platform.system() == 'Linux':
        try:
            browser_cookie3.firefox(domain_name=hoc+".ebsoc.co.kr")
        except:
            import bc3_alt as browser_cookie3
        data = str(browser_cookie3.firefox(domain_name=hoc+".ebsoc.co.kr")).replace('<CookieJar[','').replace('}>','').split(">, <")
    else:
        try:
            browser_cookie3.chrome(domain_name=hoc+".ebsoc.co.kr")
        except:
            import bc3_alt as browser_cookie3
        data = str(browser_cookie3.chrome(domain_name=hoc+".ebsoc.co.kr")).replace('<CookieJar[','').replace('}>','').split(">, <")
    cookies = ''
    for i in data:
        if hoc+'.ebsoc.co.kr' in i and 'www.ebsoc.co.kr' not in i:
            cookies = cookies + i.replace('Cookie ','').split(' for')[0] + '; '
    return cookies.replace('<','')
def getAuth(hoc):
    import platform
    import browser_cookie3
    if platform.system() == 'Linux':
        try:
            browser_cookie3.firefox(domain_name=hoc+".ebsoc.co.kr")
        except:
            import bc3_alt as browser_cookie3
        data = str(browser_cookie3.firefox(domain_name=hoc+".ebsoc.co.kr")).replace('<CookieJar[','').replace('}>','').split(">, <")
    else:
        try:
            browser_cookie3.chrome(domain_name=hoc+".ebsoc.co.kr")
        except:
            import bc3_alt as browser_cookie3
        data = str(browser_cookie3.chrome(domain_name=hoc+".ebsoc.co.kr")).replace('<CookieJar[','').replace('}>','').split(">, <")
    for i in data:
        if hoc+'.ebsoc.co.kr' in i:
            cookies = i.replace('Cookie ','').split(' for')[0].split('=')
            if cookies[0] == 'access':
                return cookies[1]
    return
def getMembSeq(hoc):
    import platform
    import browser_cookie3
    if platform.system() == 'Linux':
        try:
            browser_cookie3.firefox(domain_name=hoc+".ebsoc.co.kr")
        except:
            import bc3_alt as browser_cookie3
        data = str(browser_cookie3.firefox(domain_name=hoc+".ebsoc.co.kr")).replace('<CookieJar[','').replace('}>','').split(">, <")
    else:
        try:
            browser_cookie3.chrome(domain_name=hoc+".ebsoc.co.kr")
        except:
            import bc3_alt as browser_cookie3
        data = str(browser_cookie3.chrome(domain_name=hoc+".ebsoc.co.kr")).replace('<CookieJar[','').replace('}>','').split(">, <")
    for i in data:
        if hoc+'.ebsoc.co.kr' in i:
            cookies = i.replace('Cookie ','').split(' for')[0].split('=')
            if cookies[0] == 'memberSeq':
                return cookies[1]
    return
