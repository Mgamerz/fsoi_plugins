import SourceBase

class wallpaperAbyss(SourceBase.SourceBase):
    pluginid='_fsiplugin_wallpaperAbyss'
    sourcename='WallPaper Abyss'
    sourceurl='http://wall.alphacoders.com/'
    
    def __init__(self):
        pass
    
    def load_plugin(self):
        import WallpaperAbyssApi
        
    def get_images(self,displaybundle):
        #The bing plugin only downloads todays image.
        self.imagelist=[]

    def get_source_info(self):
        return [self.sourcename,self.sourceurl]
        
    def get_dependencies(self):
        return ['WallpaperAbyssApi']
        
    def get_pluginid(self):
        return self.sourceid
        