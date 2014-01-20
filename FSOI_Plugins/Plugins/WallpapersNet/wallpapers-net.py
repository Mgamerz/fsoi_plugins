import SourceBase
import os
import logging

class wallpapersNet(SourceBase.SourceBase):
    pluginid='_fsoiplugin_wallpapers.net'
    sourcename='Wallpapers.net'
    sourceurl='http://wallpapers.net'

    def __init__(self):
        self.logger = logging.getLogger('wallpapersnet')
        self.config_filename = '{}/wn_sources.ini'.format(os.path.dirname(__file__))

    def load_plugin(self):
        '''This method is called after the dependencies for this module are checked. You should import and store any local dependencies
        from modules that are in your plugin folder. You should create any objects you may need here or store the class if necessary.

        The reason this method is here is there will be a feature that if a module this plugin depends on is missing, it can still be instantiated,
        and further information can be passed to the user on how to fix it. The program may at one point offer a way to download dependencies.

        If you are positive that it will load, you can ignore this method and leave it blank, but it is not recommended.
        '''
        import bs4
        self.BeautifulSoup = bs4.BeautifulSoup
        import tkinter
        self.tkinter = tkinter
        import configparser
        try:
            print(self.config_filename)
            self.config = configparser.ConfigParser()
            self.config.read(self.config_filename)
            print(self.config.sections())
        except FileNotFoundError:
            print('File not found.')
            with open(self.config_filename, 'w') as f:
                self.config = configparser.ConfigParser()
                self.config['DEFAULT'] = {'resolution': '2'}
                self.config.add_section('WallpapersNET')
                self.config['WallpapersNET'] = {'resolution': '2'}
                self.config.write(f)
        import requests
        self.requests = requests
        return

    def get_images(self, displaybundle):
        imagelist = []
        url = 'http://wallpapers.net'
        pagehtml = self.gethtml(url, '/food-desktop-wallpapers.html')
        soup = self.BeautifulSoup(pagehtml.content)
        wall = soup.find_all('div', class_='wall')

        pagelinks=[]
        for paper in wall:
            pagelinks.append('{}/view-{}'.format(url, paper.find('a').get('href')[1:]))

        hd_tail = '-1920x1080.html'
        for link in pagelinks:
            link = link.replace('-wallpapers.html', hd_tail)

            print(link)
            response = self.gethtml(link)
            if response.status_code != 200:
                self.logger.warning('Wallpaper did not have normal response code - might not exist at this resolution. Skip.')
                continue
            soup = self.BeautifulSoup(response.content)
            images = soup.find_all('img')
            for image in images:
                imgurl = image.get('src')
                print(imgurl)
                imagelist.append((imgurl, self.filename_from_url(imgurl)))


        return imagelist

    def gethtml(self, link, sublink=None):
        if sublink:
            ret = self.requests.get('{}{}'.format(link, sublink), headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:26.0) Gecko/20100101 Firefox/26.0'})
            return ret
        else:
            ret = self.requests.get(link, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:26.0) Gecko/20100101 Firefox/26.0'})
            return ret

    def get_source_info(self):
        return [self.sourcename, self.sourceurl]

    def get_dependencies(self):
        dependencies = ['bs4', 'tkinter', 'configparser', 'requests']
        return dependencies

    def get_pluginid(self):
        return self.sourceid

    def configure(self, tk_window):
        wdw = self.tkinter.Toplevel()
        wdw.config(background='#ededed')

        wdw.geometry('+400+400')
        #Setup interface
        wdw.title('Wallpapers.net Plugin Options')
        self.tkinter.ttk.Label(wdw, text='Wallpapers.net Plugin Options').grid(row=0, column=0, columnspan=3)

        self.res_setting = self.tkinter.IntVar()
        self.tkinter.ttk.Label(wdw, text='Preferred Resolution').grid(row=1)

        self.tkinter.ttk.Radiobutton(wdw, text='1280 x 720', variable=self.res_setting, value=1).grid(row=2, column=0,
                                                                                                      columnspan=4,
                                                                                                      sticky='W')
        self.tkinter.ttk.Radiobutton(wdw, text='1920 x 1080', variable=self.res_setting, value=2).grid(row=3, column=0,
                                                                                                       columnspan=4,
                                                                                                       sticky='W')


        self.save = self.tkinter.ttk.Button(wdw, text='Save Settings', command=lambda: self.save_settings(wdw))
        self.save.grid(row=10, column=3)

        self.res_setting.set(self.config.getint('WallpapersNET', 'resolution'))

        #Finish up windowing.
        wdw.transient(tk_window)
        wdw.grab_set()
        tk_window.wait_window(wdw)
        #window has closed.

    def save_settings(self, settings_window):
        self.config.set('WallpapersNET', 'resolution', str(self.res_setting.get()))
        with open(self.config_filename, 'w') as configfile:
            self.config.write(configfile)
        settings_window.destroy()