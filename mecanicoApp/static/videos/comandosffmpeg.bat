ffmpeg -i drifting.mp4 -c:v libx264 -an -b:v 0.4M -s 1280x720 back.mp4

ffmpeg -i drifting.mp4 -c:v libx265 -an -b:v 0.4M -s 1280x720 back.265.mp4

ffmpeg -i drifting.mp4 -c:v vp9 -an -b:v 0.4M -s 1280x720 back.webm