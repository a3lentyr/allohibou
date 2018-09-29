import tempfile
import itertools as IT
import os
import random

# return a unique file name
def uniquify(path, sep = ''):
    def name_sequence():
        count = IT.count()
        yield ''
        while True:
            yield '{s}{n:d}'.format(s = sep, n = next(count))
    orig = tempfile._name_sequence 
    with tempfile._once_lock:
        tempfile._name_sequence = name_sequence()
        path = os.path.normpath(path)
        dirname, basename = os.path.split(path)
        filename, ext = os.path.splitext(basename)
        fd, filename = tempfile.mkstemp(dir = dirname, prefix = filename, suffix = ext)
        tempfile._name_sequence = orig
    return filename


def main():
	header = 'header.txt'
	header_file = open(header,'r')
	header_text = header_file.read()
	
	footer = 'footer.txt'
	footer_file = open(footer,'r')
	footer_text = footer_file.read()

	# forming list of places
	form_list=["triangle","carre","rond","losange"]
	color_list=["violet","orange","green"]
	places_list=[]
	for form in form_list:
		for color in color_list:
			places_list.append(form+"-"+color)
			
	data_dict={}
	
	for name in places_list:
		name_file = open(name+".svg",'r')
		name_text = name_file.read()
		data_dict[name]=name_text
		name_file.close()


	# Adding places
	content_text=""
	
	for name in places_list:
		x=random.randint(30,270)
		y=random.randint(30,230)
		content_text+='<g transform="translate('+str(x)+','+str(y)+')">' # placing it
		content_text+=data_dict[name]+'</g>' # content
		
	# Creating file
	new_path = uniquify('file.svg')
	new_file = open(new_path,'w')
	title = header_text+content_text+footer_text
	new_file.write(title)

	new_file.close()
	footer_file.close()
	header_file.close()
  
if __name__== "__main__":
  main()
