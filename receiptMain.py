import os
import sys
from fileGenerator import FileGenerator
from ftplib import FTP
import csv
from datetime import datetime
from line2 import Line2
import yagmail
import shutil

print('welcome to eBilling!')
path = 'C:\\Users\\ayesh\\git\\M122_LB2_Huber\\invoices\\'

def readInvoiceData(invoiceD):
    with open(path +invoiceD, 'r', encoding="utf-8") as csvFile:
        rows = list(csv.reader(csvFile, delimiter=';'))
        csvFile.close()
        if len(rows) < 4:
            print('CSV file is corrupted')
            sys.exit()
        else:
            name = rows[0][0].split('_')
            if 'Rechnung' not in name[0] or len(rows[0]) != 6:
                print('Invoice number missing')
                sys.exit()
            elif 'Herkunft' not in rows[1][0] or len(rows[1]) != 8:
                print('Origin undefined or corrupted')
                sys.exit()
            elif 'Endkunde' not in rows[2][0] or len(rows[2]) != 5:
                print('Receiver missing or corrupted')
                sys.exit()
            elif 'RechnPos' not in rows[3][0] or len(rows[3]) != 7:
                print('Invoice line item missing or corrupted')
                sys.exit()
            else:
                for i in rows:
                    if i[0] == 'RechnPos' and len(i) != 7:
                        print('Invoice line item missing or corrupted')
                        sys.exit()
                return rows

#connect to ftp
ftp = FTP('134.119.225.245', '310721-297-zahlsystem', 'Berufsschule8005!')
ftp.cwd('out/AP18cHuber')
receiptData = ''
#get .data file at position 0
filesineed = [filename for filename in ftp.nlst() if 'quittungsfile' in filename]
if len(filesineed) > 0:
    ftp.retrbinary("RETR " + filesineed[0], open(path  +filesineed[0], 'wb').write)
    receiptData = receiptData + path  + filesineed[0]
    ftp.delete(filesineed[0])
    ftp.quit()
    print('file has been downloaded!')
else: 
    sys.exit()


attachment = ''
attachmentName = ''
with open(receiptData, 'r') as file :
    lines =file.readlines()
    xml = lines[0].split(' ')[2]
    dateTime = datetime.strptime(lines[0].split(' ')[0], '%Y%m%d-%H%M%S')
    date = datetime.strftime(dateTime, '%d.%m.%Y')
    time = datetime.strftime(dateTime, '%H:%M:%S')
    txt = lines[1].split(' ')[2]

    invoiceFiles =os.listdir(path)
    rows = []
    for invoice in invoiceFiles :
        invoiceNr = xml.split('_')[1]
        if invoiceNr+ '.data' in invoice :
            rows = rows + readInvoiceData(invoice)

    l2 = Line2(rows[1])
    shutil.make_archive(invoiceNr, 'zip', root_dir=path)
    attachment = attachment+ 'C:\\Users\\ayesh\\git\\M122_LB2_Huber\\' + invoiceNr + '.zip'
    attachmentName = attachmentName + invoiceNr+ '.zip'
    yag = yagmail.SMTP('ayeshahuber@gmail.com',
                           '143Ash!!')
    yag.send(
        to=l2.email,
        subject="Erfolgte Verarbeitung Rechnung %s" % (invoiceNr),
        contents="<p>Sehr geehrte/r %s</p><br><p>Am %s um %s wurde die erfolgreiche Bearbeitung der Rechnung %s</p><p>vom Zahlungssystem in/AP18cHuber gemeldet.</p><br><p>Mit freundlichen Grüssen</p><br><p>A. Huber</p><p>TBZ</p>"% (l2.name, date, time, invoiceNr),
        attachments=attachment,
    )
    print('Email has been sent')
    file.close()

ftp2 = FTP('ftp.haraldmueller.ch', 'schoolerinvoices', 'Berufsschule8005!')
ftp2.cwd('in/AP18cHuber')

with open(attachment, "rb") as file1 :
    ftp2.storbinary('STOR ' + attachmentName, file1)
    file1.close()
    
ftp2.quit()

filesToDelete = os.listdir(path)
for file3 in filesToDelete :
    os.remove(path + file3)

os.remove(attachment)

     
