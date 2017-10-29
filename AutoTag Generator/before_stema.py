import os
for file in os.listdir("eattreat_tfidfstemmer/"):
	if not file.startswith('.'):
		os.remove("eattreat_tfidfstemmer/"+file)
for file1 in os.listdir("eattreat_category/"):
	if not file1.startswith('.'):
		os.remove("eattreat_category/"+file1)
for file2 in os.listdir("dictionaries/"):
	if not file2.startswith('.'):
		os.remove("dictionaries/"+file2)