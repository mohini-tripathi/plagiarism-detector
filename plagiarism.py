from flask import Flask, request, render_template
import re  #regular expression
import math

app = Flask("__name__") #Flask constructor takes the name of current module (__name__) as argument.

q = ""

@app.route("/") # displays the index page accessible at '/' & tells the application which URL should call the associated function.
def loadPage():
	return render_template('index.html', query="")

@app.route("/", methods=['POST'])
def cosineSimilarity():
	
	UniqueWordSet = []
	matchPercentage = 0

	
	inputQuery = request.form['query']
	lowercaseQuery = inputQuery.lower()

	queryWordList = re.sub("[^\w]", " ",lowercaseQuery).split()			#Replace punctuation by space and split
	# queryWordList = map(str, queryWordList)	 re.sub(pattern,repl,string)				#This was causing divide by zero error

	for word in queryWordList:
		if word not in UniqueWordSet:
			UniqueWordSet.append(word)


	fd = open("database1.txt", "r")
	database1 = fd.read().lower()

	databaseWordList = re.sub("[^\w]", " ",database1).split()	#Replace punctuation by space and split
	# databaseWordList = map(str, databaseWordList)			#And this also leads to divide by zero error

	for word in databaseWordList:
		if word not in UniqueWordSet:
			UniqueWordSet.append(word)


	queryTF = []
	databaseTF = []

	for word in UniqueWordSet:
		queryTfCounter = 0
		databaseTfCounter = 0

		for word2 in queryWordList:
			if word == word2:
				queryTfCounter += 1
		queryTF.append(queryTfCounter)

		for word2 in databaseWordList:
			if word == word2:
				databaseTfCounter += 1
		databaseTF.append(databaseTfCounter)

	dotProduct = 0
	for i in range (len(queryTF)):
		dotProduct += queryTF[i]*databaseTF[i]

	queryVectorMagnitude = 0
	for i in range (len(queryTF)):
		queryVectorMagnitude += queryTF[i]**2
	queryVectorMagnitude = math.sqrt(queryVectorMagnitude)

	databaseVectorMagnitude = 0
	for i in range (len(databaseTF)):
		databaseVectorMagnitude += databaseTF[i]**2
	databaseVectorMagnitude = math.sqrt(databaseVectorMagnitude)

	matchPercentage = (float)(dotProduct / (queryVectorMagnitude * databaseVectorMagnitude))*100

	result = "Input query text matches %0.02f%% with database."%matchPercentage

	return render_template('index.html', query=inputQuery, result=result)
app.debug = True
app.run() # four arguements : host, port, debug, options
app.run(debug = True)


# Let :
#     a : [x1, y1, z1]
#     b : [x2, y2, z2]

# (Theta) = (x1*x2 + y1*y2 + z1*z2)/
#          sqrt((x1^2 + y1^2 + z1^2))*sqrt((x2^2 + y2^2 + z2^2))
