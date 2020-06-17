from itertools import count
from typing import Iterator, Tuple


def deduplicate(line: str) -> str:
    """ remove all spaces and comments from a string and return the deduplicated one """
    line = line[:pos] if (pos := line.find('//')) != -1 else line
    return line.replace(' ', '')


def parse(filename: str, output_t='mp4') -> Iterator[Tuple[str, str, str, str]]:
    """ parse a configuration file and yield tuple(infile, t_start, t_end, outfile) each time"""
    config = open(filename).read().splitlines()
    for oldline in config:
        if line := deduplicate(oldline):
            if line.startswith('#'):
                infile = line[1:]
                basename = infile[:infile.rfind('.')]
                counter = count(1)
            else:
                args = [arg for arg in line.split(',') if arg]
                if len(args) == 2:
                    args.append(f'{basename}-{next(counter)}.{output_t}')
                yield tuple(infile, *args)
