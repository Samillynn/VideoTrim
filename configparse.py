import os
import re
import logging
from itertools import count
from typing import Iterator, Tuple
from collections import namedtuple


logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.DEBUG,
)


trim_job = namedtuple("trim_job", "file_in t_start t_end file_out")


def clean_line(line: str) -> str:
    """ remove double forward-slash comments if any
    remove leading and trailing whitespaces
    """
    line.strip("\n")
    try:
        index = line.index("//")
        line = line[:index]
    except:
        pass
    return line.strip()


class Parser:
    def __init__(self, dir_in, config):
        self.dir_in = dir_in
        self.file_lst = os.listdir(dir_in)
        self.config_fp = config

    def get_job_list(self) -> list:
        validated = True
        job_lst = []

        for job in self.parse():
            if not self.job_is_valid(job):
                validated = False

            job_lst.append(job)

        if validated:
            logging.debug("Config file has been validated.")
            return job_lst
        else:
            raise Exception(
                f"\n\nSome errors detected in your {self.config_fp}\nPlease check logs above."
            )

    def parse(self) -> Iterator[Tuple[str, str, str, str]]:
        """ parse a configuration file and
        yield tuple(file_in, t_start, t_end, file_out) each time
        """

        with open(self.config_fp) as f:
            lines = f.readlines()

        for line in lines:
            line = clean_line(line)
            if line:

                # line reads file name
                if line.startswith("#"):

                    filename = line.strip("#").strip()
                    name, ext = os.path.splitext(filename)

                    # start counting number of clips
                    counter = count(1)

                else:
                    args = [arg.strip() for arg in line.split(",") if arg]

                    # line reads two timestamps
                    if len(args) == 2:

                        # format serial number suffix
                        _sn = next(counter)
                        if _sn <= 9:
                            _suffix = f"00{str(_sn)}"
                        elif 10 <= _sn <= 99:
                            _suffix = f"0{str(_sn)}"
                        else:
                            _suffix = str(_sn)

                        args.append(f"{name}_clip_{_suffix}.mp4")
                    else:
                        logging.debug(f"Not recognised: '{line}'")

                    yield trim_job(filename, *args)

    def job_is_valid(self, job) -> bool:

        file_in, t_start, t_end, file_out = job

        clip_validated = True
        pattern = r"^\d+$|(\d{1,2}:)?[0-6]?\d:[0-6]?\d$"

        # check if video file exist
        if file_in not in self.file_lst:
            logging.error(f"'{file_in}' doesn't exist in '{self.dir_in}'")
            clip_validated = False
        # check time format
        if not re.match(pattern, t_start):
            logging.error(f"time_start: '{t_start}' doesn't satisfy time format")
            clip_validated = False
        if not re.match(pattern, t_end):
            logging.error(f"time_end: '{t_end}' doesn't satisfy time format")
            clip_validated = False

        return clip_validated


if __name__ == "__main__":

    # use this to check config file only
    VIDEO_FOLDER = ""
    CONFIG_PATH = ""

    # VIDEO_FOLDER = "/Volumes/MARK_HFS+_2T/UROP/verified/videos"
    # CONFIG_PATH = "/Users/mark/Documents/CODE/VideoTrim/config_sample.txt"

    Parser(dir_in=VIDEO_FOLDER, config=CONFIG_PATH).get_job_list()
