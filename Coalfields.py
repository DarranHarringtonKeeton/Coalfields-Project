#============================================#
# UK Coalfields Analysis                     #
#                                            #
# (c) Darran Harrington-Keeton December 2020 #
#============================================#
# Module import:
import csv
import requests
import lxml.html as lxm
# scrape:
# nmrs webpages used:
# https://www.nmrs.org.uk/resources/britains-nationalised-coal-mines-from-1947/ncb-collieries-england/
# https://www.nmrs.org.uk/resources/britains-nationalised-coal-mines-from-1947/ncb-collieries-scotland/
# https://www.nmrs.org.uk/resources/britains-nationalised-coal-mines-from-1947/ncb-collieries-wales/
#++++++++++++++++++++++++++++++++++++++++++++#
inptcllry = []
#Scrape Websites:
print("Scraping nmrs websites for data tables.")
eng = 'http://www.nmrs.org.uk/resources/britains-nationalised-coal-mines-from-1947/ncb-collieries-england/'
sco = 'https://www.nmrs.org.uk/resources/britains-nationalised-coal-mines-from-1947/ncb-collieries-scotland/'
wal = 'https://www.nmrs.org.uk/resources/britains-nationalised-coal-mines-from-1947/ncb-collieries-wales/'
# Mitigate 403 Forbidden with:
england = requests.get(eng, headers= {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
scotland = requests.get(sco, headers= {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
wales = requests.get(wal, headers= {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
cllry_eng = lxm.fromstring(england.content)
cllry_sco = lxm.fromstring(scotland.content)
cllry_wal = lxm.fromstring(wales.content)
#Parse data that are stored between <tr>..</tr> of HTML:
inptcllry_e = cllry_eng.xpath('//tr')
inptcllry_s = cllry_sco.xpath('//tr')
inptcllry_w = cllry_wal.xpath('//tr')
# Check
# print([len(T) for T in inptcllry[:12]])
for itm1 in inptcllry_e[0]:
    appnd1 = appnd1.text_content()
    inptcllry.append(appnd1)

#for itm1 in inptcllry_e[1:]:
#    appnd1 = itm1.text_content()
#    inptcllry.append(appnd1)    
#for itm2 in inptcllry_s[1:]:
#    appnd2 = itm2.text_content()
#    inptcllry.append(appnd2)
#for itm3 in inptcllry_w[1:]:
#    appnd3 = itm3.text_content()
#    inptcllry.append(appnd3)



# Sheffield Hallamshire Data - Already processed... DHK - December 2020
inptcflds = open('C:/Users/darra/OneDrive/Documents/Projects/Coalfields.csv')
#++++++++++++++++++++++++++++++++++++++++++++#
# Meta Data:  
# Data Source - https://www.nmrs.org.uk/
# Scraped from: [21/12/2020]
# https://www.nmrs.org.uk/resources/britains-nationalised-coal-mines-from-1947/ncb-collieries-england/
# https://www.nmrs.org.uk/resources/britains-nationalised-coal-mines-from-1947/ncb-collieries-scotland/
# https://www.nmrs.org.uk/resources/britains-nationalised-coal-mines-from-1947/ncb-collieries-wales/
#++++++++++++++++++++++++++++++++++++++++++++#
# Open files
#inptcllry = open('C:/Users/darra/OneDrive/Documents/Projects/UKCollieriesTestforbuild.txt')
#inptcllry = open('C:/Users/darra/OneDrive/Documents/Projects/UKCollieries.txt')

# Create Lists from imports:
print('Importing saved Data Tables')
coalfields = list(csv.reader(inptcflds))
#collieries = list(inptcllry)

# Analysis Tool 1 - List and indeces
def analysis1(anvr1):
    for cy in anvr1:
        ix = anvr1.index(cy)
        print(ix,":",cy[0])

# Other Variables
cleanselist1 = []
coltable1 = []
coltable2 = []

# Primary Cleane Tool - Remove HTML markup remnants from import
def cleanse1(clns1):
    for dx in clns1:
        dx[0] = dx[0].replace('\n\n\n',',')            
        cleanselist1.append(dx[0])
    print('Cleanse Complete')
    return cleanselist1
    #temp for build and test:
    print(cleanselist1)

def cleansenotrequired(clns1):
    for dx in clns1:
        if dx[0] == '<table>' or \
        dx[0] == '<tbody>' or \
        dx[0] == '<td width="130">' or \
        dx[0] == '<td width="200">' or \
        dx[0] == '<td width="150">' or \
        dx[0] == '<td width="80">' or \
        dx[0] == '<td width="100">' or \
        dx[0] == '<tr>' or \
        dx[0] == '</tr>' or \
        dx[0] == '</table>' or \
        dx[0] == '</tbody>':
            continue
        if dx[0] == '<td></td>':
            dx[0] = '-'
        if dx[0] == '<td>' or \
        dx[0] == '</td>':
            continue
        if dx[0][0:12:] == '<h4><strong>':
            dx[0] = dx[0][12::]
        if dx[0][-28::] == '<br />(Merged)</strong></h4>':   
            dx[0] = 'Closed(Merged)' 
        if dx[0][-14::] == '</strong></h4>':   
            dx[0] = dx[0][:-14:]             
        if dx[0][0:4:] == '<td>':
            dx[0] = dx[0][4::]
        if dx[0][-5::] == '</td>':
            dx[0] = dx[0][:-5:]
        dx[0] = dx[0].replace('&amp;','and')            
        cleanselist1.append(dx[0])
    print('Cleanse Complete')
    return cleanselist1

def Add_keys(adky):
    n = 0
    for q in adky:
        idnm = str(n).rjust(4, '0')
        q.insert(0, "CY" + idnm)
        if q[0]== "CY0000":
            q[0] = "Colliery_id"
        n += 1
        print(q)   # For test only - NB: not a list

def cr8tbl(crtbl):
    #cleanse1(collieries)
    cnt1 = 0
    cnt2 = 7
    print('Creating Table')
    while 1 == 1:
        x = len(crtbl)
        fnlst = crtbl[cnt1:cnt2]
        coltable2.append(fnlst)
        if cnt2 >= x:
            break
        cnt1 += 7
        cnt2 += 7

    #Add_keys(coltable2) 
    #  
    #print('Writing table to file')
    #with open('C:\\py\\colls1.csv', 'w', newline='') as csvfl:
    #    csv.writer(csvfl, delimiter=',').writerows(coltable2)
    #    csvfl.close()

#+++++++++++++++++++++++
#  Next Steps:
#  Cleanse Profile
#  NB Leadng 0s in CY_id
#+++++++++++++++++++++++

#print("Analysis 1:") # list out import - wth markup      
#analysis1(collieries)

#####################################################

#Execute:
print(inptcllry_e)
print(inptcllry)
#print(coltable2)

#Testing:
#print(inptcllry)
#analysis1(inptcllry)
#cleanse1(collieries)

print("Finished")