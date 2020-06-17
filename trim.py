from concurrent.futures import ProcessPoolExecutor
from configparse import parse
from cmdparse import parse_args
from trimmer import Trimmer

def main():
    config_file, infolder, outfolder, max_workers = parse_args()
    trimmer = Trimmer(infolder, outfolder)
    pool = ProcessPoolExecutor(max_workers)
    for trim_args in parse(config_file):
        pool.submit(trimmer.trim, trim_args)


if __name__ == '__main__':
    main()
