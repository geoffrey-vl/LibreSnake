# LibreSnake
Snake for LibreOffice

![classic snake](https://github.com/geoffrey-vl/libresnake/blob/master/screenshot.png)

## play the game
1. Download the snake.ods file
2. Open the file in libreoffice
3. Make sure you can run macro's in LibreOffice
4. Click in the navigation cells makred 'UP', 'DOWN', 'LEFT' or 'RIGHT' to navigate the snake

## requirements
Python runtime with uno package installed

## from source
When building from source...
In the source folder you'll find the excel file without scripts integrated
You will first need to insert the Snake.py macro into the snake.ods file,
or you can install the macro in your LibreOffice scripts folder (/usr/lib/libreoffice/share/Scripts/python/Snake.py).
To insert the macro into the ODS file run the insertMacroInODS.py script:

    python insertMacroInODS.py snake.ods

Next either run the game macro manually by running the StartEngine() method, or
attach the latter to the document-open event.