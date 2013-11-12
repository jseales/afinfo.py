import os
import subprocess
import re



class Afinfo(object):
    def __init__(self, afinfodir, audiopath):
        afinfobasename = '.'.join(os.path.basename(audiopath).split('.')[:-1])
        self.afinfopath = "{}{}_afinfo.txt".format(afinfodir, afinfobasename)
        command = "afinfo '{}' > '{}'".format(audiopath, self.afinfopath) 
        subprocess.call(command, shell=True)
        
        self.audiopath = audiopath 
        self.fileType = None
        self.resolution = None
        self.duration = None
        self.samples = None
        
        f = file(self.afinfopath,'r')
        for line in f.readlines():
            if not self.fileType:
                ft=re.search('File type ID:\s*(\w+)',line)
                if ft:
                    self.fileType = ft.group(1)

            if not self.resolution:
                r=re.search('(\d+) Hz',line)
                if r:        
                    self.resolution = int(r.group(1))

            if not self.duration:
                d=re.search('estimated duration: ([0-9.]+) sec',line)
                if d:
                    self.duration = float(d.group(1))
            
            if self.fileType in ['WAVE','AIFF'] and not self.samples :
                ap=re.search('audio packets: (\d+)',line)
                if ap:
                    self.samples = int(ap.group(1))
                    
            elif self.fileType in ['caff','m4af','MPG3','mp4f'] and not self.samples:
                avf=re.search('audio (\d+) valid frames',line)
                if avf:
                    self.samples = int(avf.group(1))
        self.duration = float(self.samples)/self.resolution

       


