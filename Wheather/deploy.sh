#!/bin/bash
echo "uploading headers_download_file.txt"
ampy put headers_download_file.txt
echo -e "Done.....\n"
echo " "

echo "uploading headers_download_page.txt"
ampy put headers_download_page.txt
echo -e "Done.....\n"
echo " "

echo "uploading headers_main_page.txt"
ampy put headers_main_page.txt
echo -e "Done.....\n"
echo " "-e 

echo "uploading html_closure_main_page.txt"
ampy put html_closure_main_page.txt
echo -e "Done.....\n"
echo " "
ampy ls
echo "uploading stub main.py"
ampy put main.py
echo -e "Done.....\n"
echo " "
ampy ls

echo "uploading mainAppConstants.py"
ampy put mainAppConstants.py
echo -e "Done.....\n"
echo " "
ampy ls

echo "uploading temperature.py"
ampy put temperature.py
echo -e "Done.....\n"
echo " "
ampy ls
echo "uploading readenv2.py"
ampy put readenv2.py
echo -e "Done.....\n"
echo " "
ampy ls
echo "uploading setwebserver.py"
ampy put setwebserver.py
echo -e "Done.....\n"
echo " "
ampy ls
echo "uploading activatenet.py"
ampy put activatenet.py
echo -e "Done.....\n"
echo " "
ampy ls
echo "uploading boot.py"
ampy put boot.py
echo -e "Done.....\n"
echo " "
ampy ls


