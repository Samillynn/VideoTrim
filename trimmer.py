import os
from os.path import join as pathjoin
import subprocess

def trim(infile, t_start, t_end, outfile):
    subprocess.run(f'ffmpeg -ss {t_start} -i {infile} -to {t_end} -c copy -f mp4 -copyts {outfile + ".part"}')
    os.rename(outfile + '.part', outfile)


class Trimmer:
    def __init__(self, infoler='.', outfolder='.'):
        self.infolder = infoler
        self.outfolder = outfolder

    def set(self, infolder, outfoler):
        self.infolder = infolder
        self.outfolder = outfoler

    def trim(self, trimConfigObj):
        infile, t_start, t_end, outfile = trimConfigObj
        infile = pathjoin(self.infolder, infile)
        if outfile not in os.listdir(self.outfolder):
            outfile = pathjoin(self.outfolder, outfile)
            trim(infile, t_start, t_end, outfile)

