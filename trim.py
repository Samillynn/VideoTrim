import os
import subprocess
from os.path import join as pathjoin
from concurrent.futures import ProcessPoolExecutor

from configparse import Parser
from cmdparse import parse_args


class Trimmer:
    def __init__(self, dir_in=".", dir_out=".", max_workers=4):
        self.dir_in = dir_in
        self.dir_out = dir_out
        self.max_workers = max_workers

    def perform_trim(self, job):
        file_in, t_start, t_end, file_out = job
        file_in = pathjoin(self.dir_in, file_in)
        if file_out not in os.listdir(self.dir_out):
            file_out = pathjoin(self.dir_out, file_out)
            subprocess.run(
                f'ffmpeg -ss {t_start} -i "{file_in}" -to {t_end} -c copy -f mp4 -copyts "{file_out + ".part"}"',
                shell=True,
            )
            os.rename(file_out + ".part", file_out)

    def run(self, job_lst):
        pool = ProcessPoolExecutor(self.max_workers)
        for job in job_lst:
            pool.submit(self.perform_trim, job)


def main():
    # get user inputs
    config, dir_in, dir_out, max_workers = parse_args()

    # instantiate Parser
    parser = Parser(dir_in, config)

    # get job list from Parser
    job_lst = parser.get_job_list()

    # instantiate Trimmer
    trimmer = Trimmer(dir_in, dir_out, max_workers)

    # start Trimmer
    trimmer.run(job_lst)


if __name__ == "__main__":
    main()
