# URL Shortener 

URL Shortener is a modern URL shortener with support for custom domains.


![](https://user-images.githubusercontent.com/4659608/61927992-834bc880-af7f-11e9-93c1-554be576b067.png)

# Setup
You need to have Python3 and Redis installed on your machine.

* Clone this repository or download zip.
* Copy .example.env to .env and fill it properly.
* Install dependencies: `pip3 install -r requirements.txt`.
* Start flask project `python3 app.py`.
* To start flask with production env: `FLASK_CONFIG=production python3 app.py`


Dependencies
------------

### Project Dependencies

* [**Python3**](https://www.python.org/)
* [*flask*](http://flask.pocoo.org/)
* [**redis**](https://pypi.org/project/redis/) 
* [**jinja**](http://jinja.pocoo.org/docs/2.10/)
