#! python3

import sys
import bs4
import requests
import os
import logging
    
def download_File(file_Link):
    downloaded_Files.append(file_Link)
    fileRequests = requests.get(file_Link)

    try:
        fileRequests.raise_for_status()
    except Exception as exc:
        return
    
    logging.debug('Downloaded: (%s)' % (file_Link))

    title = file_Link.split('/')[len(file_Link.split('/'))-1]

    file = open(title, 'wb')
    for chunk in fileRequests.iter_content(100000):
        file.write(chunk)
    file.close()
    
    print ('downloaded OK')
    
    fileNames = open('_files.txt', 'a')
    fileNames.write(', ' + file_Link)
    fileNames.close

def join_Links(link1, link2):
    link1 = link1.split('/')
    temp_Link = []
    for i in range(0, len(link1)):
        if link1[i] not in temp_Link:
            temp_Link.append(link1[i])
    link1 = '/'.join(temp_Link)
    
    try:
        if link2.startswith('#'):
            return link1
        elif link2 == '/':
            return link1
        elif link2.startswith('../'):
            return '/'.join(link1.split('/')[0:len(link1.split('/'))-2]) + link2[2:]
        elif link2.startswith('./'):
            return link1 + link2[1:]
        elif link2.startswith('/'):
            return link1 + link2
        elif link2.startswith('http'):
            return link2
        elif link2.startswith('www'):
            return 'https://' + link2
        elif link2.startswith('//'):
            return 'https://' + link2[2:]
        else:
            return link1 + '/' + link2
    except IndexError:
            return link1

def get_Link(page_Link):
    if page_Link not in visited_Links.keys():
        try:
            page = requests.get(page_Link)
        except requests.exceptions.MissingSchema:
            return
        try:
            page.raise_for_status()
        except Exception as exc:
            return
        visited_Links.update({page_Link:page})
        visited_List.append(page_Link)
    else:
        page = visited_Links.get(page_Link)

    if 'php' in page_Link:
        return
    
    logging.debug('Current link: (%s)' % (page_Link))
    
    page_Soup = bs4.BeautifulSoup(page.text, "html.parser")
    links_Temp = page_Soup.select('a')
    links = []
    
    for link in links_Temp:
        for extention in download_Extentions:
            try:
                if link.attrs['href'].endswith('.' + extention):
                    links.insert(0, link)
                elif link not in links:
                    links.append(link)
            except KeyError:
                pass
            
    for i in range(0, len(links)):
        try:
            link = (links[i].attrs)['href']
        except KeyError:
            pass 
        try:
            link = join_Links(page_Link, link)
            link_Extention = link.split('.')[len(link.split('.'))-1].lower()
            if link in visited_List:
                pass
            if 'mailto:' in link:
                pass
            elif link_Extention in download_Extentions and link_Extention not in downloaded_Files:
                download_File(link)
            elif link_Extention in extentions_List:
                pass
            elif page_Link.split('.')[1] != link.split('.')[1]:
                pass
            else:
                get_Link(link)
        except UnboundLocalError:
            pass
    return
                 

if len(sys.argv) > 1:
    if len(sys.argv) > 2:
        download_Extentions = []
        for extention in sys.argv[2:]:
            download_Extentions.append(extention.lower())
    url = sys.argv[1]
else:
    url = ('https://www.ucl.ac.uk/dpu-projects/Global_Report/cities/cairo.htm')
    download_Extentions = ['pdf']

extentions_List = ['jpg', 'png', 'gif', 'bmp', 'doc', 'docx', 'xls', 'xlsx', 'ppt',\
                   'pptx', 'txt', 'pdf', 'wav', 'mp3', 'avi', 'wmv', 'rm', 'mp4', 'mpg',\
                    'mov', 'qt', 'swf', 'dll', 'exe', 'zip', 'msi', 'reg', 'bat', 'cmd',\
                        'vbs', 'js', 'jar', 'iso', 'php']
visited_Links = {}
downloaded_Files = []
visited_List = []

os.chdir('C:')
if not os.path.exists('Files'):
    os.makedirs('Files')
os.chdir('Files')

fileNames = open('_files.txt', 'w')
fileNames.close()

logging.basicConfig(level=logging.DEBUG,\
                    format= ' %(asctime)s - %(levelname)s - %(message)s')

get_Link(url)

os.chdir('..')
print ('Finish')
