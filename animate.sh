#!/bin/bash
# Argument no. 1 is the name of the PDF file
# Argument no. 2 is the time step between consecutive frames

# Compile LaTeX source
pdflatex src/$1.tikz

# Fetch number of pages
page_no=$(pdftk $1.pdf dump_data | grep NumberOfPages | sed 's/[^0-9]*//')

# Remove old files
touch raw/foo.txt
rm raw/*

# Convert all pages to PNGs
for ((i=0; i<=$page_no-1; i++))
    do
        convert -density 600 $1.pdf[$i] raw/$1-$i.png
    done

# Render frames into mp4
ffmpeg -r 1/$2 -i raw/$1-%01d.png -c:a aac -b:a 256k -ar 44100 -c:v libx264 -pix_fmt yuv420p -preset faster -tune stillimage -vf "crop=trunc(iw/2)*2:trunc(ih/2)*2" $1.mp4
