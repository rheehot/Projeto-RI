import bs4 as bs
import requests
from Extractor import util

def wcipeg(page, link, uniqueId):
    #request = requests.get("https://wcipeg.com/problem/dt16l1p1")
    #page = bs.BeautifulSoup(request.content, "html.parser")
    
    problem = page.find("div", {"id": "descContent"})
    problemSidebar = page.find("div", {"id": "descSidebar"})
    
    dataT = {}
    
    title = page.title
    title = title.text
    problemName = title.replace("PEG Judge - ", "")
    
    #contents
    elements = problem.findAll(["h3", "p", "pre", "li","table"])
    
    if len(elements) == 0:
        elements = problem.findAll()
        elements = elements[1:]
    #Existem casos q o primeiro elemento é nome da universidade ou coisa do tipo.
    elif elements[0].name in ["h3", "table"]:
        elements = elements[1:]
        
    elementTitle = "Description"
    elementContent = ""
    inputFlag = False
    OutputFlag = False
    for element in elements:
        if element.name == "h3":
            if "Input" in element.text:
                if not inputFlag:
                    inputFlag = True
                else:
                    break
            
            if "Output" in element.text:
                if not OutputFlag:
                    OutputFlag = True
                else:
                    break
            
            if "Sample Input" in element.text:
                if elementTitle == "Example":
                    elementContent += element.text + "\n"
                else:
                    dataT[elementTitle] = elementContent[:-1]
                    elementTitle = "Example"
                    elementContent = "Sample Input \n"
            elif "Sample Output" in element.text:
                elementContent += element.text + "\n"
            else:
                dataT[elementTitle] = elementContent[:-1]
                elementTitle = element.text
                elementContent = ""
        else:
            elementContent += element.text + "\n"
            
    dataT[elementTitle] = elementContent[:-1]
            
    limits = problemSidebar.findAll("p")
    
    problemTime = util.findBetween(limits[3].text, "Time Limit: ", "\n")
    problemMemory = util.findBetween(limits[3].text, "Memory Limit: ", "\n")
    
    dataT["Title"] = problemName
    dataT["Time Limit"] = problemTime
    dataT["Memory Limit"] = problemMemory
    dataT["Problem"] = util.getText(problem) + "\n" + util.getText(problemSidebar)
    dataT["URL"] = link
    
    data = {}
    data[uniqueId] = dataT
    
    util.loadData(data)