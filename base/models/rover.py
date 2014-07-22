#-*- coding: utf-8 -*-

from django.db import models
from event import Event

import datetime

#--------------------------------------------------------------------------------
# Extending a bit the User model
# compatible with bureau_manager
from django.contrib.auth.models import User

def user_is_readonly(self):
    return bool(self.groups.filter(name='readonly').count())

User.add_to_class('is_readonly', user_is_readonly)

#---------------------------------------------------------------------------------

class Vclans(models.Model):

    idvclan = models.CharField(max_length=255, blank=True)
    idgruppo = models.CharField(verbose_name="ID gruppo", max_length=255, blank=True)
    idunitagruppo = models.CharField(verbose_name="ID unità gruppo", max_length=255, blank=True)
    # ordinale = models.CharField(max_length=255, blank=True)
    nome = models.CharField(max_length=255, blank=True)
    regione = models.CharField(max_length=255, blank=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    arrivato_al_campo = models.NullBooleanField(default=None)
    dt_verifica_di_arrivo = models.DateTimeField(blank=True, null=True, default=None)

    #route = models.ForeignKey('Routes', db_column='route_id', null=True)
    #is_ospitante = models.NullBooleanField(default=None)
    
    class Meta:
        #managed = False
        db_table = 'vclans'
        verbose_name = 'clan'
        verbose_name_plural = 'clan'

    def __unicode__(self):
        return u"%s (%s)" % (self.nome, self.idunitagruppo)


class Rover(models.Model):

    FIELDS_TO_SERIALIZE = [
        "id",
        "nome",
        "cognome",
        "eta",
        "stradadicoraggio1",
        "stradadicoraggio2",
        "stradadicoraggio3",
        "stradadicoraggio4",
        "stradadicoraggio5",
        "turno1",
        "priorita1",
        "turno2",
        "priorita2",
        "turno3",
        "priorita3",
        "soddisfacimento"
    ]

    codicecensimento = models.IntegerField()

    nome = models.CharField(max_length=50)
    cognome = models.CharField(max_length=50)

    vclan = models.ForeignKey(Vclans, verbose_name="clan", null=True, blank=True)

    eta = models.IntegerField()
    handicap = models.BooleanField(default=False)
    
    stradadicoraggio1 = models.BooleanField(
        default=False, verbose_name="Il coraggio di amare (1)"
    )
    stradadicoraggio2 = models.BooleanField(default=False,
        verbose_name = "Il coraggio di farsi ultimi (2)"
    )
    stradadicoraggio3 = models.BooleanField(default=False,
        verbose_name = "Il coraggio di essere chiesa (3)"
    )
    stradadicoraggio4 = models.BooleanField(default=False,
        verbose_name = "Il coraggio di essere cittadini (4)"
    )
    stradadicoraggio5 = models.BooleanField(default=False,
        verbose_name = "Il coraggio di liberare il futuro (5)"
    ) 

    codicecensimento = models.CharField(max_length=50)
    
    turno1 = models.ForeignKey(Event, 
        to_field='code', related_name="turno1_rover_set", 
        null=True, blank=True, db_column="turno1",
        verbose_name="Venerdì 8 mattina"
    )
    priorita1 = models.IntegerField(blank=True, default=0, 
        help_text="Valore da 0 a 9. Se 0 -> assegnato manualmente, Se 1 vuol dire che l'evento soddisfa tutti i vincoli caricati. Man mano che si alza indica che alcuni vincoli sono stati tralasciati"
    )
    valido1 = models.BooleanField(default=True, blank=True)
    
    turno2 = models.ForeignKey(Event, 
        to_field='code', related_name="turno2_rover_set", 
        null=True, blank=True, db_column="turno2",
        verbose_name="Venerdì 8 pomeriggio"
    )
    priorita2 = models.IntegerField(blank=True, default=0,
        help_text="Valore da 0 a 9. Se 0 -> assegnato manualmente, Se 1 vuol dire che l'evento soddisfa tutti i vincoli caricati. Man mano che si alza indica che alcuni vincoli sono stati tralasciati"
    )
    valido2 = models.BooleanField(default=True, blank=True)

    turno3 = models.ForeignKey(Event, 
        to_field='code', related_name="turno3_rover_set", 
        null=True, blank=True, db_column="turno3",
        verbose_name="Sabato 9 mattina"
    )
    priorita3 = models.IntegerField(blank=True, default=0,
        help_text="Valore da 0 a 9. Se 0 -> assegnato manualmente, Se 1 vuol dire che l'evento soddisfa tutti i vincoli caricati. Man mano che si alza indica che alcuni vincoli sono stati tralasciati"
    )
    valido3 = models.BooleanField(default=True, blank=True)
    
    soddisfacimento = models.IntegerField(blank=True)

    class Meta:
        db_table = "ragazzi_assegnati"

    def __unicode__(self):
        return u"%s %s - %s" % (self.nome, self.cognome, self.vclan)

    def clean(self):

        super(Rover, self).clean()
        
        if self.priorita1 is None: self.priorita1 = 0
        if self.priorita2 is None: self.priorita2 = 0
        if self.priorita3 is None: self.priorita3 = 0

        if self.turno1 is None: 
            self.valido1 = False
        elif self.turno1.state_activation == Event.ACTIVATION_ACTIVE:
            self.valido1 = True
        if self.turno2 is None: 
            self.valido2 = False
        elif self.turno2.state_activation == Event.ACTIVATION_ACTIVE:
            self.valido2 = True

        if self.turno3 is None: 
            self.valido3 = False
        elif self.turno3.state_activation == Event.ACTIVATION_ACTIVE:
            self.valido3 = True
        
        self.soddisfacimento = self.calculate_satisfaction()

    def as_dict(self):
        obj = {}
        for field in self.FIELDS_TO_SERIALIZE:
            v = getattr(self, field)
            if isinstance(v, (models.Field, models.Model)):
                v = unicode(v)
            elif isinstance(v, datetime.datetime):
                v = v.strftime("%s")
            obj[field] = v
        return obj

    def assign_lab(turn_num, lab_num, lab_code, lab_validity):
        if turn_num == 1:
            self.turno1 = lab_code
            self.seq1 = lab_num
            self.valido1 = lab_validity
            self.priorita1 = 0
        elif turn_num == 2:
            self.turno2 = lab_code
            self.seq2 = lab_num
            self.valido2 = lab_validity
            self.priorita2 = 0
        elif turn_num == 3:
            self.turno3 = lab_code
            self.seq3 = lab_num
            self.valido3 = lab_validity
            self.priorita3 = 0
        else:
            pass


    def get_lab(self, num):
        l = Event.objects.get(num=num)

    def is_road_suitable(self, road_num):
        """
        Restituisce True o False a seconda che la strada di coraggio
        sia selezionata
        """

        return getattr(self, 'stradadicoraggio%d' % road_num)

    def calculate_satisfaction(self):
        sat = 0

        events_selected = [
            x for x in self.turno1, self.turno2, self.turno3 
                if x is not None and x.state_activation == Event.ACTIVATION_ACTIVE 
        ]

        # Step 1: aumenta il punteggio se la strada di coraggio e' stata scelta
        for event in events_selected:
            if self.is_road_suitable(event.topic_id):
                sat += 5

        # Step 2: aumenta il punteggio se le strade di coraggio sono diverse

        i = 0
        while i < len(events_selected):

            e_to_compare = events_selected[i]
            for e in events_selected[i+1:]:

                if e_to_compare.topic != e.topic:
                    sat += 2
            
            i += 1

        return sat

    #def check_constraints(lab_num, turn_num):
    #    """
    #    Controlla che i vincoli siano soddisfatti per un assegnamento.
    #    Ritorna una stringa che descrive verbalmente il risultato.
    #    """

    #    msgs = []

    #    e = Event.objects.get(num=lab_num)

    #    if self.handicap and not e.state_handicap == Event.STATE_ENABLED:
    #        msgs.append("Assegnamento ragazzo disabile a laboratorio non per disabili")

    #    if self.eta < e.min_age:
    #        msgs.append("Assegnamento ragazzo disabile a laboratorio non per disabili")

    #    if e.max_boys_seats == 0:
    #        msgs.append("Assegnamento ragazzo a laboratorio per soli capi")

    #    if e.max_boys_seats <= e.seats_n_boys:
    #        msgs.append("Assegnamento ragazzo oltre il numero massimo")
    #    
    #    if turn_num == 1:
    #        if e.topic__id == self.turno2.topic__id:
    #            msgs.append("Turno 1 e turno 2 hanno la stessa strada di coraggio.")
    #        if e.topic__id == self.turno3.topic__id:
    #            msgs.append("Turno 1 e turno 3 hanno la stessa strada di coraggio.")
    #    elif turn_num == 2:
    #        if e.topic__id == self.turno3.topic__id:
    #            msgs.append("Turno 2 e turno 3 hanno la stessa strada di coraggio.")

    #    if len(msgs) == 0:
    #        return "Tutti i vincoli sono soddisfatti"
    #    return ",\n".join(msgs) + "."

    def check_constraints(self):
        """
        Controlla che i vincoli siano soddisfatti per un assegnamento.
        Ritorna una stringa che descrive verbalmente il risultato.
        """

        msgs = {}
        events_selected = []

        # Step 1: controlla i vincoli all'interno di un singolo turno
        for turn_name in ('turno1', 'turno2', 'turno3'):

            e = getattr(self, turn_name)
            if e:

                events_selected.append((turn_name, e))

                msg_turn = []

                if self.handicap and not e.state_handicap == Event.STATE_ENABLED:
                    msg_turn.append("Assegnamento ragazzo disabile a laboratorio non per disabili")

                if self.eta < e.min_age:
                    msg_turn.append("Assegnamento ragazzo disabile a laboratorio non per disabili")

                if e.max_boys_seats == 0:
                    msg_turn.append("Assegnamento ragazzo a laboratorio per soli capi")

                if e.max_boys_seats <= getattr(e, '%s_rover_set' % turn_name).count():
                    msg_turn.append("Assegnamento ragazzo oltre il numero massimo")
            
                if msg_turn: #no news good news!
                    msgs[turn_name] = msg_turn #non serve ["Tutti i vincoli sono soddisfatti"]

        # Step 2: controlla i vincoli interturno
        msgs['__all__'] = []

        # strade di coraggio

        i = 0
        while i < len(events_selected):

            turn_to_compare, e_to_compare = events_selected[i]
            for turn, e in events_selected[i+1:]:

                if e_to_compare.topic == e.topic:
                   msgs['__all__'].append("%s e %s hanno la stessa strada di coraggio." % (turn_to_compare, turn))
            
            i += 1

        if not msgs['__all__']:
            msgs.pop('__all__')

        return msgs

    def save(self, *args, **kw):
        self.clean()
        super(Rover, self).save(*args, **kw)
