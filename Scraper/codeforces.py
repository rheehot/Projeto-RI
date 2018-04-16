import requests
import bs4 as bs
import re
import util
    
request = requests.get("http://codeforces.com/problemset/problem/949/A")
page = bs.BeautifulSoup(request.content, "html.parser")
    
#Container da descricao do problema
problem = page.find("div", {"class" : "problem-statement"})

name = problem.find("div", {"class" : "title"})
problemName = name.text

time = problem.find("div", {"class" : "time-limit"})
timeText = time.text
problemTime = timeText.replace("time limit per test", "")

memory = problem.find("div", {"class" : "memory-limit"})
memoryText = memory.text
problemMemory = memoryText.replace("memory limit per test", "")

description = problem.findAll("div")[10]
problemDescripton = description.text

inputDescripton = problem.find("div", {"class" : "input-specification"})
problemInput = inputDescripton.text[5:]

outputDescripton = problem.find("div", {"class" : "output-specification"})
problemOutput = outputDescripton.text[6:]

sampleTest = problem.find("div", {"class" : "sample-test"})
samplesInput = sampleTest.findAll("div", {"class" : "input"})
samplesOutput = sampleTest.findAll("div", {"class" : "output"})
problemSamples = ""

for i in range(len(samplesInput)):
    problemSamples += util.treatStr(samplesInput[i]) + "\n" + util.treatStr(samplesOutput[i]) + "\n\n"