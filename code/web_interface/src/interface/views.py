from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from os import system as run
from os import path,getcwd,chdir
import time,mimetypes,tempfile,zipfile,subprocess,commands
from django.conf import settings
from wsgiref.util import FileWrapper
#from django.core.servers.basehttp import FileWrapper

# Create your views here.
def interface_home(request):
	a=commands.getstatusoutput("cd;cd files;pwd")[1]
	#a=commands.getstatusoutput("cd;cd Desktop;pwd")[1]
	chdir(a)
	#run("./script.sh")
	return render(request,"form.html",{})

def interface_download(request):
	a=commands.getstatusoutput("cd;cd files;pwd")[1]
	chdir(a)
	if request.method =="GET":
		email=request.GET.get('email')
		domain=request.META['HTTP_HOST']
		#send_mail('Subject here','Here is the message.','from@gmail.com',['to@email.com'],fail_silently=False,)
		email=""
		vlink=""
		pdflink=""
		category=""
		videotype=""
		if request.GET.get('videotype')==None:
			videotype=""
		else:
			videotype=request.GET.get('videotype')
		if request.GET.get('category')==None:
			category=""
		else:
			category=request.GET.get('category')
		if request.GET.get('vlink')==None:
			vlink=""
		else:
			vlink=request.GET.get('vlink')
		if request.GET.get('pdflink')==None:
			pdflink=""
		else:
			pdflink=request.GET.get('pdflink')
		if request.GET.get('email')==None:
			email=""
		else:
			email=request.GET.get('email')
		vlink.replace(" ","")
		pdflink.replace(" ","")
		site="http://"+domain+"/interface/convert/?vlink="+vlink+"&pdflink="+pdflink+"&email="+email+"&category="+category+"&videotype="+videotype
		context={
			"title":"Download completed and Conversion is going on....Please Wait...",
			"site":site,
			"progress":"20"
		}

		#time.sleep(3)
		#files script for downloading
		command=''
		if videotype=="1":
			command='rm -f download.mp4;chmod +x youtube_video.sh;./youtube_video.sh "'+vlink+'"'
		else:
			command='rm -f download.mp4;chmod +x other_video.sh;./other_video.sh "'+vlink+'"'
		run(command)
		command=''
		if pdflink=="":
			pass
			#command="chmod +x without_pdf.sh;./without_pdf.sh "+vlink
			#run(command)
		else:
			command='rm -f document.pdf;chmod +x download_pdf.sh;./download_pdf.sh "'+pdflink+'"'
			run(command)
		return render(request,"index.html",context)


def interface_convert(request):
	a=commands.getstatusoutput("cd;cd files;pwd")[1]
	chdir(a)
	if request.method =="GET":
		email=request.GET.get('email')
		domain=request.META['HTTP_HOST']
		email=""
		vlink=""
		pdflink=""
		category=""
		videotype=""
		if request.GET.get('videotype')==None:
			videotype=""
		else:
			videotype=request.GET.get('videotype')
		if request.GET.get('category')==None:
			category=""
		else:
			category=request.GET.get('category') 
		if request.GET.get('vlink')==None:
			vlink=""
		else:
			vlink=request.GET.get('vlink')
		if request.GET.get('pdflink')==None:
			pdflink=""
		else:
			pdflink=request.GET.get('pdflink')
		if request.GET.get('email')==None:
			email=""
		else:
			email=request.GET.get('email')
		vlink.replace(" ","")
		pdflink.replace(" ","")
		site="http://"+domain+"/interface/time/?vlink="+vlink+"&pdflink="+pdflink+"&email="+email+"&category="+category+"&videotype="+videotype
		run("rm -f video.mp4;chmod +x convert_video.sh;./convert_video.sh")
		if pdflink=="":
			#time.sleep(3)
			pass
		else:
			run("rm -f *.jpg;chmod +x pdf1.sh;./pdf1.sh;chmod +x pdf2.sh;./pdf2.sh;chmod +x pdf3.sh;./pdf3.sh;")#;chmod +x pdf2.sh;./pdf2.sh")
			#a=commands.getstatusoutput("pages=$(pdfinfo document.pdf | grep Pages | awk '{print $2}');echo $pages")
			#print a
			#run("rm -f inter*;rm -f common*;rm -f slide*;chmod + convert_pdf.sh;./convert_pdf.sh")
			#run("chmod +x download_with_pdf.sh;./download_with_pdf "+vlink+" "+pdflink)
		context={
			"title":"Conversion completed and Finding the transiton seconds....Please wait",
			"site":site,
			"progress":"40"
		}
		return render(request,"index.html",context)	
	

def interface_time(request):
	a=commands.getstatusoutput("cd;cd files;pwd")[1]
	chdir(a)
	if request.method =="GET":
		email=request.GET.get('email')
		domain=request.META['HTTP_HOST']
		vlink=""
		pdflink=""
		category=""
		videotype=""
		if request.GET.get('videotype')==None:
			videotype=""
		else:
			videotype=request.GET.get('videotype')
		if request.GET.get('category')==None:
			category=""
		else:
			category=request.GET.get('category') 
		if request.GET.get('vlink')==None:
			vlink=""
		else:
			vlink=request.GET.get('vlink')
		if request.GET.get('pdflink')==None:
			pdflink=""
		else:
			pdflink=request.GET.get('pdflink')
		if request.GET.get('email')==None:
			email=""
		else:
			email=request.GET.get('email')
		vlink.replace(" ","")
		pdflink.replace(" ","")
		site="http://"+domain+"/interface/compare/?vlink="+vlink+"&pdflink="+pdflink+"&email="+email+"&category="+category+"&videotype="+videotype
		#time.sleep(5)
		if category=="1":
			run("rm -f frame*.jpg;rm -f data.txt;python main.py;")
		if category=="2":
			run("rm -f frame*.jpg;rm -f data.txt;python general.py;")
		context={
			"title":"Slide Transition seconds has been figured out...Comparison with slides in going on..",
			"site":site,
			"progress":"75"
		}
		return render(request,"index.html",context)

def interface_compare(request):
	a=commands.getstatusoutput("cd;cd files;pwd")[1]
	chdir(a)
	max_ind=commands.getstatusoutput("pdfinfo document.pdf | grep Pages | awk '{print $2}'")[1]
	max_ind=int(max_ind)-1
	if request.method =="GET":
		email=request.GET.get('email')
		domain=request.META['HTTP_HOST']
		vlink=""
		pdflink="" 
		email=""
		category=""
		command=""
		videotype=""
		if request.GET.get('videotype')==None:
			videotype=""
		else:
			videotype=request.GET.get('videotype')
		if request.GET.get('category')==None:
			category=""
		else:
			category=request.GET.get('category')
		if request.GET.get('vlink')==None:
			vlink=""
		else:
			vlink=request.GET.get('vlink')
		if request.GET.get('pdflink')==None:
			pdflink=""
		else:
			pdflink=request.GET.get('pdflink')
		if request.GET.get('email')==None:
			email=""
		else:
			email=request.GET.get('email')
		#time.sleep(5)
		site="http://"+domain+"/interface/home"
		restart="http://"+domain+"/interface/again/?vlink="+vlink+"&pdflink="+pdflink+"&email="+email+"&category="+category+"&videotype="+videotype
		command="rm -f ans.csv;python slide_match.py "+str(max_ind)
		if pdflink=="":
			pass
			#run("chmod +x download_without_pdf.sh;./download_without_pdf "+vlink)
		else:
			#pass
			run(command)
		mail_list=[email]
		string=""
		data_file=""
		ans_file=""
		seconds=[]
		slides=[]
		sus_sec=""
		sus_sli=""
		if path.isfile("data.txt")==True:
			data_file="http://"+domain+"/interface/data.txt"
			seconds = [line.rstrip('\n') for line in open('data.txt')]
			string=string+"The suspectable transition seconds are\n"
			num_ele=len(seconds)
			for i in range(0,num_ele):
				if i != num_ele-1:
					sus_sec=sus_sec+seconds[i]+","
					string=string+seconds[i]+","
				else:
					sus_sec=sus_sec+seconds[i]
					string=string+seconds[i]
			#seconds = [line.rstrip('\n') for line in open('data.txt')]

		if path.isfile("ans.csv")==True:
			ans_file="http://"+domain+"/interface/ans.csv"
			slides = [line.rstrip('\n') for line in open('ans.csv')]
			string=string+"\nThe matched slide number \n"
			num_ele=len(slides)
			for i in range(0,num_ele):
				k=slides[i].split(",")
				if i != num_ele-1:
					sus_sli=sus_sli+k[0]+"-"+k[1]+","
					string=string+k[0]+"-"+k[1]+","
				else:
					sus_sli=sus_sli+k[0]+"-"+k[1]
					string=string+k[0]+"-"+k[1]
			#slides = [line.rstrip('\n') for line in open('ans.csv')]
		print string
		#send_mail('Results',string,'from@gmail.com',mail_list,fail_silently=False,)	
		context={
			"site":site,
			"restart":restart,
			"sus_sec":sus_sec,
			"sus_sli":sus_sli,
			"data_file":data_file,
			"ans_file":ans_file
		}
		return render(request,"final.html",context)

def interface_again(request):
	a=commands.getstatusoutput("cd;cd files;pwd")[1]
	chdir(a)
	if request.method=="GET":
		email=request.GET.get('email')
		domain=request.META['HTTP_HOST']
		vlink=""
		pdflink=""
		category=""
		videotype=""
		if request.GET.get('videotype')==None:
			videotype=""
		else:
			videotype=request.GET.get('videotype')
		if request.GET.get('category')==None:
			category=""
		else:
			category=request.GET.get('category') 
		if request.GET.get('vlink')==None:
			vlink=""
		else:
			vlink=request.GET.get('vlink')
		if request.GET.get('pdflink')==None:
			pdflink=""
		else:
			pdflink=request.GET.get('pdflink')
		if request.GET.get('email')==None:
			email=""
		else:
			email=request.GET.get('email')
		vlink=vlink.strip()
		pdflink=pdflink.strip()
		site="http://"+domain+"/interface/compare/?vlink="+vlink+"&pdflink="+pdflink+"&email="+email+"&category="+category+"&videotype="+videotype
		#time.sleep(3)
		#run("rm -f data.txt;rm -f ans.csv")
		#run("python main.py")
		if category=="1":
			run("rm -f data.txt;python main.py;")
		if category=="2":
			run("rm -f data.txt;python general.py;")
		context={
			"title":"Slide Transition seconds has been figured out...Comparison with slides in going on..",
			"site":site,
			"progress":"75"
		}
		return render(request,"index.html",context)

def seconds_file(request):
	a=commands.getstatusoutput("cd;cd files;pwd")[1]
	chdir(a)
	filename     = getcwd()+'/data.txt' # Select your file here.
	#print filename
	download_name ="data.txt"
	wrapper      = FileWrapper(open(filename))
	content_type = mimetypes.guess_type(filename)[0]
	response     = HttpResponse(wrapper,content_type=content_type)
	response['Content-Length']      = path.getsize(filename)    
	response['Content-Disposition'] = "attachment; filename=%s"%download_name
	return response

def slides_file(request):
	a=commands.getstatusoutput("cd;cd files;pwd")[1]
	chdir(a)
	filename     = getcwd()+'/ans.csv' # Select your file here.
	#print filename
	download_name ="ans.csv"
	wrapper      = FileWrapper(open(filename))
	content_type = mimetypes.guess_type(filename)[0]
	response     = HttpResponse(wrapper,content_type=content_type)
	response['Content-Length']      = path.getsize(filename)    
	response['Content-Disposition'] = "attachment; filename=%s"%download_name
	return response

def mail_to(request):
	a=commands.getstatusoutput("cd;pwd")[1]
	chdir(a)
	#a=commands.getstatusoutput("pdfinfo document.pdf | grep Pages | awk '{print $2}'")[1]
	#a=int(a)-1
	print a
	if request.method =="GET":
		email=request.GET.get('email')
		domain=request.META['HTTP_HOST']
		vlink=""
		pdflink=""
		category=""
		videotype=""
		if request.GET.get('videotype')==None:
			videotype=""
		else:
			videotype=request.GET.get('videotype')
		if request.GET.get('category')==None:
			category=""
		else:
			category=request.GET.get('category') 
		if request.GET.get('vlink')==None:
			vlink=""
		else:
			vlink=request.GET.get('vlink')
		if request.GET.get('pdflink')==None:
			pdflink=""
		else:
			pdflink=request.GET.get('pdflink')
		if request.GET.get('email')==None:
			email=""
		else:
			email=request.GET.get('email')
		vlink.replace(" ","")
		pdflink.replace(" ","")
		string=""
		if path.isfile("data.txt")==True:
			fr = [line.rstrip('\n') for line in open('data.txt')]
			string="The suspectable transition seconds are\n"
			for i in fr:
				string=string+i+"\n"

		if path.isfile("ans.csv")==True:
			fr = [line.rstrip('\n') for line in open('ans.csv')]
			string=string+"The matched slide number \n"
			for i in fr:
				string=string+i+"\n"
		#send_mail('Subject here','Here is the message.','from@gmail.com',['to@email.com'],fail_silently=False,)
		#site="http://"+domain+"/interface/compare/?vlink="+vlink+"&pdflink="+pdflink+"&email="+email
		#run("chmod + convert_pdf.sh;./convert_pdf.sh")
		#a=commands.getstatusoutput("chmod +x convert_pdf.sh;./convert_pdf.sh")
		#run("chmod +x pdf1.sh;./pdf1.sh;chmod +x pdf2.sh;./pdf2.sh;chmod +x pdf3.sh;./pdf3.sh;")#;chmod +x pdf2.sh;./pdf2.sh")
		#run("chmod +x pdf2.sh;./pdf2.sh;")
		command=''
		if videotype=="1":
			command='chmod +x youtube_video.sh;./youtube_video.sh "'+vlink+'"'
		else:
			command='chmod +x other_video.sh;./other_video.sh "'+vlink+'"'
		run(command)
		command=''
		if pdflink=="":
			pass
			#command="chmod +x without_pdf.sh;./without_pdf.sh "+vlink
			#run(command)
		else:
			command='chmod +x download_pdf.sh;./download_pdf.sh "'+pdflink+'"'
			run(command)
		return HttpResponse(string)
