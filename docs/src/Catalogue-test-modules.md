The catalogue system equipped with testing modules. 
There are six main modules inside the system which are `useraccounts`, `catalogue`, `dictionaries` ,`orders`, `search`,`reports`.

We can run the testing for each module or run all directly in one command. 

* First, we need to shell to the catalogue-uwsgi container by command `make shell`. You have to make sure that you already in the `/home/web/catalogue/deployment` path. 

* If you want to run all test module in the single command, you just need this command `python manage.py test` then you will get the all test result. 

* If you want to run test one by one for each module. You need to specified the module in the parameter, like `python manage.py test orders` this command to run the test on orders module. 

Below the result of testing on the catalogue system. 


```
root@uwsgi:/home/web/django_project# python manage.py test useraccounts
Creating test database for alias 'default'...
......
----------------------------------------------------------------------
Ran 6 tests in 0.555s

OK
Destroying test database for alias 'default'...
root@uwsgi:/home/web/django_project# 


root@uwsgi:/home/web/django_project# python manage.py test catalogue
----------------------------------------------------------------------
Ran 145 tests in 18.756s

OK (skipped=10)
Destroying test database for alias 'default'...
Waiting up to 10 seconds
Press Ctrl-C to quit
root@uwsgi:/home/web/django_project# 


root@uwsgi:/home/web/django_project# python manage.py test dictionaries
Creating test database for alias 'default'...
........................................................................................................................................................
----------------------------------------------------------------------
Ran 152 tests in 2.988s

OK
Destroying test database for alias 'default'...


root@uwsgi:/home/web/django_project# python manage.py test orders
Creating test database for alias 'default'...
.........................s......s.........................s......s......s....................
----------------------------------------------------------------------
Ran 93 tests in 14.888s

OK (skipped=5)
Destroying test database for alias 'default'...
Waiting up to 10 seconds
Press Ctrl-C to quit
root@uwsgi:/home/web/django_project# 


root@uwsgi:/home/web/django_project# python manage.py test reports
Creating test database for alias 'default'...
..............................s.........
----------------------------------------------------------------------
Ran 40 tests in 4.479s

OK (skipped=1)
Destroying test database for alias 'default'...
root@uwsgi:/home/web/django_project# 


root@uwsgi:/home/web/django_project# python manage.py test search
----------------------------------------------------------------------
...........................................................................
----------------------------------------------------------------------
Ran 84 tests in 7.713s

Destroying test database for alias 'default'...
Waiting up to 10 seconds
Press Ctrl-C to quit
root@uwsgi:/home/web/django_project# 
```
