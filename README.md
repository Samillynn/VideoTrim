# VideoTrim
_A python package to trim a large amount of videos conveniently using ffmpeg_

  ### Usage:
  **$ python trim.py [-h]  [-i infolder] [-o outfolder] [-c config.txt] [-w num_of_max_workers]**  
  _before run trim.py you first should write a configure file, which will tell the program how to trim your videos._  
  [See here to write a configure file for trim.py](#how-to-write-the-configuration-file)
  ### Options
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
        
  ### How to write the configuration file
    // config.txt example
    // comments can be written after '//'
    
    #demo.mp4                 // every video to be trimmed must follows an '#'
    
    4, 20, output1.mp4        // in the following lines, every line must consist 
                              // start_time, end_time, output_file_name(optional)
                              // **this line will trim from 4s to 20s of demo.mp4 to output1.mp4**
    
    1:13, 09:8, output2.mp4   // you can use a integer to set the trim time, 
                              // also you can format like hh:mm:ss
                             
    02:34, 07:24              // if you don't specify a output file name,
                              // the output file will be named demo{x}.mp4
                              // x means it is the xth output video using the current input video
                              
       
    #example.flv              // this program support different type of input video
    1, 4, example1.flv        // also different format of output video 
    134, 09:00
                        
     
    #another_example.mp4
    1, 2, 
    2, 3
    3, 4,
    4, 5,
    // ...
     
   ###Notes
   1. The program will not download the file if the output folder consists of the file  
      so feel free to run trim.py multiple times.
    
