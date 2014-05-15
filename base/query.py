from django.db import models

class EventQuerySet(models.QuerySet):
    """
    Facility methods
    """

    def labs(self):
        return self.filter(
            code__startswith=self.model.EVENT_LAB
        )

    def round_tables(self):
        return self.filter(
            code__startswith=self.model.EVENT_TAV
        )


