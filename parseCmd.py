import argparse
from collections import namedtuple
CmdArgs = namedtuple('CmdArgs', 'configFile infolder outfolder max_workers')


def parseArgs():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-i', '--infolder',
                           help='configure where to find input videos', default='.')
    argparser.add_argument('-o', '--outfolder', help='config where to output videos',
                           default='.')
    argparser.add_argument('-c', '--config', help='config the right config.txt file',
                           default='config.txt')
    argparser.add_argument('-m', '--max_workers', type=int, default=4,
                           help='config the maxium process number, default value is 4')
    args = argparser.parse_args()
    return CmdArgs(args.config, args.infolder, args.outfolder, args.max_workers)

