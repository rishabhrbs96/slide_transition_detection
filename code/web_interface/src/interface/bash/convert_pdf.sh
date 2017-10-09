convert -density 300 document.pdf slide%d.jpg
counter=0
pages=$(pdfinfo document.pdf | grep Pages | awk '{print $2}')
((pages--))
until [ $counter -gt $pages ]
do
echo $counter
ffmpeg -i slide$(echo $counter).jpg -vf scale=640:360 inter$(echo $counter).jpg
#ffmpeg -i image$(echo $counter).jpg -vf format=gray gray$(echo $counter).jpg
ffmpeg -i inter$(echo $counter).jpg -vf "eq=contrast=1.0:brightness=-0.05:saturation=0.75" common$(echo $counter).jpg 
((counter++))
done
	#ffmpeg -i $($b).jpg -vf scale=640:360 image$($b).jpg
rm inter*
rm slide*
