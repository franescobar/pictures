#!/bin/bash
# Argument no. 1 is the name of the PDF file
# Argument no. 2 is the time step between consecutive frames

# Render frames into mp4
ffmpeg -r $2 -i raw/$1-%01d.png -c:a aac -b:a 256k -ar 44100 -c:v libx264 -pix_fmt yuv420p -preset faster -tune stillimage -vf "crop=trunc(iw/2)*2:trunc(ih/2)*2" $1.mp4
