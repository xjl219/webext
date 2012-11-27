'''
Created on 2012-11-22
    Single Process Crawler
@author: roger.luo
'''

from bs4 import BeautifulSoup
import mechanize
import urllib

def generate_browser():
    ''' generate a virtual browser '''
    br = mechanize.Browser()
    br.addheaders = [('User-agent','Mozilla/5.0;textmode;Linux 2.6.1 i686;en'),
             ('HTTP_CONNECTION', 'keep-alive'),
             ('HTTP_ACCEPT', 'text/html,application/xhtml+xml,aplication/xml;q=0.9,*/*;q=0.8'),
             ('HTTP_ACCEPT_CHARSET', 'UTF-8;q=0.7,*;q=0.7'),
             ('HTTP_ACCEPT_ENCODING', 'gzip,deflate'),
             ('HTTP_USER_AGENT', 'Mozilla/5.0;textmode;Linux 2.6.1 i686;en')]

    br.set_handle_robots(False)    
    return br

def generate_search_url(text,engine):
    ''' generate a search url for the search engine'''
    if engine.lower() == 'google':
        url = 'http://www.google.com/search?' + urllib.urlencode(
            {'hl':'en','source':'hp','biw':1280,'bih':664,'q':text.encode('utf-8'),'aq':'f','api':'','apl':'','oq':''})
    elif engine.lower() == 'baidu':
        url = 'http://www.baidu.com/s?' + urllib.urlencode({'wd':text.encode('utf-8')})
    else:
        raise 'NotSupported'
    return url

def decode_text(text):
    '''decode text to unicode(middle code)'''
    try:
        text = text.decode('utf-8')
    except:
        try:
            text = text.decode('gb2312')
        except:
            text = text.decode('gbk')            
    return text

def get_page(browser,url):
    '''get url content using browser'''
    try:
        browser.open(url,None,30)
    except:
        return '' 
    return browser.response().read()

def get_selected_page_url(page, page_number, engine):
    ''' '''
    if engine.lower() == 'google':
        return get_selected_page_url_google(page,page_number)
    elif engine.lower() == 'baidu':
        return get_selected_page_url_baidu(page,page_number)
    else:
        raise 'Not Support'

def get_selected_page_url_google(page,page_number):
    ''' '''
    page = decode_text(page)
    soup = BeautifulSoup(page)

    foot = soup.find('body').find('div', {'id':'foot'})
    nav = foot.find('table', {'id':'nav'})

    max_available_page = 0
    max_available_page_url = ""
    min_available_page = 110
    min_available_page_url = ""

    for td in nav.tr.findChildren('td'):
        if td.has_key('class'):
            pass
        elif td.a == None:
            pass
        else:
            if int(td.a.contents[1]) == page_number: 
                return 'http://www.google.com' + td.a['href'] 
            elif int(td.a.contents[1]) > max_available_page:
                max_available_page = int(td.a.contents[1])
                max_available_page_url = 'http://www.google.com' + td.a['href']
            elif int(td.a.contents[1]) < min_available_page:
                min_available_page_url = int(td.a.contents[1])
    
    if max_available_page < page_number:
        br = generate_browser()
        page = get_page(browser = br, url = max_available_page_url) 
        return get_selected_page_url_google(page, page_number)

    if min_available_page > page_number:
        br = generate_browser()
        page = get_page(browser = br, url = min_available_page_url) 
        return get_selected_page_url_google(page, page_number)

    return ''

def get_selected_page_url_baidu(page, page_number):
    ''' '''
    page = decode_text(page)
    soup = BeautifulSoup(page)

    fpage = soup.find('p', {'id':'page'})
    
    max_available_page = 0
    max_available_page_url = ""
    min_available_page = 110
    min_available_page_url = ""

    for a in fpage.findChildren('a'):
        if a.has_key('class'):
            pass
        else: 
            p = int(a.contents[1].contents[0])
            if p == page_number:
                return 'http://www.baidu.com'+a['href']
            elif p > max_available_page:
                max_available_page = p
                max_available_page_url = 'http://www.baidu.com'+a['href']
            elif p < min_available_page:
                min_available_page = p
                min_available_page_url = 'http://www.baidu.com'+a['href']
    
    if max_available_page < page_number:
        br = generate_browser
        page = get_page(browser = br,url = max_available_page_url)
        return get_selected_page_url_baidu(page,page_number)
    if min_available_page > page_number:
        br = generate_browser
        page = get_page(browser = br,url = min_available_page_url)
        return get_selected_page_url_baidu(page,page_number)

    return ''

def search(text,page_number,engine):
    ''' '''
    br = generate_browser()
    url = generate_search_url(text,engine)
    print 'Start crawler "%s",return result in page %s' % (text,engine)
    page = get_page(browser = br, url = url)

    if page_number == 1:
        return page
    else:
        url = get_selected_page_url(page = page, page_number = page_number,engine = engine)
        if url != '':
            return get_page(browser = br, url = url)
        else:
            return ''

def extract_url(page, engine):
    ''' '''
    if engine.lower() == 'google':
        return extract_url_google(page)
    elif engine.lower() == 'baidu':
        return extract_url_baidu(page)
    else:
        raise 'Not Supported'

def extract_url_google(page):
    ''' '''
    page = decode_text(page)
    soup = BeautifulSoup(page)

    ires = soup.find('body').find('div',{'id':'ires'})
    urls =[]

    for li in ires.ol.findChildren('li',{'class':'g'}):
        url = 'http://www.google.com'+li.h3.a['href']
        urls.append(url)

    return urls

def extract_url_baidu(page):
    ''' '''
    page = decode_text(page)
    soup = BeautifulSoup(page)

    container = soup.find('body').find('div',{'id':'container'})
    urls = []

    for table in container.findChildren('table',{'class':'result'}):
        url = table.tr.td.h3.a['href']
        urls.append(url)
        
    return urls

def find_next_page_url(page, engine):
    ''' '''
    if engine.lower() == 'google':
        return find_next_page_url_google(page)
    elif engine.lower() == 'baidu':
        return find_next_page_url_baidu(page)
    else:
        raise 'Not Supported'

def find_next_page_url_google(page):
    ''' '''
    page = decode_text(page)
    soup = BeautifulSoup(page)

    foot = soup.find('body').find('div', {'id':'foot'})
    nav = foot.find('table', {'id':'nav'})

    for td in nav.tr:
        if td.has_key('class'):
            if td.a != None:
                return 'http://www.google.com'+td.a['href'] 

    return None

def find_next_page_url_baidu(page):
    ''' '''
    page = decode_text(page)
    soup = BeautifulSoup(page)

    fpage = soup.find('p', {'id':'page'})

    for a in fpage.findChildren('a'):
        if a.has_key('class') and a['class'][0] == 'n':
            return 'http://www.baidu.com' + a['href'] 

    return None
