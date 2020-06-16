from concurrent.futures import ProcessPoolExecutor
from parseConfig import parse
from parseCmd import parseArgs
from trimmer import Trimmer

def main():
    configFile, infolder, outfolder, max_workers = parseArgs()
    trimmer = Trimmer(infolder, outfolder)
    pool = ProcessPoolExecutor(max_workers)
    for trimConfig in parse(configFile):
        pool.submit(trimmer.trim, trimConfig)


if __name__ == '__main__':
    main()
