1) Download python 3.10.9
2) create a virtual environemnet using (ctrl+shift+P) -->create virtual environement in the folder
3) activate environement
4) install the libraries (pip install -r requirements.txt)
5) For Automated Daily run(Windows task scheduler)
6) create a daily_runner.bat file (which is already in the folder)
7) Start menu ---> task scheduler ---> enter
8) On the right panel, click "Create Task"

9) On the General tab:

Name: Daily TSLA Prediction

Choose: Run whether user is logged on or not

Check: Run with highest privileges

10) Go to the Triggers tab → Click New:

Begin the task: On a schedule

Set Daily

Choose a time: e.g., 6:30 PM

Click OK

11) Go to the Actions tab → Click New:

Action: Start a program

Browse → Select your daily_runner.bat file

Click OK

12) Click OK to save the task

If asked, enter your Windows password

13) for password change:
        (Windows+I) -- > Go to Accounts --> sign-in options--> under password --> add or change password-->OK


**Running the files**
step1: pip install -r requirements.txt
step2: python model.py
step3: streamlit run app.py