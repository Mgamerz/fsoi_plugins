import SourceBase
import re
import praw

class redditEarthporn(SourceBase.SourceBase):
	pluginid='_r_LakePorn'
	subreddit='LakePorn'
	sourceurl='http://reddit.com/r/LakePorn'
	top_images = praw.Reddit(user_agent='Python CrossPlatform Image Downloader [indev]: LakePorn Plugin by /u/Mgamerz @SourceForge')
	
	def __init__(self):
		pass
	
	def get_images(self,displaybundle):
		#get top images list from sources list. Run in a thread.
		submissions = self.top_images.get_subreddit(self.subreddit).get_hot(limit=10)
		self.imagelist=[]
		for x in submissions:
			filename = (x.url).split('/')[-1] #get filename
			resolutionReg = re.search('[0-9]+ *(x *[0-9]+)',x.title) #get resolution info from title (following the rules)
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
		