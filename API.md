RESTful API
===========

* POST login
* GET /event/ - lista eventi con parametri
   * user (utente): <user_id> -> server per filtro per età, e sapere a quali lui si è già iscritto
   * can_subscribe (disponibilità): 0, 1
   * kind (tipologia): 
        * lab (laboratorio)
        * tav (tavola rotonda)
   * timeslot (fascia): 
        * 0 (venerdì mattina), 
        * 1 (venerdì pomeriggio), 
        * 2 (sabato mattina)
    * subcamp (quartiere) : <subcamp_id>
    * is_handicap_enabled (accessibilità): 0, 1
* GET /event/:event_code/ - singolo evento 
* POST /event/:event_code/subscribe - iscrizione evento 

