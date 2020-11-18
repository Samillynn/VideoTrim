from trim import main
from pathlib import Path

config: Path = "config_adhoc0.txt"
dir_in: Path = "/Users/mark/Desktop/trafficQA_featured_imgs/video"
dir_out: Path = "/Users/mark/Desktop/trafficQA_featured_imgs/video/new"
max_workers = 4  # the workstation has 32 cores

# pass in parameters directly
main(config, dir_in, dir_out, max_workers)
