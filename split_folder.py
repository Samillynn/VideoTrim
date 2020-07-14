import shutil
import json
import os
from pathlib import Path
import subprocess


def split_into_folders(json_filepath: str, from_folder: str, to_folder_base: str):
    from_folder = Path(from_folder)
    to_folder_base = Path(to_folder_base)
    json_filepath = Path(json_filepath)
    assert from_folder.is_dir()
    assert to_folder_base.is_dir()
    assert json_filepath.is_file()

    with json_filepath.open() as f:
        vid_lst: list = json.load(f)

    vid_lst = sorted(vid_lst, key=lambda x: (x["duration"], x["filename"]))

    counter = 0
    folder_count = 1
    folder_prefix = "bilibili_"
    # folder_prefix = "youtube_"
    dst_folder_path: Path = Path("")

    for video in vid_lst:
        filename = video.get("filename") + video.get("ext")
        filepath = from_folder / filename
        if filepath.is_file():
            counter += 1
            print(counter)
            print(f"Moving {filepath}")
            print(f"...vid duration: {video.get('duration')}s")
        else:
            print(f"{filepath} not found")
            continue

        if counter == 1:
            # create a new folder
            if folder_count <= 9:
                folder_suffix = f"00{str(folder_count)}"
            elif 10 <= folder_count <= 99:
                folder_suffix = f"0{str(folder_count)}"
            else:
                folder_suffix = str(folder_count)
            # new folder name
            dst_folder_name = f"{folder_prefix}{folder_suffix}"
            dst_folder_path: Path = to_folder_base / dst_folder_name
            try:
                if not dst_folder_path.is_dir():
                    os.mkdir(dst_folder_path)
                    print(f">>>> new dir created: {dst_folder_path}")
                else:
                    print(f"{dst_folder_path} dir alr exist")
            except Exception as err:
                print("creating directory failed")
                print(err)
                return

            # copy file
            try:
                new_filepath: Path = dst_folder_path / filename
                if new_filepath.is_file():
                    print(f"{new_filepath} alr exist")
                    continue
                else:
                    # shutil.copyfile(filepath, new_filepath)
                    subprocess.call(["mv", filepath, new_filepath])
                    print(f"...move successful\n")

            except Exception as err:
                print("copy file failed")
                print(err)
                return

        elif 1 < counter <= 99:
            # copy file
            try:
                new_filepath: Path = dst_folder_path / filename
                if new_filepath.is_file():
                    print(f"{new_filepath} alr exist")
                    continue
                else:
                    # shutil.copyfile(filepath, new_filepath)
                    subprocess.call(["mv", filepath, new_filepath])
                    print(f"...move successful\n")
            except Exception as err:
                print("copy file failed")
                print(err)
                return
        elif counter == 100:
            # set counter to zero
            counter = 0
            # folder_count next
            folder_count += 1
            # copy file
            try:
                new_filepath: Path = dst_folder_path / filename
                if new_filepath.is_file():
                    print(f"{new_filepath} alr exist")
                    continue
                else:
                    # shutil.copyfile(filepath, new_filepath)
                    subprocess.call(["mv", filepath, new_filepath])
                    print(f"...move successful\n")
            except Exception as err:
                print("copy file failed")
                print(err)
                return

        else:
            print("unexpected: something is wrong")
            return


if __name__ == "__main__":
    json_filepath = (
        "/home/UROP/data_urop/bilibili_copy/trimmed_videos/video_metadata_lst.json"
    )
    from_folder = "/home/UROP/data_urop/bilibili_copy/trimmed_videos"
    to_folder_base = (
        "/home/UROP/shared_drive/UROP_CV_2020_Shared/Video_Folders/Trimmed_All_Videos"
    )
    split_into_folders(json_filepath, from_folder, to_folder_base)
