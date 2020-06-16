import os
from collections import namedtuple

TrimConfig = namedtuple('TrimConfig', 'infle t_start t_end outfile')

def parseOneVideo(s):
    initialLines = s.split('\n')
    lines = list()
    for line in initialLines:
        if line.find('//') != -1:
            line = line[:line.find('//')]
            if line:
                lines.append(line)
    videoName = lines[0]
    basename, ext = os.path.splitext(videoName)
    trimConfigs = []
    for index, line in enumerate(lines[1:], 1):
        attrs = list(filter(None, line.replace(' ', '').split(',')))
        if len(attrs) == 2:
            attrs.append(basename + str(index) + '.mp4')
        trimConfigs.append(TrimConfig(videoName, *attrs))
    return videoName, trimConfigs


class Parser:
    def __init__(self, infile):
        self.parsee = open(infile).read()

    def __iter__(self):
        for videoConfig in filter(None, self.parsee.split('#')):
            yield parseOneVideo(videoConfig)
