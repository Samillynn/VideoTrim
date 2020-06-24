import os
from pathlib import Path


def generate_config_template(dir: str, export_path: str = "config.txt"):
    dir = Path(dir)
    export_path = Path(export_path)

    if not dir.is_dir():
        raise ValueError(f"'{dir}' is not a valid path to a folder.")

    index = 0

    while export_path.is_file():
        index += 1
        head, tail = os.path.split(export_path)
        name, ext = os.path.splitext(tail)
        tail = f"{name}_{str(index)}{ext}"
        export_path = Path(head) / tail

    template_str = ""
    count = 0

    for file in os.listdir(dir):
        name, ext = os.path.splitext(file)
        if ext in (".mp4", ".flv", ".mov", ".avi", ".wmv", ".mkv"):
            count += 1
            print(f"recognised video file: {file}")

            template_str += f"\n// {str(count)}\n"
            template_str += f"#{file}\n\n"
            template_str += "00:00, 00:00\n" * 5
        else:
            print(f"error >>>>> not recognised file: `{file}`")

    with export_path.open(mode="w") as config:
        config.write(template_str)

    print(f"Successfully generated config template: {export_path}")
    return


if __name__ == "__main__":
    generate_config_template(dir="PATH/TO/YOUR/VIDEO/FOLDER",)
