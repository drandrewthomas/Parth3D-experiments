ffmpeg.exe -framerate 30 -i ".\timelapseoutput\frame%%06d.jpg" -c:v libx264 -pix_fmt yuv420p -vf scale=1280:720 timelapse3d.mp4
