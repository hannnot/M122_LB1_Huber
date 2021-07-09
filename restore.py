#get .data file at position 0
filesineed = [filename for filename in ftp.nlst() if 'quittungsfile' in filename]
if len(filesineed) > 0:
    ftp.retrbinary("RETR " + filesineed[0], open(path  +filesineed[0], 'wb').write)
    
    #ftp.delete(filesineed[0])
ftp.quit()
print('file has been downloaded!')
