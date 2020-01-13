# Working work captured video clips

## Example Uses

```
./vid.py --datetime "2020-01-09T11:43:26.000000Z" --duration 10 /Volumes/\[2019\]\ Soepel/Footage/2020-01-09\ GOM/
```
To fix time offsets, you can create a `offset.txt` file per folder. This contains exactly one line containing an `HH:MM:SS.SSS` offset.

**Caveats:**

- This only shows clips that have video at that starting point. It does not select clips that fall within the duration but only after the start. 
- This does not manage having to cross clip boundaries.


## Step 1: Given timestamp and folder, open the video at that timestamp.



# FFPROBE stuff

Show the container ("format") and all the streams
`ffprobe -v error -show_format -show_streams`

Show the container creation time
`ffprobe -v error -show_entries format_tags=creation_time -of default=noprint_wrappers=1:nokey=1`

Show the first video stream's duration
`ffprobe -v error -select_streams v:0 -show_entries stream=duration -of default=noprint_wrappers=1:nokey=1`

# FFMPEG stuff

Merge two videos into one dual-screen video and scale both to 1080p: (merge audio tracks)
```
ffmpeg -i Angle1_OTSGP_GH010004.MP4 -i Angle2_FrontGP_GH010003.MP4 -filter_complex "[0:v]scale=1920:1080[lt];[1:v]scale=1920:1080[rt];[lt][rt]hstack,format=yuv420p[v];[0:a][1:a]amerge=inputs=2[a]" -map "[v]" -map "[a]" -ac 2 output.mp4
```

Merge two videos and crop the center to 1080p and encode HEVC: (merge audio tracks)
```
ffmpeg -i Angle1_OTSGP_GH010004.MP4 -i Angle2_FrontGP_GH010003.MP4 -filter_complex "[0:v]crop=1920:1080:436:220[lt];[1:v]crop=1920:1080:436:220[rt];[lt][rt]hstack,format=yuv420p[v];[0:a][1:a]amerge=inputs=2[a]" -map "[v]" -map "[a]" -ac 2 -c:v hevc -crf 0  output.mp4
```

Merge two videos and crop the center to 1080p and encode HEVC: (keep only audio track 1)
```
ffmpeg -i Angle1_OTSGP_GH010004.MP4 -i Angle2_FrontGP_GH010003.MP4 -filter_complex "[0:v]crop=1920:1080:436:220[lt];[1:v]crop=1920:1080:436:220[rt];[lt][rt]hstack,format=yuv420p[v]" -map "[v]" -map 0:a -c:v hevc -crf 0  output.mp4
```

Merge four videos into one quad-screen video: (merge audio tracks)
```
ffmpeg -i Angle1_OTSGP_GH010004.MP4 -i Angle2_FrontGP_GH010003.MP4 -i Angle3_Canon_MVI_1292.MOV -i Angle4_Cell_IMG_8087_cones_external.MOV -filter_complex "[0:v]scale=1920:1080[lt];[1:v]scale=1920:1080[rt];[lt][rt]hstack[top];[2:v][3:v]hstack[bottom];[top][bottom]vstack,format=yuv420p[v];[0:a][1:a][2:a][3:a]amerge=inputs=4[a]" -map "[v]" -map "[a]" -ac 2 output.mp4
```

Merge four videos into one quad-screen video, crop centers to 1080p, keep audio track 1
```
ffmpeg -i Angle1_OTSGP_GH010004.MP4 -i Angle2_FrontGP_GH010003.MP4 -i Angle3_Canon_MVI_1292.MOV -i Angle4_Cell_IMG_8087_cones_external.MOV -filter_complex "[0:v]crop=1920:1080:436:220[lt];[1:v]crop=1920:1080:436:220[rt];[lt][rt]hstack[top];[2:v][3:v]hstack[bottom];[top][bottom]vstack[v]" -map "[v]" -map 0:a -c:v hevc -crf 0  output.mp4

```

Merge four videos, high quality fast GPU encode
```
ffmpeg -i Angle1_OTSGP_GH010004.MP4 -i Angle2_FrontGP_GH010003.MP4 -i Angle3_Canon_MVI_1292.MOV -i Angle4_Cell_IMG_8087_cones_external.MOV -filter_complex "[0:v]crop=1920:1080:436:220[lt];[1:v]crop=1920:1080:436:220[rt];[lt][rt]hstack[top];[2:v][3:v]hstack[bottom];[top][bottom]vstack[v]" -map "[v]" -map 0:a -c:v hevc_videotoolbox -b:v 10000k -tag:v hvc1  output2.mp4
```

# References

If you wanna parse the actual GoPro metadata such as sensor metadata, you can!
https://github.com/stilldavid/gopro-utils
https://github.com/gopro/gpmf-parser

We use ffmpeg since its generic

