import os
import subprocess
from os.path import join as pathjoin
from concurrent.futures import ProcessPoolExecutor

from configparse import Parser
from cmdparse import parse_args
from pathlib import Path

logging.basicConfig(format="%(levelname)s - %(message)s",)
_logger = logging.getLogger()
_logger.setLevel(logging.DEBUG)


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
                f'ffmpeg -loglevel warning -i "{file_in}" -ss {t_start} -to {t_end} -f mp4 -copyts "{file_out + ".part"}"',
                shell=True,
            )
            os.rename(file_out + ".part", file_out)

    def run(self, job_lst):
        pool = ProcessPoolExecutor(self.max_workers)
        for job in job_lst:
            _logger.debug(f"Submitting job: {job}")
            pool.submit(self.perform_trim, job)


def main(config="", dir_in="", dir_out="", max_workers=4):
    # validate path first
    config = Path(config)
    dir_in = Path(dir_in)
    dir_out = Path(dir_out)

    if not config.is_file():
        _logger.error(f"{config} is not a file")
        return

    if not dir_in.is_dir():
        _logger.error(f"{dir_in} is not a folder")
        return

    if not dir_out.is_dir():
        _logger.error(f"{dir_out} is not a folder")
        return

    # get user inputs
    if config == "":
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
    config: Path = "/home/UROP/data_urop/REPLACE ME/config.txt"
    dir_in: Path = "/home/UROP/data_urop/REPLACE ME/original_videos"
    dir_out: Path = "/home/UROP/data_urop/REPLACE ME/trimmed_videos"
    max_workers = 32  # the workstation has 32 cores

    # pass in parameters directly
    main(config, dir_in, dir_out, max_workers)

    # use command line
    # main()
