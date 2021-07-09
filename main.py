from fileGenerator import FileGenerator
from ftplib import FTP
import re
import csv

print('welcome to eBilling!')

#connect to ftp
ftp = FTP('ftp.haraldmueller.ch', 'schoolerinvoices', 'Berufsschule8005!')
ftp.cwd('out/AP18cHuber')
print(ftp.dir())

#get .data file at position 0
filesineed = [filename for filename in ftp.nlst() if '.data' in filename]
if len(filesineed) > 0:
    ftp.retrbinary("RETR " + filesineed[0], open(filesineed[0], 'wb').write)
ftp.quit()
print('file has been downloaded!')

#separate csv
def readInvoiceData():
    with open('rechnung21003.data', 'r', encoding="utf-8") as csvFile:
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
