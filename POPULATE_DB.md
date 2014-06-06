
NOTE SUL POPOLAMENTO DEI DATI NEL DATABASE
==========================================

Vediamo le tabelle, i modelli cui sono agganciati
e tutti i campi significativi.

Premessa
--------

DEFAULT
^^^^^^^

Django gestisce i default a livello di codice,
non di database. Quindi se di seguito leggete ''default=''
non vuol dire che nel DB trovate la colonna con il default impostato.

Se vi trovate comodi per l''importazione potete alterare a mano
i default delle colonne nel db.

TIMEZONE
^^^^^^^^

Non so qual è il formato data di MySQL per le date con timezone,
ma per Django è importante usare quello. In postgres ad esempio è 

YYYY-MM-DD HH:MM+UTCOFFSET

Capi scout: scout_chiefs
------------------------

* Nome convenzionale: capo scout
* Descrizione: anagrafica capo e se è spalla;
* Modello: [ScoutChief](https://github.com/route-nazionale/event_subscribe/blob/master/base/models/base.py)

* Campi:

 * code: codice censimento
 * scout_unit: riferimento esterno alla tabella scout_units;
 * name
 * surname
 * birthday: giorno di nascita
 * is_spalla: booleano (Django default false)

Sottocampi: camp_districts
--------------------------

* Campi:

  * `name`: nome
  * `code`: codice

Strade di coraggio: base_heartbeat
----------------------------------

come camp_districts


Definizione eventi: camp_events
-------------------------------

* Nome convenzionale: definizione evento
* Descrizione: informazioni caratterizzanti un evento (Event) senza riferimenti temporali (EventTimeSlot) ed iscritti;
* Modello: [Event](https://github.com/route-nazionale/event_subscribe/blob/master/base/models/event.py)

* Campi:

 * `name`: nome umano; 
 * `description`: descrizione. Può essere HTML forse (sentire Lorenzo se ha problemi);
 * `kind`: TAV o LAB
 * `district`: chiave esterna a camp_districts;
 * `topic`: chiave esterna a base_heartbeat;
 * `num`: codice numerico dell''evento (ultima parte del codice <TIPO>-<COD DISTRETTO>-<COD STRADA DI CORAGGIO>-<COD NUMERICO>;
 * `seats_tot`: totale posti (quelli totali, NON quelli attualmente disponibili);
 * `max_chiefs_seats`: numero massimo di capi iscrivibili se NULL = "no limits" (default da django = 5);
 * `max_boys_seats`: numero massimo di ragazzi iscrivibili se NULL = "no limits" (default da django = 30);
 * `min_seats`: numero minimo di posti affinché l''evento si possa tenere (django default=1);
 * `min_age`: età minima. Il controllo c''è ma non penso che per i capi valga;
 * `max_age`: VIENE IGNORATO, lo elimineremo in una successiva versione. fuori specifica;
 * state_handicap = ENABLED|DISABLED
 * state_chief = ENABLED|DISABLED|RESERVED
 * state_activation = CREATING|ACTIVE|DISMISSED
 * state_subscription = OPEN|CLOSED

Turni: camp_eventtimeslots
--------------------------

* Nome convenzionale: turno
* Descrizione: turno in cui si può svolgere un happening
* Modello: [EventTimeSlot](https://github.com/route-nazionale/event_subscribe/blob/master/base/models/event.py)

* Campi:

 * name: nome dello slot opzionale. Se non settato risulta essere "$giorno dalle $ora alle $ora"
 * dt_start: data/ora in formato ISO (YYYY-MM-DD HH:MM +TIMEZONE -non so esattamente come è in mysql)
 * dt_stop: data/ora in formato ISO

* In pratica in questa tabella ci vanno 3 record :)

Happenings: camp_eventhappenings
--------------------------------

* Nome convenzionale: happening
* Descrizione: un evento (Event) collegato ad un turno (EventTimeSlot)
* Modello: [EventHappening](https://github.com/route-nazionale/event_subscribe/blob/master/base/models/event.py)

* Campi:

 * `event`: chiave esterna a camp_events;
 * `timeslot`: chiave esterna a camp_eventtimeslots;
 * `seats_n_boys`: numero dei ragazzi iscritti;
 * `seats_n_chiefs`: numero dei capi iscritti. **ATTENZIONE** questo equivale al numero delle iscrizioni riferite all''happening nella tabella subscriptions. **ATTENZIONE** forma normale non rispettata. **ATTENZIONE** settarlo a mano!

Animatori: camp_eventhappeningpeople
------------------------------------

* Nome convenzionale: animatore
* Descrizione: 
* Modello: [EventPerson](https://github.com/route-nazionale/event_subscribe/blob/master/base/models/event.py)

**TODO** vedi campi del modello se si vuole implementare, ma per ora tralasciato
**TODO** si relaziona con il modello Person tabella base_person

* TODO name
* TODO surname
* TODO kind: CHIEF (=capo), GUEST (=ospite)
* TODO code: codice censimento se è un capo, altrimenti... codice fiscale se lo si ha
* TODO city: città di provenienza
* TODO description: descrizione del personaggio
* TODO event

