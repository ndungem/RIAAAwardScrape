RIAA Awards Data-Scraping Project

PREREQUISITES:
  * Python3
  * [WebDriver](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/) (to help with automating the browser)
      You will have to keep track of wherever this is downloaded, as it is a
      necessary argument to run the program.
  * [Selenium](https://pypi.org/project/selenium/)
      There are a lot of ways to download this. The easiest way will be through
      the terminal with this line if you have pip installed, but it’s not
      necessary (more info will be given in the link if you do not have pip):
      ```
          pip install selenium
      ```
  * [Mouse Jiggler](http://www.sticksoftware.com/software/Jiggler.html)
      This is just to keep the code running. If your computer sleeps,
      the code will terminate.

HOW TO RUN:
  To do this, you will need to use the riaaDataScrape.py file. This file has
  three arguments/flags:
  ```
     —award (-a): this flag chooses which award section to run.
     —outputfile (-o): this flag is the filename for the output file
                        where the data will reside. If using this path, make
                        sure to use .csv at the end of the file name. If this
                        is left out, it will go to a default path (riaaAwards.csv).
     —servicefile (-s): this flag is the WebDriver service path mentioned in the
                        prerequisites. This is required.
  ```
  There are two ways to run the data scraping process:
  
   * Run each award section separately. To do this, you will use the -a flag
    to run each one at a time. There are four different award
    sections: gold, mplat (multi-platinum), plat (platinum), diamond.
    I would recommend this so that you can monitor the process for each section.
        EXAMPLE:
	
   ```
            riaaDataScrape.py -a mplat -o <outputFile.csv> -s <serviceFilePath>
   ```
   * Run Gold first, then the rest of the awards. This will still use the -a
    flag for gold  — however, without the -a flag, it will run multi-platinum,
    platinum, and diamond by running the file getOtherAwards.py. This process
    has been partially tested, only because it will take very long to run.
      EXAMPLE:
   ```
          riaaDataScrape.py -o <outputFile.csv> -s <serviceFilePath>
   ```
AFTER IT RUNS:
  When you want to open the CSV file, you have to open it in a text editor
  first such as Notepad or TextEdit. Then, in the first line, you’ll add this:
	       ```
            sep=;
         ```
  This line makes sure that the text turns into a spreadsheet before you open
  it in Excel/Google Sheets.
