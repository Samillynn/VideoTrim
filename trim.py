from concurrent.futures import ProcessPoolExecutor
from configparse import parse
from cmdparse import parseArgs
from trimmer import Trimmer

def main():
    configFile, infolder, outfolder, maxWorkers = parseArgs()
    trimmer = Trimmer(infolder, outfolder)
    pool = ProcessPoolExecutor(maxWorkers)
    for trimConfig in parse(configFile):
        pool.submit(trimmer.trim, trimConfig)


if __name__ == '__main__':
    main()
