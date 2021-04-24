#!/bin/bash
# Argument no. 1 is the name of the PDF file
# Argument no. 2 is the time step between consecutive frames
# Argument no. 3 is the density expected by imagemagick

# Compile LaTeX source
pdflatex src/$1.tikz

# Fetch number of pages
page_no=$(pdftk $1.pdf dump_data | grep NumberOfPages | sed 's/[^0-9]*//')

# Remove old files
touch raw/foo.png
rm raw/*.png

# Convert all pages to PNGs
for ((i=0; i<=$page_no-1; i++))
    do
        convert -density $3 $1.pdf[$i] raw/$1-$i.png
    done

# Render frames into mp4
bash render.sh $1 $2
