import os
from pathlib import Path

known_video_formats = (".mp4", ".flv", ".mov", ".avi", ".wmv", ".mkv")


def generate_config_template(dir: str, export_filepath: str = "config.txt"):
    dir = Path(dir)
    export_filepath = Path(export_filepath)

    if not dir.is_dir():
        raise ValueError(f"'{dir}' is not a valid path to a folder.")

    # avoid overwriting existing config file

    def alter_export_filepath(filepath: Path):
        head, tail = os.path.split(filepath)
        name, ext = os.path.splitext(tail)
        suffix = 0

        while filepath.is_file():
            suffix += 1
            new_name = f"{name}_{str(suffix)}{ext}"
            filepath = Path(head) / new_name

        return filepath

    export_filepath: Path = alter_export_filepath(export_filepath)

    filenames_lst = []

    # traverse filenames in the directory
    # put video filenames into filenames_lst
    for file in os.listdir(dir):
        name, ext = os.path.splitext(file)
        if ext in known_video_formats:
            filenames_lst.append(file)
            print(f"recognised video file: {file}")
        else:
            print(f"error >>>>> not recognised file: `{file}`")

    # sort filenames_lst alphabetically
    filenames_lst = sorted(filenames_lst)
    template_str = ""
    count = 0

    for file in filenames_lst:
        name, ext = os.path.splitext(file)
        count += 1
        template_str += f"\n// {str(count)}\n"
        template_str += f"#{file}\n\n"
        template_str += "00:00, 00:00   // Low quality? (y/n): n\n" * 5

    with export_filepath.open(mode="w") as config:
        config.write(template_str)

    print(f"Successfully generated config template: {export_filepath}")
    return


if __name__ == "__main__":
    # change this to the path that leads to the folder containing all the video files
    # always use single forward slash in your path, even if you are using windows
    FOLDER_PATH = "PATH/TO/YOUR/VIDEO/FOLDER"

    # FOLDER_PATH = "/Volumes/MARK_HFS+_2T/UROP/verified/videos"

    # call the function
    generate_config_template(dir=FOLDER_PATH)
