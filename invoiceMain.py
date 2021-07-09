import os
from fileGenerator import FileGenerator
from ftplib import FTP
import csv

print('welcome to eBilling!')

#connect to ftp
ftp = FTP('ftp.haraldmueller.ch', 'schoolerinvoices', 'Berufsschule8005!')
ftp.cwd('out/AP18cHuber')
invoiceData = ''
path = 'C:\\Users\\ayesh\\git\\M122_LB2_Huber\\invoices'

#get .data file at position 0
filesineed = [filename for filename in ftp.nlst() if '.data' in filename]
if len(filesineed) > 0:
    ftp.retrbinary("RETR " + filesineed[0], open(path+'\\'+filesineed[0], 'wb').write)
    invoiceData = invoiceData+ path+ '\\' + filesineed[0]
    #ftp.delete(filesineed[0])
ftp.quit()
print('file has been downloaded!')

#separate csv
def readInvoiceData():
    with open(invoiceData, 'r', encoding="utf-8") as csvFile:
        rows = list(csv.reader(csvFile, delimiter=';'))
        csvFile.close()
        if len(rows) < 4:
            print('CSV file is corrupted')
        else:
            name = rows[0][0].split('_')
            if 'Rechnung' not in name[0] or len(rows[0]) != 6:
                print('Invoice number missing')
            elif 'Herkunft' not in rows[1][0] or len(rows[1]) != 8:
                print('Origin undefined or corrupted')
            elif 'Endkunde' not in rows[2][0] or len(rows[2]) != 5:
                print('Receiver missing or corrupted')
            elif 'RechnPos' not in rows[3][0] or len(rows[3]) != 7:
                print('Invoice line item missing or corrupted')
            else:
                for i in rows:
                    if i[0] == 'RechnPos' and len(i) != 7:
                        print('Invoice line item missing or corrupted')
                return rows

rows = readInvoiceData()
FileGenerator(rows)

ftp2 = FTP('134.119.225.245', '310721-297-zahlsystem', 'Berufsschule8005!')
ftp2.cwd('in/AP18cHuber')
path = 'C:\\Users\\ayesh\\git\\M122_LB2_Huber\\invoices'
files = os.listdir(path)
for file in files :
    with open(path +'\\'+ file, "rb") as file1 :
        newPath = path + '\\' + file
        ftp2.storbinary('STOR ' + file, file1)
        file1.close()
    #os.remove(newPath)
ftp2.quit()
#os.remove('C:\\Users\\ayesh\\git\\M122_LB2_Huber\\' + invoiceData)