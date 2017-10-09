rm -f inter*.jpg
rm -f slide*.jpg
rm -f common*.jpg
rm -f image*.jpg
convert -density 300 document.pdf slide%d.jpg

