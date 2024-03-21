# To run this application

1. Create a virtual enviroment

    ## For Windows:
    `python -m venv cpsc449`

    `cpsc449\bin\activate.ps1`

    ## For MacOS\Linux:
    `python3 -m venv cpsc449`

    `source cpsc449\bin\activate`

2. Install all the requirements with 

    `pip install -r requirements.txt`

    Use pip3 for MacOS

3. Install [MySQL Community Edition](https://www.mysql.com/products/community/) and configure it.

4. Open MySQL shell and create a database using

    `create database cpsc449`

5. Run the application using `flask run`

