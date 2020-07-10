import os
import json
import logging
from pathlib import Path
from get_vid_info import get_video_metadata


logging.basicConfig(format="%(levelname)s - %(message)s",)
_logger = logging.getLogger()
_logger.setLevel(logging.DEBUG)


def generate_video_list(video_folder: str):
    """
    get metadata of all videos inside a video_folder, and
    write to `video_metadata_lst.json` and save it to the video_folder
    existing `video_metadata_lst.json` inside the target folder will be overwritten
    """
    video_folder = Path(video_folder)
    if not video_folder.is_dir():
        raise ValueError(f"'{dir}' is not a valid path to a folder.")

    video_list: list = []

    for file in os.listdir(video_folder):
        _logger.debug(file)
        video_filepath = os.path.join(video_folder, file)
        if os.path.isfile(video_filepath):
            try:
                video_metadata: dict = get_video_metadata(video_filepath)
                video_list.append(video_metadata)
            except Exception:
                continue

    # sort video list by video name alphabetically
    video_list = sorted(video_list, key=lambda x: x["filename"])

    print(f"\nTotal number of videos: {len(video_list)}\n")

    export_filepath = video_folder / "video_metadata_lst.json"
    with export_filepath.open(mode="w") as f:
        f.write(json.dumps(video_list, indent=4))


if __name__ == "__main__":

    VIDEO_FOLDER = "/home/UROP/data_urop/REPLACE ME/trimmed_videos"

    print("Traversing ...")
    generate_video_list(VIDEO_FOLDER)
    print("Done ...")
