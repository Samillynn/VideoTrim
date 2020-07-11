"""
depencency: ffmpeg

reference: https://trac.ffmpeg.org/wiki/FFprobeTips#FrameRate
"""

import subprocess
import shlex
import json
from pathlib import Path
import os
import logging

logging.basicConfig(format="%(levelname)s - %(message)s",)
_logger = logging.getLogger()
_logger.setLevel(logging.DEBUG)


def get_video_metadata(video_path: str) -> dict:

    # check if the file exist
    video_path = Path(video_path)
    if not video_path.is_file():
        _logger.error(f"Invalid video_path: `{video_path}` does not exist.")
        raise Exception("Invalid video_path: file does not exist.")

    # check if it is a video file
    known_video_formats = (".mp4", ".flv", ".mov", ".avi", ".wmv", ".mkv")
    video_path_obs = video_path.resolve()
    head, tail = os.path.split(video_path_obs)
    name, ext = os.path.splitext(tail)
    if ext not in known_video_formats:
        _logger.warning(f"Invalid video_path: `{tail}` is not a known video format.")
        raise Exception(f"Invalid video_path: `{tail}` is not a known video format.")

    command_template = "ffprobe -v error -select_streams v:0 -show_entries stream=width,height,avg_frame_rate,duration -of json"
    args = shlex.split(command_template)
    args.append(str(video_path))
    proc = subprocess.Popen(args, stdout=subprocess.PIPE)
    out: bytes = proc.communicate()[0]
    json_string: str = out.decode("utf-8").strip()

    # _logger.debug(json_string)

    json_obj: dict = json.loads(json_string)

    streams: list = json_obj.get("streams", [])
    if len(streams) == 1:
        _data = streams[0]
    elif len(streams) == 0:
        raise Exception()
    else:
        _data: dict = streams[0]
        _logger.info(f"More than one stream is found at {video_path}")

    width: int = _data.get("width")
    height: int = _data.get("height")
    avg_frame_rate: str = _data.get("avg_frame_rate")
    frame_rate: int = round(eval(avg_frame_rate)) if avg_frame_rate else None
    duration: float = round(float(_data.get("duration")), 2)

    video_metadata: dict = {
        "filepath": str(video_path_obs),
        "filename": name,
        "ext": ext,
        "width": width,
        "height": height,
        "duration": duration,  # in number of seconds
        "fps": frame_rate,  # frame per seconds
        "avg_frame_rate": avg_frame_rate,
    }

    _logger.debug(json.dumps(video_metadata, indent=4))
    return video_metadata


if __name__ == "__main__":
    single_video_path = "0PgyK_oW1Vg.mp4"
    get_video_metadata(single_video_path)
