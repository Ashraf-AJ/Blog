To run the backend you must have python installed (currently using `python 3.8.2`), and do the following:<br>
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

- Run the development server:<br>
  `flask run`
