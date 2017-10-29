# encoding: utf-8

from nltk.stem.snowball import SnowballStemmer
#from nltk.stem.wordnet import WordNetLemmatizer

#c=lmtzr.lemmatize("cactuses")
#print c
import nltk
from nltk.corpus import stopwords
import codecs
import os
import re
import linecache
import math
from nltk.stem.wordnet import WordNetLemmatizer
stp=set(stopwords.words("english"))
st=['us','get',"all",'too','wow','eat','head','say', 'hello', 'tsp', 'tbsp', 'gm','gram', 'kg','tbs']
punctuations = [",",".","/",":",";",")","(","*","-",'"','?','\\',"!","&"]
wrong=0
#print len(stp)
#print len(st)

for i in range(len(st)):
	stp.add(st[i])
#lmtzr=WordNetLemmatizer()
#stemmer = SnowballStemmer("english")
#print len(stp)
vocab={}
allartic={}
post_count=0
pathname="eattreat classes/"
path = ['Bakery&Sweets/','Snacks/','Meats/','Organics/','Other/','Drinks/','Restaurants/']
tagsre=re.compile('<.*?>')

special_char = []
#spec = open('special_char.txt','r')
#for line in spec:
#	line = line.replace('\n','')
#	spec_arr = line.split('\t')
#	special_char.append([spec_arr[0],spec_arr[1]])
#print special_char
for p in range(len(path)):
	
	for filename in os.listdir(pathname+path[p]):
		array=[]
		words_article=[]
		inputfile=codecs.open(pathname+path[p]+filename,'r', encoding="utf-8")
		post_count+=1
		#for line in  inputfile:
		line = linecache.getline(pathname+path[p]+filename, 1)
		line=line.replace("\n","")
		article=line.split("\t")
		file=article[0]
		content_encoded=article[2]

		content = content_encoded.replace("\xe2\x80\x99","'").replace('\xe2\x82\xb9','Rs').replace('\xc3\xa8','e').replace('\xc3\x80','A').replace('\xc3\x82','A').replace('\xc3\x83','A').replace('\xc3\x84','A').replace('\xc3\xa0','a').replace('\xc3\xa1','a').replace('\xc3\xa2','a').replace('\xc3\xa3','a').replace('\xc3\xa4','a').replace('\xc3\xa5','a')
		#content = content.replace("\s#8217\s","'")
		content = re.sub("&#(\d+)(;|(?=\s))", "'", content)
		content = content.lower()

		content=re.sub(tagsre," ",content)
		while ("  " in content):
			content  = content.replace("  ",' ')

#		content = content.replace("’".decode('ascii'),"'")
		if ("'s" in content):
			content = content.replace("'s","")
		if ("'ve" in content):
			content = content.replace("'ve"," have")
		if ("'re" in content):
			content=content.replace("'re"," are")
		if ("n't" in content):
			content=content.replace("n't", " not")
		if ("s'" in content):
			content=content.replace("s'","")
		if ("'m" in content):
			content=content.replace("'m"," am")
		if ("'d" in content):
			content=content.replace("'d"," had")
		if ("'ll" in content):
			content=content.replace("'ll"," will")
		
		while ("  " in content):
			content  = content.replace("  ",' ')

		ofile=open("eattreat_cleanedcontent/"+file+".txt","w")
		
		#if post_count < 2:
#		print post_count
		for punct in punctuations:
			content = content.replace(punct,'')
		

		words_article=content.split(" ")
		clean_words=[]
		ofile.write(content)
		for term in words_article:
			
			if term not in stp and term != '':
				try:
					#lemaword=lmtzr.lemmatize(term)
					#lemaword=stemmer.stem(term)
#					output1 = re.sub(r'\d+', '', term)
					if term.endswith("s"):
						if term.endswith("es"):
							if term.endswith("ies"):
								term=term[:len(term)-len("ies")]
								term=term+"y"
							else:
								term=term[:len(term)-len("es")]
						else:
							term=term[:len(term)-1]
					clean_words.append(term)
					#print("normal word is "+term+"\t"+"stem word is "+output1)

				except(UnicodeDecodeError):
					wrong+=1
					print wrong
				#	print("unicode characyer "+term) 
		word_count=len(clean_words)
		article_counter={}
		#print clean_words
		for index,clean in enumerate(clean_words):
			if index < len(clean_words)-1:
				bigram = clean+'-'+clean_words[index+1]
				if bigram not in article_counter:
					article_counter.update({bigram:1})
				else:
					article_counter[bigram]+=1
			if index < len(clean_words)-2:
				trigram = clean+'-'+clean_words[index+1]+'-'+clean_words[index+2]
				if trigram not in article_counter:
					article_counter.update({trigram:1})
				else:
					article_counter[trigram]+=1
			
			if clean not in article_counter:
				article_counter.update({clean:1})
			else :
				article_counter[clean]+=1
		for e in article_counter:	
			if e not in vocab:
				vocab.update({e:1})
			else:
				vocab[e]+=1
		for key in article_counter:
			temp_value = article_counter[key]
			article_counter[key]=float(temp_value)/float(word_count)
			array.append([key,article_counter[key]])
		#print counter	
		if file not in allartic:
			allartic.update({file:array})
		#print clean_words
#print allartic['2674']
		
#tfidfscore={}
tfidfscore={}
for key in allartic:
	ids=key
	temp=[]
	ele = allartic[key]
	for jk in range(len(ele)):
		name=ele[jk][0]
		value=float(ele[jk][1]*math.log(float(post_count)/float(vocab[name])))
		temp.append([name,value])
	temp = sorted(temp, key = lambda x: float(x[1]),reverse=True)
	tfidfscore.update({ids:temp})
result_file = open("eattreat_tfidfstemmer/Score.txt","w")
for key in tfidfscore:
	element=tfidfscore[key]
	for value in range(15):
		if not  element[value][0].startswith(" "):
			count=element[value][0].count("-")
			if count ==0:
				try:
					string = key +'\t'+ element[value][0] +'\t'+str(element[value][1])+'\n'
					result_file.write(string)
				except(UnicodeDecodeError):
					string =key + "\t" + "unicode character" #+ element[value][0]
			if count == 1:
				try:
					string = key +'\t'+"\t"+"\t"+ element[value][0] +'\t'+str(element[value][1])+'\n'
					result_file.write(string)
				except(UnicodeDecodeError):
					string =key + "\t" + "unicode character" #+ element[value][0]
			if count==2:
				try:
					string = key +'\t'+"\t"+ "\t"+"\t"+"\t"+element[value][0] +'\t'+str(element[value][1])+'\n'
					result_file.write(string)
				except(UnicodeDecodeError):
					string =key + "\t" + "unicode character" #+ element[value][0]
	outputfile=open("eattreat_tfidfstemmer/"+key+".txt","w")
	outputfile.write(string+"\n")

