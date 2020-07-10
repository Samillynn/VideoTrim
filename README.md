# Video Trimer

_A python package to trim a large amount of videos conveniently using `ffmpeg`_

### Dependency
  - [FFmpeg](https://ffmpeg.org/download.html)

### Usage:

```
python trim.py [-h]  [-i infolder] [-o outfolder] [-c config.txt] [-w num_of_max_workers]
```

 >before run trim.py you first should write a configure file, which will tell the program how to trim your videos.
 >
 >See [here](#how-to-write-the-configuration-file) on how to write a trimming configure file for `trim.py`

### Command Line Options

> You can use `trim.py` with or without Command Line.
>
> You can edit the variables in `trim.py` to avoid using Command Line arguments.

```
-h, --help:     
    seek help about how to use the program

-i, --infolder:    
    configure where the program finds your input videos, default is the current folder

-o, --outfoler:    
    configure where the program output your videos, default is the current folder

-c, --config:      
    locate your config.txt, default is './config.txt'

-w, --max_workers:
    configure the maxium processes the program can use, default is 4
```

### How to write the trimming configuration file

- To generate a template trimming config file automatically, use [generate_config_template.py](generate_config_template.py)

```
// comments can be written after '//'

#demo.mp4                 // every video to be trimmed must follows an '#'

4, 20, output1.mp4        // in the following lines, every line must consist
                          // start_time, end_time, output_file_name(optional)
                          // this line will trim from 4s to 20s of demo.mp4 to output1.mp4

1:13, 09:8, output2.mp4   // you can use a integer to set the trim time
                          // also you can format like hh:mm:ss

02:34, 07:24              // if you don't specify a output file name,
                          // the output file will be named demo{x}.mp4
                          // x means it is the xth output video using the current input video


#example.flv              // this program support different type of input video
1, 4, example1.flv        // also different format of output video
134, 09:00

```

### Use `video_list_generation.py` to extract Video Metadata

- Get metadata of all videos inside a `video_folder`, and write to `video_metadata_lst.json`.

- `video_metadata_lst.json` will be saved to the `video_folder`.

- Existing `video_metadata_lst.json` inside the target folder will be overwritten.

Example Output:
```json
[
    {
        "filepath": "/Users/mark/Downloads/vid-d/videos/zwHslNAuyPo.mp4",
        "filename": "zwHslNAuyPo",
        "ext": ".mp4",
        "width": 1280,
        "height": 720,
        "duration": 234.22,
        "fps": 30
    },
    {
        "filepath": "/Users/mark/Downloads/vid-d/videos/zr0Y4wv_-LU.mp4",
        "filename": "zr0Y4wv_-LU",
        "ext": ".mp4",
        "width": 1280,
        "height": 720,
        "duration": 720.0,
        "fps": 30
    }
]
```

### Additional Notes

- The program will not trim the file again if the clip already exist in the output folder. So, feel free to run `trim.py` multiple times.
