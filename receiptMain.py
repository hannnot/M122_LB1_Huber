import os
from fileGenerator import FileGenerator
from ftplib import FTP
import csv
from datetime import datetime
from line2 import Line2
print('welcome to eBilling!')
path = 'C:\\Users\\ayesh\\git\\M122_LB2_Huber\\invoices\\'
#separate csv
def readInvoiceData(invoiceD):
    with open(path +invoiceD, 'r', encoding="utf-8") as csvFile:
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



#connect to ftp
ftp = FTP('134.119.225.245', '310721-297-zahlsystem', 'Berufsschule8005!')
ftp.cwd('out/AP18cHuber')
receiptData = ''
receiptData = receiptData + path  + 'quittungsfile20210709_112003.txt'

with open(receiptData, 'r') as file :
    lines =file.readlines()
    xml = lines[0].split(' ')[2]
    dateTime = datetime.strptime(lines[0].split(' ')[0], '%y%m%d_%H%m%s')
    date = datetime.strftime(dateTime, '%d%m%Y')
    time = datetime.strftime(dateTime, '%H:%M:%S')
    txt = lines[1].split(' ')[2]

    invoiceFiles =os.listdir(path)
    rows = []
    for invoice in invoiceFiles :
        invoiceNr = xml.split('_')[1]
        if invoiceNr+ '.data' in invoice :
            rows = rows + readInvoiceData(invoice)

    l2 = Line2(rows[1])
    # TODO: send email with yagmail 
    # TODO: make zip archive with shutil.make_archive from invoice folder 
    # TODO: delete all files in invoice folder
    # TODO : now u're done


     
