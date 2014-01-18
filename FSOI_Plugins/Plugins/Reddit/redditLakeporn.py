import SourceBase
import re


class redditEarthporn(SourceBase.SourceBase):
    pluginid='_r_LakePorn'
    subreddit='LakePorn'
    sourceurl='http://reddit.com/r/LakePorn'

    def __init__(self):
        pass

    def load_plugin(self):
        '''This method is called after the dependencies for this module are checked. You should import and store any local dependencies
        from modules that are in your plugin folder. You should create any objects you may need here or store the class if necessary.

        The reason this method is here is there will be a feature that if a module this plugin depends on is missing, it can still be instantiated,
        and further information can be passed to the user on how to fix it. The program may at one point offer a way to download dependencies.

        If you are positive that it will load, you can ignore this method and leave it blank, but it is not recommended.
        '''
        import praw
        self.top_images = praw.Reddit(user_agent='Python CrossPlatform Image Downloader [indev]: LakePorn Plugin by /u/Mgamerz @SourceForge')
        return

    def get_images(self, displaybundle):
        #get top images list from sources list. Run in a thread.
        submissions = self.top_images.get_subreddit(self.subreddit).get_hot(limit=10)
        self.imagelist=[]
        for x in submissions:
            filename = (x.url).split('/')[-1] #get filename
            resolutionReg = re.search('[0-9]+ *(x *[0-9]+)', x.title) #get resolution info from title (following the rules)
            if resolutionReg != None:
                imageDimensions = resolutionReg.group().split('x')
                image_width=int(imageDimensions[0].strip())
                image_height=int(imageDimensions[1].strip())
                if image_width<displaybundle.get_screen_width() or image_height<displaybundle.get_screen_height():
                    print(image_width,'x',image_height,'Image does not meet this screen\'s resolution, skipping.')
                    continue #skip this image
            #Only work on images in a certain domain
            self.download_domains(x,filename)
        return self.imagelist

    def download_domains(self,prawobj,filename):
        '''This method gets adds image URLs to the imagelist. It can parse different types of URLs.'''
        if prawobj.domain=='i.imgur.com':
            self.imagelist.append((prawobj.url,filename))
            return

        if prawobj.domain=='ppcdn.500px.org':
            self.imagelist.append((prawobj.url,filename))
            return

    def get_source_info(self):
        return [self.subreddit+' Subreddit',self.sourceurl]

    def get_dependencies(self):
        dependencies=['praw']
        return dependencies

    def get_pluginid(self):
        return self.sourceid
