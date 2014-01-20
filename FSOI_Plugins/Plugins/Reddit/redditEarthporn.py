import SourceBase
from tkinter import *
from tkinter import ttk
import re

class redditEarthporn(SourceBase.SourceBase):
    pluginid = '_r_EarthPorn'
    subreddit = 'EarthPorn'
    sourceurl = 'http://reddit.com/r/EarthPorn'

    def __init__(self):
        pass

    def load_plugin(self):
        '''This method is called after the dependencies for this module are checked. You should import and store any local dependencies
        from modules that are in your plugin folder. You should create any objects you may need here or store the class if necessary.

        The reason this method is here is is because if a module this plugin depends on is missing, it can still be instantiated,
        and further information can be passed to the user on how to fix it. The program may at one point offer a way to download dependencies.

        If you are positive that it will load, you can ignore this method and leave it blank, but it is not recommended.
        '''
        import praw
        self.top_images = praw.Reddit(user_agent='Python CrossPlatform Image Downloader [indev]: EarthPorn Plugin by /u/Mgamerz @SourceForge')
        return

    def get_images(self, displaybundle):
        #get top images list from sources list. Run in a thread.
        displaybundle.screen_height = 900
        displaybundle.screen_width = 1600
        submissions = self.top_images.get_subreddit(self.subreddit).get_hot(limit=10)
        self.imagelist=[]
        for x in submissions:
            filename = (x.url).split('/')[-1] #get filename
            resolutionReg = re.search('[0-9]+ *(x *[0-9]+)',x.title) #get resolution info from title (following the rules)
            if resolutionReg != None:
                imageDimensions = resolutionReg.group().split('x')
                image_width = int(imageDimensions[0].strip())
                image_height = int(imageDimensions[1].strip())
                if image_width < displaybundle.get_screen_width() or image_height < displaybundle.get_screen_height():
                    print(image_width,'x',image_height,'Image does not meet this screen\'s resolution, skipping.')
                    continue #skip this image
            #Only work on images in a certain domain
            self.download_domains(x, filename)
        return self.imagelist

    def download_domains(self,prawobj,filename):
        '''This method gets adds image URLs to the imagelist. It can parse different types of URLs.'''
        if prawobj.domain == 'i.imgur.com':
            self.imagelist.append((prawobj.url, filename))
            return

        if prawobj.domain == 'ppcdn.500px.org':
            self.imagelist.append((prawobj.url, filename))
            return

    def get_source_info(self):
        return ['{} Subreddit'.format(self.subreddit), self.sourceurl]

    def get_dependencies(self):
        dependencies = ['praw', 'tkinter']
        return dependencies

    def configure(self, tk_window):
        wdw = Toplevel()
        wdw.geometry('+400+400')
        #Setup interface
        wdw.title('Earthporn Plugin Options')
        ttk.Label(wdw, text='EarthPorn Subreddit Plugin Options').grid(row=0, column=0, columnspan=3)

        self.res_setting = IntVar()
        self.monitor_res = ttk.Radiobutton(wdw, text='Use monitor resolution as size minimum', variable=self.res_setting, value=1, command=self.res_setting_change)
        self.monitor_res.grid(row=1, column=0, columnspan=4, sticky='W')

        self.custom_res = ttk.Radiobutton(wdw, text='Use custom resolution as size minimum', variable=self.res_setting, value=2, command=self.res_setting_change)
        self.custom_res.grid(row=2, column=0, columnspan=4, sticky='W')


        self.custom_xreslabel = ttk.Label(wdw, text='Minimum Height:')
        self.custom_xreslabel.grid(row=3, column=1, sticky='W')
        self.custom_yreslabel = ttk.Label(wdw, text='Minimum Width:')
        self.custom_yreslabel.grid(row=4, column=1, sticky='W')

        self.custom_xres = ttk.Entry(wdw, width=6)
        self.custom_xres.grid(row=3, column=2, sticky='W')
        self.custom_yres = ttk.Entry(wdw, width=6)
        self.custom_yres.grid(row=4, column=2, sticky='W')

        self.save = ttk.Button(wdw, text='Save Settings', command=lambda: self.save_settings(wdw))
        self.save.grid(row=10, column=3)


        self.res_setting.set(1)
        self.res_setting_change()

        #Finish up windowing.
        wdw.transient(tk_window)
        wdw.grab_set()
        tk_window.wait_window(wdw)
        #window has closed.


    def save_settings(self, settings_window):
        settings_window.destroy()

    def res_setting_change(self):
        self.custom_xres.config(state='disabled' if self.res_setting.get() == 1 else 'active')
        self.custom_yres.config(state='disabled' if self.res_setting.get() == 1 else 'active')
        self.custom_xreslabel.config(state='disabled' if self.res_setting.get() == 1 else 'active')
        self.custom_yreslabel.config(state='disabled' if self.res_setting.get() == 1 else 'active')

    def get_pluginid(self):
        return self.sourceid
