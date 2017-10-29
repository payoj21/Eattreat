#!/usr/bin/env python
import math
def naivebayes(fileid,string_tags,dictionary,global_var) :
  import sys
  import os
  import codecs
  import json
  pathname="eattreat_nlp_taggenerator/"
  path = ['Bakery&Sweets/','Snacks/','Meats/','Organics/','Other/','Drinks/','Restaurants/']
  path1 = ['Bakery&Sweets','Snacks','Meats','Organics','Other','Drinks','Restaurants']
  dict_bakery =['bakery','cake','chocolate','dessert','sweet']
  dict_snacks =['cafe','street','chaat','food','snack','golgappe']
  dict_organics =['healthy','detox','vegan','salad','diet','dietary']
  dict_restaurants =['restaurant','bar','new','market','menu','eatery','kitchen','hotel','cafe']
  dict_meats =['chicken','biryani','seafood','prawn','fish','salmon','mutton','meat']
  dict_drinks =['rum','cocktail','mocktail','drink','beer','wine','drinking','tea','coffee','whisky','whiskey']
  dict_others =['festival','fest','travel']

  dict_top_keywords = {'Bakery&Sweets':dict_bakery,'Snacks':dict_snacks,'Meats':dict_meats,'Organics':dict_organics,'Other':dict_others,'Drinks':dict_drinks,'Restaurants':dict_restaurants}
  vocab = [{},{},{},{},{},{},{}]
  V =[]
  alltags=set()
  classoccur=[0.0,0.0,0.0,0.0,0.0,0.0,0.0]
  for p in range(len(path)):
    
    for filename in os.listdir(pathname+path[p]):
      if not filename.startswith('.'):
        classoccur[p]+=1
        inputfile=codecs.open(pathname+path[p]+filename,'r')
        for line in  inputfile:
          content=line.split("\t")
          post_id=content[0]
          post_title=content[1]
          post_tags=content[2]
          tags = post_tags.split(', ')
          terms_freq = dictionary[post_id]
#          print terms_freq
          for t in tags:
            if t != '':
              t_freq = terms_freq[t]
#              hyp_count = t.count('-')
              tt = t.split('-')
              t_score =0
              for ttt in tt:
                if ttt not in alltags:
                  alltags.add(ttt)
#                 if ttt in dict_top_keywords[path1[p]]:
#                   t_score = t_score + (hyp_count+1)
                if ttt not in vocab[p]:                                    
                  vocab[p].update({ttt:1})
                else:
                  vocab[p][ttt]+=1


    V.append(sum(vocab[p].values()))

  naive = [{},{},{},{},{},{},{}]
  lenalltags=len(alltags)
  
#---------------------DICTIONARIES------------------------------------------
  if global_var <2:
    for alpha in range(len(vocab)):
      class_dict = open('dictionaries/'+path1[alpha]+'.txt','a')
      for key in vocab[alpha]:
        class_dict.write(str(key)+'\t'+str(vocab[alpha][key])+'\n')

#---------------------------------------------------------------------------
  
  test_tags=[]

  total_tags=string_tags.split(", ")
  frequency = dictionary[fileid]
  sum1 = [0.0,0.0,0.0,0.0,0.0,0.0,0.0]
  for k in range(len(vocab)):
    s=0

    for e in total_tags:
      fterm_freq = frequency[e]
      hyphen_count = e.count('-')
      ee = e.split('-')
      e_score = 1
      for eee in ee:
        if eee not in alltags:
          alltags.add(eee)
          lenalltags+=1
        if eee in dict_top_keywords[path1[k]]:  
          e_score = (hyphen_count + 1)
        if eee not in vocab[k]:   
          vocab[k].update({eee:1})
          V[k]+=1
        else:
          vocab[k][eee]+=1
          V[k]+=1
        log_prior = math.lo
        naive[k].update({eee:e_score*float(float(1+vocab[k][eee])/float(lenalltags+V[k]))})
        s=s+math.logarithm(naive[k][eee])

    beta=float(s+math.logarithm(classoccur[k]/sum(classoccur)))
    sum1[k]=beta
    

  inputfile.close()

  max_value = max(sum1)
  max_index = sum1.index(max_value)

  classoccur[max_index]+=1

  print path1[max_index]
  return path1[max_index]
 
#naivebayes()