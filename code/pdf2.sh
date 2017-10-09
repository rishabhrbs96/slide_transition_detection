#rm -f inter*
#rm -f slide*
#rm -f common*
#convert -density 300 document.pdf slide%d.jpg
counter=0
pages=$(pdfinfo document.pdf | grep Pages | awk '{print $2}')
((pages--))
until [ $counter -gt $pages ]
do
ffmpeg -i slide$(echo $counter).jpg -vf scale=640:360 image$(echo $counter).jpg
counter=$((counter+1))
done

