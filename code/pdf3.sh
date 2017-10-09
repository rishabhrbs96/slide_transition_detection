counter=0
pages=$(pdfinfo document.pdf | grep Pages | awk '{print $2}')
((pages--))
until [ $counter -gt $pages ]
do
#echo $counter
#ffmpeg -i slide$(echo $counter).jpg -vf scale=640:360 inter$(echo $counter).jpg
#ffmpeg -i image$(echo $counter).jpg -vf format=gray gray$(echo $counter).jpg
ffmpeg -i image$(echo $counter).jpg -vf "eq=contrast=1.0:brightness=-0.05:saturation=0.75" common$(echo $counter).jpg
#rm -f inter$(echo $counter).jpg
#rm -f slide$(echo $counter).jpg
counter=$((counter+1))
done

rm -f inter*.jpg
rm -f slide*.jpg
rm -f image*.jpg
