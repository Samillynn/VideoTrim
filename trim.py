import os
from os.path import join as pathjoin
import subprocess
from concurrent.futures import ProcessPoolExecutor
from configparse import Parser
from cmdparse import parse_args


class Trimmer:
    def __init__(self, infoler='.', outfolder='.', max_workers=4):
        self.infolder = infoler
        self.outfolder = outfolder
        self.max_workers = max_workers

    def trim_one(self, config_obj):
        infile, t_start, t_end, outfile = config_obj
        infile = pathjoin(self.infolder, infile)
        if outfile not in os.listdir(self.outfolder):
            outfile = pathjoin(self.outfolder, outfile)
            subprocess.run(f'ffmpeg -ss {t_start} -i "{infile}" -to {t_end} -c copy -f mp4 -copyts "{outfile + ".part"}"', shell=True)
            os.rename(outfile + '.part', outfile)

    def run(self, config_lst):
        pool = ProcessPoolExecutor(self.max_workers)
        for config_obj in config_lst:
            pool.submit(self.trim_one, config_obj)


def main():
    config, infolder, outfolder, max_workers = parse_args()
    trimmer = Trimmer(infolder, outfolder, max_workers)
    parser = Parser(infolder, config)
    config_lst = parser.run()
    trimmer.run(config_lst)


if __name__ == '__main__':
    main()
