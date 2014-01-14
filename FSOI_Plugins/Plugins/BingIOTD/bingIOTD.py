import SourceBase
from xml.dom import minidom
import sys
from urllib.request import urlopen, urlretrieve
import datetime

class bingIOTD(SourceBase.SourceBase):
    pluginid='_fsiplugin_bing'
    sourcename='Bing Image of the Day'
    sourceurl='http://bing.com'
    
    def __init__(self):
        pass
    
    def get_images(self,displaybundle):
        #The bing plugin only downloads todays image.
        self.imagelist=[]
        #Getting and Parsing the XML File
        usock = urlopen('http://www.bing.com/HPImageArchive.aspx?format=xml&idx=0&n=1&mkt=ru-RU') #ru-RU, because they always have 1920x1200 resolution pictures
        xmldoc = minidom.parse(usock)
        bing = 'http://bing.com'
        for element in xmldoc.getElementsByTagName('url'):
            url = bing+element.firstChild.nodeValue
            
            #Download and Save the Picture
            #Get a higher resolution by replacing the image name
            url=url.replace('_1366x768', '_1920x1200')
            filename = (url).split('/')[-1] #get filename
            
            self.imagelist.append((url,filename))
        return self.imagelist

    def get_source_info(self):
        return [self.sourcename,self.sourceurl]
        
    def get_dependencies(self):
        return []
        
    def get_pluginid(self):
        return self.sourceid
        