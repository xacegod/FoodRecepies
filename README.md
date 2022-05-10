# Food Recepies Django App

The object of this task is to create a simple web service for Food recipes. It should be written
in Python, using the Django and Django REST framework.

### Entities needed: 
```
● User 
● Recipe 
● Ingredient 
```
### Basic features:
```
● User registration 
● User login 
● Recipe creation 
● Recipe Rating (you cannot rate your own recipes) 
● List all recipes 
● List own recipes 
● Get most used ingredients (top 5)
``` 
### Requirements:
```
● User should at least have email, first name, and last name 
● Recipe should have a name, recipe text, and ingredients 
● Ingredient should have a name 
● Rating is number between 1 and 5 
● When listing recipes, return an average rating for each recipe. 
● Use hunter for verifying email existence on registration 
● Use clearbit for getting additional data for the user 
● Use JWT for user authentication 
● The solution should be posted on any source control 
```
### Bonus:
```
● Dockerized solution is a plus 
● Unit tests are a plus 
● Search recipes (name, text, ingredients) is a plus 
```

### Hunter.io
Based on info found here:
https://hunter.io/api/email-verifier

I created a request with the following data:
GET https://api.hunter.io/v2/email-verifier?email=patrick@stripe.com&api_key=API_KEY

In setting set up the Hunter.io Api key.

 ```
{'status': 'accept_all', 
'result': 'risky', 
'_deprecation_notice': 'Using result is deprecated, use status instead', 
'score': 78, 
'email': 'jelena@jelena.com', 
'regexp': True, 'gibberish': False, 'disposable': False, 'webmail': False, 'mx_records': True, 
'smtp_server': True, 'smtp_check': True, 'accept_all': True, 
'block': False, 
'sources': [{'domain': 'mytennisprofile.com', 
'uri': 'http://mytennisprofile.com/users/player/jelena-jankovic', 'extracted_on': '2020-10-25', 
'last_seen_on': '2021-01-25', 'still_on_page': False}]}
```

### ClearBit
https://dashboard.clearbit.com/docs?python#
