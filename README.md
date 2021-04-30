# SudokuScanner
Repository for the Real Time Sudoku Scanner Individual Project <br/> <br/>

# How to Run
##	Website
Access the website at https://sudokuscannerproject.web.app/. <br/> <br/>
## Local Machine
With Docker installed on your machine, simply run the following command which will pull and run the prebuilt image.
1.	 docker run -p 5000:5000 benmarkfrost/sudoku <br/> <br/>

Alternatively, pull the code from GitHub, and with Python 3 installed, run the following setup lines from the root folder.
1.	git clone https://github.com/BenMarkFrost/SudokuScanner
2.	cd SudokuScanner
3.	pip3 install -r requirements.txt
4.	pip3 install tensorflow==2.4.2
#### If running Linux:
---
5.	sudo apt-get update
6.	sudo apt-get install ffmpeg libsm6 libxext6 -y
---
###
7.	python app.py <br/> <br/>


Using either of these approaches, the server can then be accessed at localhost:5000 in your browser.
