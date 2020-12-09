# ShelfSense

Welcome to ShelfSense.
This repository contains the code for a smart shelf system that uses weight as a form of stock control.
This project was completed as part of COMP 47570 - Ubiquitous Computing, UCD. 

The application is simply a proof of conceptIt is designed to be used with a Raspberry Pi connected to a load cell and hx711 amplifier.

Commits regarding the build of the application can be seen in this branch. The branch 'hardware' contains code that is stored on the Pi. Contributions for this have been split Ronan: 45%, Yuqian: 30%, Yi: 20% and the contributions to this code base and project reflect this.


To view this project you cancompleted the following steps:

1) Pull this repository and navigate to the inner django files

```bash
cd ShelfSense-hardwareDjango
cd ShelfSense-hardwareDjango
```

2) Create a clean python 3 environment and activate it

3) Add requirements

```bash
pip install requirements.txt
```

Please note, there may be some issues surrounding the installation of mysqldb, please refer to the documents for your specific OS here.

4) Add the password presented in the final slide of the presentation to the shelfSense/settings.py (line 88) to set up database connection

5) Run server

```bash
python manage.py runserver
```

6) Sign into the application with the following credentials

```bash
username: ronanbyrne2
password: demopass
```
