
NOTE SULL'IMPORTAZIONE BULK DEI DATI
====================================

Nell'intento di minimizzare lo sforzo implementativo si 
riduce l'importazione alle entità:

1. Capi iscritti alla route
2. Eventi
3. Animatori degli eventi

Altre 2 entità minori, che penso siano impostabili anche a mano,
e che richiedono esclusivamente i campi "codice" e "nome umano"
sono:

4. Distretti (sottocampi)
5. Strade di coraggio

Si descrivono i singoli campi.

Capi iscritti alla route
------------------------

* code: codice censimento
* unit: gruppo di appartenenza
* name
* surname
* birthday: giorno di nascita in formato ISO YYYY-MM-DD (valutare se è più comodo altro)


Eventi
------

Questa è la parte più impegnativa. Ci sono varie informazioni ripetute,
anche se nella fase di import vengono rimodellate e non vengono mantenute incoerenze.

* dt_start: data/ora in formato ISO (YYYY-MM-DD HH:MM)
* dt_stop: data/ora in formato ISO
* codice: <TIPO>-<COD DISTRETTO>-<COD STRADA DI CORAGGIO>-<COD NUMERICO> 
    (queste info possono essere fornite anche separatamente se è più comodo)
    NOTA IMPORTANTE se forniti insieme i codici devono avere lunghezza fissa
* name
* description
* seats_tot: posti disponibili
* min_seats: posti minimi (default=1)
* max_boys_seats: max posti ragazzi
* max_chief_seats: max posti capi
* min_age = età minima
* max_age = età massima
* state_handicap = ENABLED|DISABLED
* state_chief = ENABLED|DISABLED|RESERVED
* state_activation = CREATING|ACTIVE|DISMISSED
* state_subscription = OPEN|CLOSED
* num_ragazzi_iscritti
* num_capi_iscritti


Animatori degli eventi
----------------------

* name
* surname
* kind: CHIEF (=capo), GUEST (=ospite)
* code: codice censimento se è un capo, altrimenti... codice fiscale se lo si ha
* city: città di provenienza
* description: descrizione del personaggio
* event_code
