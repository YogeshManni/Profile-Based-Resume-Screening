import pandas as pd
import string,re
import PyPDF2
import textract
import matplotlib.pyplot as plt
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import numpy as np

#-------------- Data extraction process -----------------------#

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

#calling the function to open file and get Data
text = convert_pdf_to_txt("Resume.pdf")


#---------------Data Cleaning Process---------------------------#

#convert data into lowercase
text  = text.lower()

#Remove Numeric digits
text = re.sub(r'\d+','',text)

# Removing  punctuation from data
text = text.translate(str.maketrans('','',string.punctuation))

text = text.replace('\n',' ')

text = text.split(' ')
#-----------------Preparing a Dictionary containing the keywords for each profile ----------------#

keyWords_Dict = {'Quality/Six Sigma':['black belt','capability analysis','control charts','doe','dmaic','fishbone',
                              'gage r&r', 'green belt','ishikawa','iso','kaizen','kpi','lean','metrics',
                              'pdsa','performance improvement','process improvement','quality',
                              'quality circles','quality tools','root cause','six sigma',
                              'stability analysis','statistical analysis','tqm'],      
        'Operations management':['automation','bottleneck','constraints','cycle time','efficiency','fmea',
                                 'machinery','maintenance','manufacture','line balancing','oee','operations',
                                 'operations research','optimization','overall equipment effectiveness',
                                 'pfmea','process','process mapping','production','resources','safety',
                                 'stoppage','value stream mapping','utilization'],
        'Supply chain':['abc analysis','apics','customer','customs','delivery','distribution','eoq','epq',
                        'fleet','forecast','inventory','logistic','materials','outsourcing','procurement',
                        'reorder point','rout','safety stock','scheduling','shipping','stock','suppliers',
                        'third party logistics','transport','transportation','traffic','supply chain',
                        'vendor','warehouse','wip','work in progress'],
        'Project management':['administration','agile','budget','cost','direction','feasibility analysis',
                              'finance','kanban','leader','leadership','management','milestones','planning',
                              'pmi','pmp','problem','project','risk','schedule','scrum','stakeholders'],
        'Data analytics':['analytics','api','aws','big data','busines intelligence','clustering','code',
                          'coding','data','database','data mining','data science','deep learning','hadoop',
                          'hypothesis test','iot','internet','machine learning','modeling','nosql','nlp',
                          'predictive','programming','python','r','sql','tableau','text mining',
                          'visualuzation'],
        'Healthcare':['adverse events','care','clinic','cphq','ergonomics','healthcare',
                      'health care','health','hospital','human factors','medical','near misses',
                      'patient','reporting system'],
        'Web Development':['Jquery','javascript','css','html','angular','react','vue.js','web']              
                      }


#---------------------------Processing the data and getting useful scores for each profile ---------------------------#


#Initialize a list to store scores
scores = []
sigma,operations,supply,pro_mgmt,data_analytic,heath,web = 0,0,0,0,0,0,0

#Now loop over the Data
for profile in keyWords_Dict.keys():
        if(profile == 'Quality/Six Sigma'):
            for word in keyWords_Dict[profile]:
                if(word in text):
                    sigma+=1
            scores.append(sigma)

        elif(profile == 'Operations management') :
            for word in keyWords_Dict[profile]:
                if(word in text):
                    operations+=1
            scores.append(operations)

        elif(profile == 'Supply chain'):
            for word in keyWords_Dict[profile]:
                if(word in text):
                    supply+=1
            scores.append(supply)

        elif(profile == 'Project management'):
            for word in keyWords_Dict[profile]:
                if(word in text):
                    pro_mgmt+=1
            scores.append(pro_mgmt)

        elif(profile == 'Data analytics'):
            for word in keyWords_Dict[profile]:
                if(word in text):
                    data_analytic+=1
            scores.append(data_analytic)

        elif(profile == 'Healthcare'):
            for word in keyWords_Dict[profile]:
                if(word in text):
                    heath+=1
            scores.append(heath)
            
        elif(profile == 'Web Development'):
            for word in keyWords_Dict[profile]:
                if(word in text):
                    web+=1
            scores.append(web)        


#---------Here comes the use of pandas, we will make data frame for our final scores ------------------------#

dataPresented = pd.DataFrame(scores,index = keyWords_Dict.keys(),columns = ['Scores'])  
dataPresented = dataPresented[(dataPresented.T != 0).any()]
print(dataPresented)
#--------Now, lets represent the extracted data in a visual way i.e PIE CHART -------------------------------------#


#finding the max scored profile to popout its pie piece
explodeList = [0] * dataPresented.shape[0]
ind =  np.argmax(dataPresented.values)
explodeList[ind] = 0.1
explode = tuple(explodeList)


# Creating Pie Chart
pie = plt.figure(figsize=(10,10))
plt.pie(dataPresented['Scores'], labels=dataPresented.index , explode = explode, autopct=lambda p: '{:.1f}%'.format(round(p)) if p > 0 else '',shadow=True,startangle=90)
plt.title('Profile Wise Resume Screening')
plt.axis('equal')
plt.show()

# Save pie chart as a .png file
pie.savefig('Resume_Screening_PieChart.png')




