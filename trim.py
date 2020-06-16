from concurrent.futures import ProcessPoolExecutor
from VideoTrim.parseConfig import Parser
from VideoTrim.parseCmd import parseArgs
from VideoTrim.trim import Trimmer

def main():
    configFile, infolder, outfolder, max_workers = parseArgs()
    trimmer = Trimmer(infolder, outfolder)
    parser = Parser(configFile)
    pool = ProcessPoolExecutor(max_workers)
    for videoName, trimConfigs in parser:
        pool.map(trimmer.trim, trimConfigs)


if __name__ == '__main__':
    main()
