# FoodRecepies

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