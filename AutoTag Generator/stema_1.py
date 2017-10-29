#!/usr/bin/env python
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
from bs4 import BeautifulSoup
import sys
from classifier import naivebayes

rest_type =['bistro','café','restaurant','brewery','buffet','cafe','parlour','dessert parlor','casual dining','dhaba','food truck','lounge','pub','bar','pop up','deli','rooftop']
type_of_meal = ['tea','wine','chocolate','drink','beverage','breakfast','brunch','dessert','dinner','lunch','party','snacks','quick bite']
areas = ['east','west','north','south','nagar','market','chowk','bazaar']
stp=set(stopwords.words("english"))
st=['posted','pm','am','pay','they','timing','their','them','us','follow','get',"all",'too','wow','eat','head','say', 'hello','tablespoon','teaspoon', 'tsp', 'tbsp', 'gm','gram', 'kg','tbs', 'inr',"explore",'mg',"011",'full',"plate","approx","022","033","044",'0120','+91','91']
punctuations = [",",".","/",":",";",")","(","*","-",'"','?','\\',"!","'",'--','—','$'] 
wrong=0

for i in range(len(st)):
	stp.add(st[i])

vocab={}
allartic={}
key_class={}
post_count=0
pathname="eattreat classes/"
path = ['Bakery&Sweets/','Snacks/','Meats/','Organics/','Other/','Drinks/','Restaurants/','test_data/']
tagsre=re.compile('<.*?>')
recipere = re.compile('<p>(.*?)</p>')
special_char = []
dict_term_freq = {}

def tag_generator(u,b,t,q):
	final_tags = []
	tri_deleted_tags = set()
	bi_deleted_tags = set()
	uni_deleted_tags = set()

#-----------------------QUADGRAM-------------------------
	if q != []:
		
		for ele in q:			
			tag_terms = ele.split('-')
			t1 = tag_terms[0]+'-'+tag_terms[1]+'-'+tag_terms[2]
			t2 = tag_terms[1]+'-'+tag_terms[2]+'-'+tag_terms[3]
			if t1 in t and t2 in t:
				final_tags.append(ele)
				t11 = tag_terms[0]+'-'+tag_terms[1]
				t12 = tag_terms[1]+'-'+tag_terms[2]
				t21 = tag_terms[1]+'-'+tag_terms[2]
				t22 = tag_terms[2]+'-'+tag_terms[3]
				if t11 in b:
					bi_deleted_tags.add(t11)
				if t12 in b:
					bi_deleted_tags.add(t12)
				if t21 in b:
					bi_deleted_tags.add(t21)
				if t22 in b:
					bi_deleted_tags.add(t22)
				if tag_terms[0] in u:
					uni_deleted_tags.add(tag_terms[0])
				if tag_terms[1] in u:
					uni_deleted_tags.add(tag_terms[1])
				if tag_terms[2] in u:
					uni_deleted_tags.add(tag_terms[2])
				if tag_terms[3] in u:	
					uni_deleted_tags.add(tag_terms[3])
				
				if t1 not in tri_deleted_tags:
					tri_deleted_tags.add(t1)	
				if t2 not in tri_deleted_tags:
					tri_deleted_tags.add(t2)
		if tri_deleted_tags != []:
			for i in tri_deleted_tags:
				t.remove(i)
		if bi_deleted_tags != []:
			for i in bi_deleted_tags:
				if i in b:
					b.remove(i)
		if uni_deleted_tags != []:
			for i in uni_deleted_tags:
				if i in u:
					u.remove(i)
#---------------------TRIGRAM-------------------------------------		
	if t != []:
		for ele in t:			
			tag_terms = ele.split('-')
			t1 = tag_terms[0]+'-'+tag_terms[1]
			t2 = tag_terms[1]+'-'+tag_terms[2]
			if tag_terms[2] == 'recipe':
				final_tags.append(ele)
				bi_deleted_tags.add(t1)
				bi_deleted_tags.add(t2)
				uni_deleted_tags.add(tag_terms[0])
				uni_deleted_tags.add(tag_terms[1])
				uni_deleted_tags.add(tag_terms[2])

			else:
				if t1 in b and t2 in b:
					final_tags.append(ele)
					if tag_terms[0] in u:			
						uni_deleted_tags.add(tag_terms[0])
					if tag_terms[1] in u:
						uni_deleted_tags.add(tag_terms[1])
					if tag_terms[2] in u:			
						uni_deleted_tags.add(tag_terms[2])

					if t1 not in bi_deleted_tags:
						bi_deleted_tags.add(t1)	
					if t2 not in bi_deleted_tags:
						bi_deleted_tags.add(t2)
		
		if bi_deleted_tags != []:
			for i in bi_deleted_tags:
				if i in b:
					b.remove(i)
		if uni_deleted_tags != []:
			for i in uni_deleted_tags:
				if i in u:
					u.remove(i)

#-----------------BIRGRAM-----------------------------------------
	if b != []:
		
		for ele in b:			
			tag_terms = ele.split('-')
			t1 = tag_terms[0]
			t2 = tag_terms[1]
			if t1 in rest_type or t2 in rest_type or t1 in areas or t2 in areas:
				final_tags.append(ele)
				if t1 in u and t1 not in uni_deleted_tags:
					uni_deleted_tags.add(t1)	
				if t2 in u and t2 not in uni_deleted_tags:
					uni_deleted_tags.add(t2)
			else:
#				print t1, t2
				if t1 in u and t2 in u:
					final_tags.append(ele)
					if t1 not in uni_deleted_tags:
						uni_deleted_tags.add(t1)	
					if t2 not in uni_deleted_tags:
						uni_deleted_tags.add(t2)
#					print uni_deleted_tags
		if uni_deleted_tags != []:
#			print u 
			for i in uni_deleted_tags:
#				print i
				if i in u:
					u.remove(i)


#----------------------UNIGRAM----------------------------------
	if u != []:
#		print final_tags, u				
		for index, ele in enumerate(u):
			if ele in rest_type or ele in type_of_meal:
				final_tags.append(ele)
				f = ele
				u.remove(f)
			else:
				tag_counts = len(final_tags)
				if tag_counts < 7:
					uni_range = 6-tag_counts
				if index < uni_range:
					final_tags.append(u[index])
			
	return final_tags				


for filepath in range(len(path)):
	
	for filename in os.listdir(pathname+path[filepath]):
		if not filename.startswith('.'):
			array=[]
			words_article=[]
			inputfile=codecs.open(pathname+path[filepath]+filename,'r', encoding="utf-8")
			post_count+=1
			line = linecache.getline(pathname+path[filepath]+filename, 1)
			if line.endswith("\t"):
				line=line[:len(line)-len("\t")]
			line=line.replace("\n","")
			article=line.split("\t")
			file=article[0]
#			print filename, file, path[filepath]
			key_class.update({file:path[filepath]})
			
			articlename=article[1]
			content_encoded=article[2]
			articlename=articlename.lower()
			countss=0
			instatrend = ['#instagram trend','#instagramtrend','#instatrend']
			for ins in instatrend:
				if ins in articlename:
					countss+=1
					soup= BeautifulSoup(article[2],"html.parser")
					textt=soup.find_all("h4")
					for tt in textt:
						try:
							content+=tt.lower()
						except:
							pass
					content=content.lower()


				else:
					content = content_encoded.replace("\xc2\xa0"," ").replace("’","'").replace("\xe2\x80\xb2","'").replace("&#8211","'").replace("\xe2\x80\x99","'").replace('\xe2\x82\xb9','Rs').replace('\xc3\xa9','e').replace('\xc3\x80','A').replace('\xc3\x82','A').replace('\xc3\x83','A').replace('\xc3\x84','A').replace('\xc3\xa0','a').replace('\xc3\xa1','a').replace('\xc3\xa2','a').replace('\xc3\xa3','a').replace('\xc3\xa4','a').replace('\xc3\xa5','a')
					content = re.sub("&#(\d+)(;|(?=\s))", "'", content)
					content = content.lower()
					if 'yumprint' in content or '<strong>the element' in content or '<strong>element' in content:
						content_paras=re.findall('<p>(.*?)</p>',content)
						if len(content_paras) !=0:
							content = content_paras[0]
							content = re.sub(tagsre," ",content)
						else:
							content = ''
					else:
						content=re.sub(tagsre," ",content)

			content=content+' '+article[1].lower()
			content=content.replace('nbsp','')
			content=content.replace('&amp','and')
			content=content.replace('&','and')
			while ("  " in content):
				content  = content.replace("  ",' ')

			if ("'s" in content):
				content = content.replace("'s","s")
			if ("'ve" in content):
				content = content.replace("'ve"," have")
			if ("'re" in content):
				content=content.replace("'re"," are")
			if ("n't" in content):
				content=content.replace("n't", " not")
			if ("s'" in content):
				content=content.replace("s'","s")
			if ("'m" in content):
				content=content.replace("'m"," am")
			if ("'d" in content):
				content=content.replace("'d"," had")
			if ("'ll" in content):
				content=content.replace("'ll"," will")
			
			ofile=open("eattreat_cleanedcontent/"+file+".txt","w")
			
			for punct in punctuations:
				content = content.replace(punct,'')
			
			while ("  " in content):
				content  = content.replace("  ",' ')


			words_article=content.split(" ")
			clean_words=[]
			ofile.write(content)
			for term in words_article:
				if term.isdigit() and len(term) >2:
					pass
				else:

					if term not in stp and term != '':
						'''	lemaword=lmtzr.lemmatize(term)
						lemaword=stemmer.stem(term)
						output1 = re.sub(r'\d+', '', term)

						if word ends with 's'

						if word ends with 'es' then check 
							if s, ss, sh, ch, x, z before 'e' 
								remove 'es'
						
							if word ends with 'ves'
								replace 'ves' with 'fe' or 'f'

							if word ends with 'ies'
								if word == calories
									remove 's'
								else
									replace 'ies' with 'y'
							if word end with 'oes'
								remove 's'
						else 
							remove s	 
						'''

						try:
							if term.endswith("s"):
								#sprint term
								if term.endswith("es"):
									
									if term.endswith("ses") or term.endswith("shes") or term.endswith("ches") or term.endswith("xes") or term.endswith("zes"):
										term = term[:len(term)-len("es")]
									else:
										if term.endswith("ves"):
											term= term[:len(term)-len("ves")]
											term= term+"f"
										else:
											if term.endswith("ies"):
												if term == 'calories':
													pass
												else:
													term=term[:len(term)-len("ies")]
													term=term+"y"
											else:
												if term.endswith('oes'):
													term=term[:len(term)-len("es")]
												else:
													term=term[:len(term)-1]

										#print term
										#print term
								else:
									if term=='christmas':
										term = term
									else:
										if term.endswith('ss') or term.endswith('ous') or term.endswith('us') or term.endswith('os'):
											term = term
										else:
											term=term[:len(term)-1]

							clean_words.append(term)

						except(UnicodeDecodeError):
							wrong+=1
							print wrong

			word_count=len(clean_words)
			article_counter={}
			
			#print clean_words

			for index,clean in enumerate(clean_words):

	# ------------------BIGRAM-------------------------------------------------------			

				if index < len(clean_words)-1:
					bigram = clean+'-'+clean_words[index+1]
					if bigram not in article_counter:
						article_counter.update({bigram:1})
					else:
						article_counter[bigram]+=1

	# ------------------TRIGRAM------------------------------------------------------			
				
				if index < len(clean_words)-2:
					if word_count <50:
						if clean_words[index+2] == 'recipe':
							trigram = clean+'-'+clean_words[index+1]+'-'+clean_words[index+2]
							if trigram not in article_counter:
								article_counter.update({trigram:1})
							else:
								article_counter[trigram]+=1
					else:
						trigram = clean+'-'+clean_words[index+1]+'-'+clean_words[index+2]
						if trigram not in article_counter:
							article_counter.update({trigram:1})
						else:
							article_counter[trigram]+=1

	# ------------------QUADGRAM------------------------------------------------------			

				if index < len(clean_words)-3:
					if word_count < 100:
						if clean_words[index+3] == 'recipe':
							quadgram = clean+'-'+clean_words[index+1]+'-'+clean_words[index+2]+'-'+clean_words[index+3]
							if quadgram not in article_counter:
								article_counter.update({quadgram:1})
							else:
								article_counter[quadgram]+=1
					else:
						quadram = clean+'-'+clean_words[index+1]+'-'+clean_words[index+2]+'-'+clean_words[index+3]
						if quadram not in article_counter:
							article_counter.update({quadram:1})
						else:
								article_counter[quadram]+=1

	#-------------------UNIGRAM-------------------------------------------------------

				if clean not in article_counter:
					article_counter.update({clean:1})
				else :
					article_counter[clean]+=1

	#-------------------DOCUMENT FREQUENCY--------------------------------------------				

			for e in article_counter:	
				if e not in vocab:
					vocab.update({e:1})
				else:
					vocab[e]+=1

	#-----------------------TF----------------

			for key in article_counter:
				temp_value = article_counter[key]
				article_counter[key]=temp_value 
				array.append([key,article_counter[key],word_count])
			#print counter	
			if file not in allartic:
				allartic.update({file:array})



tfidfscore={}


#------TFIDF-----------------------------------------------
for key in allartic:
	ids=key
	temp=[]
	ele = allartic[key]
	for jk in range(len(ele)):
		name=ele[jk][0]
		value=float(ele[jk][1]*math.log(float(post_count)/float(vocab[name])))
		no_of_words = ele[jk][2]
		temp.append([name,value,no_of_words,ele[jk][1]])
	temp = sorted(temp, key = lambda x: float(x[1]),reverse=True)
	tfidfscore.update({ids:temp})
result_file = open("eattreat_tfidfstemmer/Score.txt","w")

#----------------TAG GENERATER---------------------------------
for key in tfidfscore:
	dict_id_freq = {}
	element=tfidfscore[key]
	unigram_counter = []
	bigram_counter = []
	trigram_counter = []
	quadgram_counter = []
#	words_counter = element[value][2]	
	if len(tfidfscore[key])>14:
		iterations = 15
	else:
		iterations = len(tfidfscore[key])
	for value in range(iterations):
		
		dict_id_freq.update({element[value][0]:element[value][3]})
		if not element[value][0].startswith(" "):
			count=element[value][0].count("-")
			if count ==0:
				try:
					unigram_counter.append(element[value][0])
					string = key +'\t'+ element[value][0] +'\t'+str(element[value][1])+'\t'+'\t'+'\t'+'\t'+'\t'+'\t'+'\t'+str(element[value][2])+'\n' #comment this 
					result_file.write(string) #comment this
				except(UnicodeDecodeError):
					string =key + "\t" + "unicode character" #+ element[value][0]
			if count == 1:
				try:
					bigram_counter.append(element[value][0])
					string = key +'\t'+'\t'+'\t'+ element[value][0] +'\t'+str(element[value][1])+'\t'+'\t'+'\t'+'\t'+'\t'+str(element[value][2])+'\n' #comment this
					result_file.write(string) #comment this
				except(UnicodeDecodeError):
					string =key + "\t" + "unicode character" #+ element[value][0]
			if count==2:
				try:
					trigram_counter.append(element[value][0])
					string = key +'\t'+'\t'+ '\t'+'\t'+'\t'+element[value][0] +'\t'+str(element[value][1])+'\t'+'\t'+'\t'+str(element[value][2])+'\n' #comment this
					result_file.write(string) #comment this
				except(UnicodeDecodeError):
					string =key + "\t" + "unicode character" #+ element[value][0]
			if count==3:
				try:
					quadgram_counter.append(element[value][0])
					string = key +'\t'+'\t'+'\t'+ '\t'+'\t'+'\t'+'\t'+element[value][0] +'\t'+str(element[value][1])+'\t'+str(element[value][2])+'\n' #comment this
					result_file.write(string) #comment this
				except(UnicodeDecodeError):
					string =key + "\t" + "unicode character" #+ element[value][0]


	dict_term_freq.update({key:dict_id_freq})
	
	article_tag = tag_generator(unigram_counter,bigram_counter,trigram_counter,quadgram_counter)
	outputfile=open("eattreat_tfidfstemmer/Tags.txt","a")
	file_class = key_class[key]
	output=open("eattreat_nlp_taggenerator/"+file_class+key+'.txt','w')
	output.write(key+'\t\t')
	for tag_index,article in enumerate(article_tag):
		outputfile.write(key+'\t'+article+"\n")
		if tag_index > 0:
			output.write(', '+article)
		else:
			output.write(article)
	output.write('\t'+file_class+'\n')
category_outfile = open('eattreat_category/categories.txt','a')
global_var = 1
for filename in os.listdir('eattreat_nlp_taggenerator/test_data/'):
	if not filename.startswith('.'):
		inputfile=codecs.open('eattreat_nlp_taggenerator/test_data/'+filename,'r', encoding="utf-8")
		line = linecache.getline('eattreat_nlp_taggenerator/test_data/'+filename, 1)
		line_elements = line.split('\t')
		test_data_tags = line_elements[2]
		category = naivebayes(line_elements[0],test_data_tags, dict_term_freq,global_var)
		global_var+=1
	#	print line_elements[0]+'\t'+test_data_tags+'\t'+category
		category_outfile.write(line_elements[0]+'\t'+test_data_tags+'\t'+category+'\n')

















