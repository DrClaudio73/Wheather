#!/bin/bash
echo "uploading headers_download_file.txt"
ampy put headers_download_file.txt
echo -e "Done.....\n"
echo " "

echo "uploading headers_download_page.txt"
ampy put headers_download_page.txt
echo -e "Done.....\n"
echo " "

echo "uploading headers_main_pageESP32.txt"
ampy put headers_main_pageESP32.txt
echo -e "Done.....\n"
echo " "

echo "uploading headers_main_pageESP8266.txt"
ampy put headers_main_pageESP8266.txt
echo -e "Done.....\n"
echo " "

echo "uploading html_closure_main_page.txt"
ampy put html_closure_main_page.txt
echo -e "Done.....\n"
echo " "

echo "uploading main.py"
ampy put main.py
echo -e "Done.....\n"
echo " "

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
echo "uploading readenv.py"
ampy put readenv.py
echo -e "Done.....\n"
echo " "
ampy ls
echo "uploading Wheather.py"
ampy put Wheather.py
echo -e "Done.....\n"
echo " "
ampy ls

echo "uploading activateNet.py"
ampy put activateNet.py
echo -e "Done.....\n"
echo " "
ampy ls
echo "uploading boot.py"
ampy put boot.py
echo -e "Done.....\n"
echo " "
ampy ls

echo "uploading credentials.py"
ampy put credentials.py
echo -e "Done.....\n"
echo " "