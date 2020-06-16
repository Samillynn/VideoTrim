from concurrent.futures import ProcessPoolExecutor
from VideoTrim.parseConfig import parse
from VideoTrim.parseCmd import parseArgs
from VideoTrim.trimmer import Trimmer

def main():
    configFile, infolder, outfolder, max_workers = parseArgs()
    trimmer = Trimmer(infolder, outfolder)
    pool = ProcessPoolExecutor(max_workers)
    for trimConfig in parse(configFile):
        pool.submit(trimmer.trim, trimConfig)


if __name__ == '__main__':
    main()
