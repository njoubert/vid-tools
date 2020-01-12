# Working work captured video clips



## Step 1: Given timestamp and folder, open the video at that timestamp.



# FFMPEG stuff

Show the container ("format") and all the streams
`ffprobe -v error -show_format -show_streams`

Show the container creation time
`ffprobe -v error -show_entries format_tags=creation_time -of default=noprint_wrappers=1:nokey=1`

Show the first video stream's duration
`ffprobe -v error -select_streams v:0 -show_entries stream=duration -of default=noprint_wrappers=1:nokey=1`

# References

If you wanna parse the actual GoPro metadata such as sensor metadata, you can!
https://github.com/stilldavid/gopro-utils
https://github.com/gopro/gpmf-parser

We use ffmpeg since its generic

