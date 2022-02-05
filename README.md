# VAST-2019 Mini Challenge 1 - Crowdsourcing for Situational Awareness

#### How to run the project
- install python 3
- install flask, `pip3 install flask`
- run the server: `python3 server.py`
- on the browser: `localhost:5000`

**Frontend**-has the code for the front end of the application - JS, HTML, CSS

**Backend**-has the code for the back end of the application - Python, Flask

## How to run the project:

Clone the repository using the command 
```bash
git clone https://github.com/tanujsingh/Data-Visualisation-Project-CSE-578.git
```
Now change the path to the cloned folder using the command 
```bash
cd Data-Visualisation-Project-CSE-578
```
This project was developed using [Python 3.8.1](https://www.python.org/downloads/release/python-381/) please Install python 3.8.1. Please install all the [python packages](https://packaging.python.org/tutorials/installing-packages/) with their respective versions as specified in the **requirements.txt** file in the root folder  depending on your configuration
```bash
pip install -r requirements.txt (or) py -3 -m pip install -r requirements.txt
```
.Now that we are done with the required installations please follow the following steps to run the **front end** and **backend** to view the output. 

Both the front end and back end are to be run simultaneously for the application to work as the front end consumes the backend APIs.

For starting **Frontend**: 

i) Open one terminal in the root project directory ***Data-Visualisation-Project-CSE-578*** and change directory to the Frontend from the root directory i.e., Data-Visualisation-Project-CSE-578 using the following command:
```bash
cd Frontend
```
ii) Now start the python local server using the command 
```bash
python3 -m http.server (or) py -3 -m http.server (or) python -m http.server 
```
Depending on your configuration. 

iii) Now, we should see a message **"Serving HTTP on :: port 8000 (http://[::]:8000/) ..."** which indicates the successful start of the python server. Keep this terminal running and proceed with the next steps.


For starting **Backend**:

i) Open a terminal in the root project directory **Data-Visualisation-Project-CSE-578** and Change directory to the Backend from the root directory i.e., Data-Visualisation-Project-CSE-578 using the following command: 

```bash
cd Backend 
```

ii) Now start the flask server using the following command: 

```bash
flask run (or) py -3 -m flask run
```

Depending on your configuration 

iii) Now, we should see a message ***"Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)"*** which indicates the successful start of the flask server. Keep this terminal running and proceed with the next steps.

 iv) Some environments (like Mac) may ask to set the FLASK_APP environment variable explicitly. In that case, set the environment variable using the below commands before step(ii).
```bash
export FLASK_APP=app.py
```
 
Now, open a mozilla firefox browser window and type **http://localhost:8000** to view the project



