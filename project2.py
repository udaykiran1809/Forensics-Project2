import os
import sys
import math
import struct

 # BMP possible error when calculating file sizes

 # Potentially need to include WinZIP


file_header = {
    'MPG': '000001B',
    'PDF': '25504446',
    'BMP': '424D',
    'GIF1': '474946383761',
    'GIF2': '474946383961',
    'JPG': 'FFD8FF',
    'DOCX': '504B030414000600',
    'AVI': '52494646',
    'PNG': '89504E470D0A1A0A',
    'ZIP': '504B0304'
    
}

file_footer = {
    'MPG1': '000001B7',
    'MPG2': '000001B9',
    'PDF1': '0A2525454F46000000',
    'PDF2': '0A2525454F460A000000',
    'PDF3': '0D0A2525454F460D0A000000',
    'PDF4': '0D2525454F460D000000',
    'GIF': '003B0000',
    'JPG': 'FFD90000',
    'DOCX': '504B0506',
    'PNG': '49454E44AE426082',
    'ZIP': '504B'
}

def FileRecovery(disk_hex):

    # Num of Files Found
    total_found = 0

    # Look for all headers
    for header in file_header:

        # Searching Location
        search = 0

        # Signature Location
        loc = disk_hex.find(file_header[header])

        while loc != -1:

            # MPG 
            if header == 'MPG':

                # Start of Sector
                if loc%512 == 0:

                    # Found File 
                    total_found = total_found + 1
                    
                    # File Footer Location
                    footer = disk_hex.find(file_footer['MPG1'], loc)
                    if footer == -1:
                        footer = disk_hex.find(file_footer['MPG2'], loc)
                    
                    # Get Entire File including length of footer
                    footer = footer + 7 

                    # Generating File Name
                    file_name = 'File' + str(total_found)+ '.mpg'

                    # Extracting File 
                    start_offset = int(loc / 2)
                    end_offset = int(math.ceil(footer / 2))
                    filesize = end_offset - start_offset
                    
                    # Printing Information
                    print(file_name + ", ",end='')
                    print('Start Offset: ' + str(hex(start_offset)) + ", ",end='')
                    print('End Offset: ' + str(hex(end_offset)))

                    File_Extract(start_offset,filesize,file_name)

                    search = footer
                else:
                    # If not start of sector move to the next search space
                    search = loc + 8

            # PDF
            if header == 'PDF':

                # Start of Sector
                if loc%512 == 0:

                    # Found File 
                    total_found = total_found + 1
                    
                    # File Footer Location and length of footer
                    footer = disk_hex.find(file_footer['PDF1'], loc)
                    footer_len = 11
                    if footer == -1:
                        footer = disk_hex.find(file_footer['PDF2'], loc)
                        footer_len = 13
                    if footer == -1:
                        footer = disk_hex.find(file_footer['PDF3'], loc)
                        footer_len = 17
                    if footer == -1:
                        footer = disk_hex.find(file_footer['PDF4'], loc)
                        footer_len = 13
                    
                    # Get Entire File including Footer
                    footer = footer + footer_len

                    # Generating File Name
                    file_name = 'File' + str(total_found)+ '.pdf'

                    # Extracting File 
                    start_offset = int(loc / 2)
                    end_offset = int(math.ceil(footer / 2))
                    filesize = end_offset - start_offset
                    
                    # Printing Information
                    print(file_name + ", ",end='')
                    print('Start Offset: ' + str(hex(start_offset)) + ", ",end='')
                    print('End Offset: ' + str(hex(end_offset)))

                    File_Extract(start_offset,filesize,file_name)

                    search = footer
                else:
                    # If not start of sector move to the next search space
                    search = loc + 8

            # BMP
            if header == 'BMP':

                # Start of Sector
                if loc%512 == 0:

                    # Found File 
                    total_found = total_found + 1
                    
                    # Calculate size of file from header
                    file_size = disk_hex[loc + 4: loc + 12]
                    file_size = struct.pack('<Q', file_size)
                    file_size = int(file_size, 16)

                    # Generating File Name
                    file_name = 'File' + str(total_found)+ '.bmp'

                    # Extracting File 
                    start_offset = int(loc / 2)
                    end_offset = start_offset + file_size
                    
                    # Printing Information
                    print(file_name + ", ",end='')
                    print('Start Offset: ' + str(hex(start_offset)) + ", ",end='')
                    print('End Offset: ' + str(hex(end_offset)))

                    File_Extract(start_offset,file_size,file_name)

                    search = end_offset
                else:
                    # If not start of sector move to the next search space
                    search = loc + 4

            # GIF87a
            if header == 'GIF1':

                # Start of Sector
                if loc%512 == 0:

                    # Found File 
                    total_found = total_found + 1
                    
                    # File Footer Location
                    footer = disk_hex.find(file_footer['GIF'], loc)
                    
                    # Get Entire File including Footer
                    footer = footer + 3

                    # Generating File Name
                    file_name = 'File' + str(total_found)+ '.gif'

                    # Extracting File 
                    start_offset = int(loc / 2)
                    end_offset = int(math.ceil(footer / 2))
                    filesize = end_offset - start_offset
                    
                    # Printing Information
                    print(file_name + ", ",end='')
                    print('Start Offset: ' + str(hex(start_offset)) + ", ",end='')
                    print('End Offset: ' + str(hex(end_offset)))

                    File_Extract(start_offset,filesize,file_name)

                    search = footer
                else:
                    # If not start of sector move to the next search space
                    search = loc + 12
            
            # GIF89a
            if header == 'GIF2':

                # Start of Sector
                if loc%512 == 0:

                    # Found File 
                    total_found = total_found + 1
                    
                    # File Footer Location
                    footer = disk_hex.find(file_footer['GIF'], loc)
                    
                    # Get Entire File including Footer
                    footer = footer + 3

                    # Generating File Name
                    file_name = 'File' + str(total_found)+ '.gif'

                    # Extracting File 
                    start_offset = int(loc / 2)
                    end_offset = int(math.ceil(footer / 2))
                    filesize = end_offset - start_offset
                    
                    # Printing Information
                    print(file_name + ", ",end='')
                    print('Start Offset: ' + str(hex(start_offset)) + ", ",end='')
                    print('End Offset: ' + str(hex(end_offset)))

                    File_Extract(start_offset,filesize,file_name)

                    search = footer
                else:
                    # If not start of sector move to the next search space
                    search = loc + 12

            # JPG
            if header == 'JPG':

                # Start of Sector
                if loc%512 == 0:

                    # Found File 
                    total_found = total_found + 1
                    
                    # File Footer Location
                    footer = disk_hex.find(file_footer['JPG'], loc)
                    
                    # Get Entire File including Footer
                    footer = footer + 3

                    # Generating File Name
                    file_name = 'File' + str(total_found)+ '.jpg'

                    # Extracting File 
                    start_offset = int(loc / 2)
                    end_offset = int(math.ceil(footer / 2))
                    filesize = end_offset - start_offset
                    
                    # Printing Information
                    print(file_name + ", ",end='')
                    print('Start Offset: ' + str(hex(start_offset)) + ", ",end='')
                    print('End Offset: ' + str(hex(end_offset)))

                    File_Extract(start_offset,filesize,file_name)

                    search = footer
                else:
                    # If not start of sector move to the next search space
                    search = loc + 6
            
            # DOCX
            if header == 'DOCX':

                # Start of Sector
                if loc%512 == 0:

                    # Found File 
                    total_found = total_found + 1
                    
                    # File Footer Location
                    footer = disk_hex.find(file_footer['DOCX'], loc)
                    
                    # Get Entire File including Footer
                    footer = footer + 43

                    # Generating File Name
                    file_name = 'File' + str(total_found)+ '.docx'

                    # Extracting File 
                    start_offset = int(loc / 2)
                    end_offset = int(math.ceil(footer / 2))
                    filesize = end_offset - start_offset
                    
                    # Printing Information
                    print(file_name + ", ", end='')
                    print('Start Offset: ' + str(hex(start_offset)) + ", ", end='')
                    print('End Offset: ' + str(hex(end_offset)))

                    File_Extract(start_offset,filesize,file_name)

                    search = footer
                else:
                    # If not start of sector move to the next search space
                    search = loc + 16

            # AVI
            if header == 'AVI':

                # Start of Sector
                if loc%512 == 0:

                    # Found File 
                    total_found = total_found + 1
                    
                    # COllecting File Size
                    file_size = disk_hex[loc + 8: loc + 16]
                    file_size = struct.pack('<Q', file_size)
                    file_size = int(file_size, 16)

                    # Generating File Name
                    file_name = 'File' + str(total_found)+ '.avi'

                    # Extracting File 
                    start_offset = int(loc / 2)
                    end_offset = start_offset + file_size
                    
                    # Printing Information
                    print(file_name + ", ", end='')
                    print('Start Offset: ' + str(hex(start_offset)) + ", ", end='')
                    print('End Offset: ' + str(hex(end_offset)))

                    File_Extract(start_offset,file_size,file_name)

                    search = end_offset
                else:
                    # If not start of sector move to the next search space
                    search = loc + 32

            # PNG
            if header == 'PNG':

                # Start of Sector
                if loc%512 == 0:

                    # Found File 
                    total_found = total_found + 1
                    
                    # File Footer Location
                    footer = disk_hex.find(file_footer['PNG'], loc)
                    
                    # Get Entire File including Footer
                    footer = footer + 15

                    # Generating File Name
                    file_name = 'File' + str(total_found)+ '.png'

                    # Extracting File 
                    start_offset = int(loc / 2)
                    end_offset = int(math.ceil(footer / 2))
                    filesize = end_offset - start_offset
                    
                    # Printing Information
                    print(file_name + ", ", end='')
                    print('Start Offset: ' + str(hex(start_offset)) + ", ", end='')
                    print('End Offset: ' + str(hex(end_offset)))

                    File_Extract(start_offset,filesize,file_name)

                    search = footer
                else:
                    # If not start of sector move to the next search space
                    search = loc + 16

            # ZIP
            if header == 'ZIP':

                # Start of Sector
                if loc%512 == 0:

                    # Found File 
                    total_found = total_found + 1
                    
                    # File Footer Location
                    footer = disk_hex.find(file_footer['ZIP'], loc)

                    # Get Entire File including Footer
                    footer = footer + 23

                    # Generating File Name
                    file_name = 'File' + str(total_found)+ '.zip'

                    # Extracting File 
                    start_offset = int(loc / 2)
                    end_offset = int(math.ceil(footer / 2))
                    filesize = end_offset - start_offset
                    
                    # Printing Information
                    print(file_name + ", ", end='')
                    print('Start Offset: ' + str(hex(start_offset)) + ", ", end='')
                    print('End Offset: ' + str(hex(end_offset)))

                    File_Extract(start_offset,filesize,file_name)

                    search = footer
                else:
                    # If not start of sector move to the next search space
                    search = loc + 8

        loc = disk_hex.find(file_header[header], search)

def File_Extract(start_offset,count, file_name):
    extraction_command = 'dd if=' + str(sys.argv[1]) + ' of=' + str(file_name) + ' bs=1 skip=' + str(start_offset) + ' count='+ str(count)
    os.system(extraction_command)

    generateHash(file_name)

def generateHash(inputFile):
    hash = 'sha256sum' + inputFile
    print('SHA-256: ', end='')
    os.system(hash)


if __name__ == "__main__":
    with open(sys.argv[1], 'rb') as disk_image:
        disk_data = disk_image.read().hex()
    disk_image.close()

    FileRecovery(disk_data)
    
