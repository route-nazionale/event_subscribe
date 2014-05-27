event_subscribe
==================
Iscrizione capi agli eventi della Route Nazionale 2014


Installazione
=============
Requisiti:

* virtualenv (consigliato ma non obbligatorio)
* python 2
* django 1.7
* recaptcha-client

Procedura di installazione:

```sh
sudo apt-get install virtualenvwrapper
mkvirtualenv rn-django17
git clone git@github.com:route-nazionale/event_subscribe.git
pip install -r requirements.txt
cd event_subscribe
cp event_subscribe/settings_dist.py event_subscribe/settings.py
```
inserite nel file event_subscribe/settings.py le vostre chiavi RECAPTCHA Google

Procedura di sviluppo/test:

```sh
# per entrare nel virtualenv
workon rn-django17
cd event_subscribe
python manage.py runserver

# per uscire dal virtualenv
deactivate
```

Il repository contiene un DB sqlite che ha dentro alcuni dati di test.

Per visualizzare e modificare i dati, utilizzate la comoda interfaccia di admin di django.

http://localhost:8000/admin

Potete accedere con nome utente 'admin' e password 'admin'


