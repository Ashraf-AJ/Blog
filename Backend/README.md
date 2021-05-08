To run the backend you must have `python 3.6+` installed, and do the following:<br>
On **Windows**:<br>

- `cd` into `Backend` directory<br>
- Create a virtual environment named `venv` :<br>
  `python -m venv venv`<br>
- Activate the virtual environment:<br>
  `venv\Scripts\activate`
- Install required packages :<br>
  `pip install -r requirements\dev.txt`<br>
- Create a file named `.flaskenv` and set the following variables:<br>

```shell
FLASK_APP=app.py
FLASK_ENV=development
```
