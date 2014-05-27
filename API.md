API
===

* POST login
* GET /events/
    restituisce un JSON con la lista di tutti gli elementi disponibili
* POST /event/<event_code>/subscribe
    il capo viene iscritto all'evento specificato
* POST /event/<event_code>/unsubscribe
    il capo viene disiscritto all'evento specificato

Alle POST viene restituito un JSON di conferma o di errore
{status: 'OK'}
{status: 'ERROR', message: 'Descrizione errore'}

Le richieste devono essere accompagnate dal cookie "sessionid" che permette
l'autenticazione del capo attraverso le sessioni.

Ogni POST deve essere accompagnata dal csrftoken (come in index.html)
