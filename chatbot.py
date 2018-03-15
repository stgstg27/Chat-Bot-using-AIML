# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 20:01:51 2018

@author: Saurabh
"""
# These are the libraries required during the assignment
import aiml
import json
import os
from nsetools import Nse
from weather import Weather
import urllib2
from pprint import pprint
"""from googlesearch import search"""
import webbrowser
 
weather = Weather()
	
# Create the kernel and learn AIML files
kernel = aiml.Kernel()

if os.path.isfile("bot_brain.brn"):
    kernel.bootstrap(brainFile = "bot_brain.brn")
else:
    kernel.bootstrap(learnFiles = "startup.xml", commands = "load aiml b")
    kernel.saveBrain("bot_brain.brn")
    

#unique_sequence = uniqueid()
# Press CTRL-C to break this loop
name_map =  raw_input("Hello there!! What is you name ??\n")
session_id = hash(name_map)

#print (session_id)
nse = Nse()
print("\n")
# Press CTRL-C to break this loop
while True:
    query = raw_input("Enter your message >> ")
    #evaluates various conditions according to query
    
    #checks for weather using wetaher-api
    if "WEATHER" in query or 'weather' in query or 'Weather' in query:
    	location = weather.lookup_by_location('dublin')
    	condition = location.condition()
    	print (condition.text())
    	print("\n")
    	 
    elif "GOOGLE" in query or 'google' in query or 'Google' in query:
    	#for using google using googlesearch-api
    	print ("What do you want to search in google?")
    	query=raw_input()
    	address="http://www.google.com/#q="
    	new_query=address+query
    	"""for j in search(query, tld="co.in", num=3, stop=1, pause=2):"""
    	webbrowser.open(new_query)
    	print("\n")
    elif "Remember that" in query:
    	#for remembering stuff 
        query_list = query.split()
        print ("Sure I will Remember that")
        #kernel.respond(query[-1]+" "+query,session_id)
        kernel.setPredicate(query_list[-1],query[14:],session_id)
        exDict = {query_list[-1]:query[14:]}
        #print (type(exDict))
        #print ("This is a remember query problem")
        with open(str(session_id), 'w') as file:
            file.write(json.dumps(exDict))
    elif "What did " in query:
        query_list = query.split()
        #answer = kernel.getPredicate(query_list[-1], session_id)
        jsonfile = ''
        with open(str(session_id), 'r') as file:
            jsonfile = json.loads(file.read())
        answer =  jsonfile[query_list[-1]]
        #print (answer)
        if answer is None:
            print ("Google Search")
        else:
       		print (answer) 
        
    elif "exit" in query:
    	break
    elif "Stock" in query or 'stock' in query:
    	#for using stockgogole-api
    	stock = raw_input("Please tell me the exact stock name\n")
    	St = nse.get_quote(stock)
    	try:
    		a = St['averagePrice']
    		b = St['buyPrice1']
    		c = St['sellPrice1']
	    	print ("Average Price:"),a
	    	print ("BuyPrice:"),b
	    	print ('SellPrice:'),c
	except:
		s = raw_input("Please type correct Stock name, Should I tell you about avaiable Stocks?")
		if s=='yes':
			pprint (nse.get_stock_codes())
	   
    else:
    	line = kernel.respond(query)
    	for j in line.split("."):
    		print (j)
            

	
