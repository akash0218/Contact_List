<div align="center">
<h1>Contact List</h1>
<h3>A Python App Based on SQLite3 and Tkinter</h3>
</div>

# Languages Used
* Python 3
* SQL

# Requirements
* Python 3 with `Tkinter` enabled
* Runs on any `platform` or `OS` supported by Python

# Installation
* This is a `Python3` app and has no external dependencies other than the standard library.

* To use this app anyone can either use the **binary** or just by executing the **.Py** file

* In case of **Virtual Environment** user should install `datetime` module from Pypi

  ```
  > pip install datetime
  ```

* Then just run the app using the Command
    
    ```
    > python Contact_list.py
    ```
    

# Building a binary using PyInstaller
* First install PyInstaller from PyPi
    ```
    > pip install PyInstaller
    ```

* Then Just run
    ```
    > pyinstaller -F --noconsole Contacts_list.py
    ```
* This will generate the binary in `dist` folder in the same directory

# Frameworks Used
* [Tkinter](https://docs.python.org/3/library/tk.html)
* [SQLite3](https://www.sqlite.org/index.html)
