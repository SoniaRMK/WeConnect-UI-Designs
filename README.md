[![Build Status](https://travis-ci.org/SoniaRMK/WeConnect.svg?branch=master)](https://travis-ci.org/SoniaRMK/WeConnect)
[![Maintainability](https://api.codeclimate.com/v1/badges/5005cc713b8de4cd9d91/maintainability)](https://codeclimate.com/github/SoniaRMK/WeConnect/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/5005cc713b8de4cd9d91/test_coverage)](https://codeclimate.com/github/SoniaRMK/WeConnect/test_coverage)
[![Coverage Status](https://coveralls.io/repos/github/SoniaRMK/WeConnect/badge.svg?branch=master)](https://coveralls.io/github/SoniaRMK/WeConnect?branch=master)

# WeConnect
This repository contains the description, a guide on how to clone and run the platform.

### Project Description:
WeConnect provides a platform that brings businesses and individuals together. This platform creates awareness for businesses and gives the users the ability to write reviews about the businesses they have interacted with.  

### Required Features
  1.	Users can create an account and log in
  2.	Authenticated Users can register a business.
  3.	Only the user that creates the business can update and delete a business
  4.	Users can view businesses.
  5.	Users can give reviews about a business.
  6.	Users can search for businesses based on business location or business category.
  
| EndPoint                                              | Functionality                                    |
| ----------------------------------------------------- | ------------------------------------------------ |
| [POST\   /api/v1/auth/register](#)                    | Creates a user account                           |
| [POST\   /api/v1/auth/login](#)                       | Logs in a user                                   |
| [POST\   /api/v1/auth/logout](#)                      | Logs out a user                                  |
| [POST\   /api/v1/auth/reset-password](#)              | Password reset                                   |
| [POST\   /api/v1/businesses](#)                       | Register a business                              |
| [PUT\    /api/v1/businesses/\<int:bizid>](#)          | Updates a business profile                       |
| [DELETE\ /api/v1/businesses/\<int:bizid>](#)          | Remove a business                                |
| [GET\    /api/v1/businesses](#)                       | Retrieves all businesses                         |
| [GET\    /api/v1/businesses/\<int:bizid>](#)          | Get a business                                   |
| [GET\    /api/v1/businesses/\<int:bizid>/reviews](#)  | Get all reviews for a business                   |

### Prerequisites
  1.	HTML/CSS
  2.	Javascript/ES6
  3.	Python/Flask
  4.  GIT and Version Control  

## Technologies

* Python 3.6
* Flask Restful

## Requirements

* Install [Python](https://www.python.org/downloads/)
* Run `pip install virtualenv` on command prompt
* Run `pip install virtualenvwrapper-win` on command prompt
* Run `set WORKON_HOME=%USERPROFILES%\Envs` on command prompt

## Setup

* Run `git clone` this repository and `cd` into the project root.
* Run `mkvirtualenv venv` on command prompt
* Run `workon venv` on command prompt
* Run `pip freeze > requirements.txt` on command prompt
* Run `set FLASK_CONFIG=development` on command prompt
* Run `python app.py` on command prompt
* View the app on `http://127.0.0.1:5000/`

## Use endpoints

* Run `python app.py` on command prompt
* View the api on `http://127.0.0.1:5000/api/v2`
* Test it's usage with postman

## Unittests

* Run `pytest` on command prompt
  
## GitHub pages

Go to [WeConnect](https://soniarmk.github.io/index.html)

Happy Browsing! :smile:
