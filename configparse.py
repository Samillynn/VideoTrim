import os
from itertools import count
from typing import Iterator, Tuple


def deduplicate(line: str) -> str:
    """ remove all spaces and comments from a string and return the deduplicated one """
    line = line[:pos] if (pos := line.find('//')) != -1 else line
    return line.replace(' ', '')


def parse(filename: str, outType='mp4') -> Iterator[Tuple[str, str, str, str]]:
    """ parse a configuration file and yield (infile, t_start, t_end, outfile) each time"""
    config = open(filename).read().splitlines()
    for oldline in config:
        if line := deduplicate(oldline):
            if line.startswith('#'):
                infile = line[1:]
                basename = infile[:infile.rfind('.')]
                subCounter = count(1)
            else:
                attrs = [attr for attr in line.split(',') if attr]
                if len(attrs) == 2:
                    attrs.append(f'{basename}-{next(subCounter)}.{outType}')
                yield infile, *attrs