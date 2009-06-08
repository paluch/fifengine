# coding: utf-8

import pychan
import pychan.widgets as widgets
import sys

class FileBrowser(object):
	"""
	FileBrowser displays directory and file listings from the vfs.
	The fileSelected parameter is a callback invoked when a file selection has been made; its
    signature must be fileSelected(path,filename). If selectdir is set, fileSelected's
		filename parameter should be optional.
	The savefile option provides a box for supplying a new filename that doesn't exist yet.
  The selectdir option allows directories to be selected as well as files.
	"""
	def __init__(self, engine, fileSelected, savefile=False, selectdir=False, extensions=('xml',), guixmlpath="gui/filebrowser.xml"):
		self.engine = engine
		self.fileSelected = fileSelected

		self._widget = None
		self.savefile = savefile
		self.selectdir = selectdir
		
		self.guixmlpath = guixmlpath

		self.extensions = extensions
		self.path = './..'
		self.dir_list = []
		self.file_list = []

	def showBrowser(self):
		if self._widget:
			self._widget.show()
			return
		self._widget = pychan.loadXML(self.guixmlpath)
		self._widget.mapEvents({
			'dirList'       : self._setDirectory,
			'selectButton'  : self._selectFile,
			'closeButton'   : self._widget.hide
		})
		self._setDirectory()
		if self.savefile:
			self._file_entry = widgets.TextField(name='saveField', text=u'')	
			self._widget.findChild(name="fileColumn").addChild(self._file_entry)
		self._widget.show()

	def _setDirectory(self):
		selection = self._widget.collectData('dirList')
		if not (selection < 0):
			new_dir = self.dir_list[selection]
			lst = self.path.split('/')
			if new_dir == '..' and lst[-1] != '..' and lst[-1] != '.':
				lst.pop()
			else:
				lst.append(new_dir)
			self.path = '/'.join(lst)
			
			
		def decodeList(list):
			fs_encoding = sys.getfilesystemencoding()
			if fs_encoding is None: fs_encoding = "ascii"
		
			newList = []
			for i in list:
				try:
					newList.append(unicode(i, fs_encoding))
				except:
					newList.append("WARNING: This entry could not be decoded!")
					print "WARNING: Coult not decode an item!"
			return newList

		self.dir_list = []
		self.file_list = []
		
		dir_list = ('..',) + filter(lambda d: not d.startswith('.'), self.engine.getVFS().listDirectories(str(self.path)))
		file_list = filter(lambda f: f.split('.')[-1] in self.extensions, self.engine.getVFS().listFiles(str(self.path)))
				
		self.dir_list = decodeList(dir_list)
		self.file_list = decodeList(file_list)
		self._widget.distributeInitialData({
			'dirList'  : self.dir_list,
			'fileList' : self.file_list
		})

	def _selectFile(self):
		self._widget.hide()
		selection = self._widget.collectData('fileList')

		if self.savefile:
			if self._widget.collectData('saveField'):
				self.fileSelected(self.path,self._widget.collectData('saveField'))
				return

		if selection >= 0:
			self.fileSelected(self.path,self.file_list[selection])
			return
		
		if self.selectdir:
			self.fileSelected(self.path)
			return

		print 'FileBrowser: error, no selection.'
