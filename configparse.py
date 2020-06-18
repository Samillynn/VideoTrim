import os
import re
from itertools import count
from typing import Iterator, Tuple
from collections import namedtuple

ConfigObj = namedtuple('ConfigObj', 'infile t_start t_end outfile')


def deduplicate(line: str) -> str:
    """ remove all spaces and comments from a string and return the deduplicated one """
    line = line[:pos] if (pos := line.find('//')) != -1 else line
    return line.replace(' ', '')


class Parser:
    def __init__(self):
        self.infolder = None
        self.file_lst = None

    def run(self, config='config.txt', infolder='.'):
        config_lst = list()
        self.infolder = infolder
        self.file_lst = os.listdir(infolder)
        for config_obj in self.parse(config):
            self.check(config_obj)
            config_lst.append(config_obj)
        return config_lst

    @staticmethod
    def parse(filename: str, output_t='mp4') -> Iterator[Tuple[str, str, str, str]]:
        """ parse a configuration file and yield tuple(infile, t_start, t_end, outfile) each time"""
        config = open(filename).read().splitlines()
        for oldline in config:
            if line := deduplicate(oldline):
                if line.startswith('#'):
                    infile = line[1:].strip()
                    basename = infile[:infile.rfind('.')]
                    counter = count(1)
                else:
                    args = [arg for arg in line.split(',') if arg]
                    if len(args) == 2:
                        args.append(f'{basename}_clip_{next(counter)}.{output_t}')
                    yield ConfigObj(infile, *args)

    def check(self, config_obj):
        infile, t_start, t_end, oufile = config_obj
        if infile not in self.file_lst:
            raise FileNotFoundError(f'Can not find {infile} in input folder {self.infolder}')
        pattern = r'^\d+$|(\d{1,2}:)?[0-6]?\d:[0-6]?\d$'
        if not re.match(pattern, t_start):
            raise Exception(f'{t_start} doesn\'t satisfy time format')
        if not re.match(pattern, t_end):
            raise Exception(f'{t_end} doesn\'t satisfy time format')
