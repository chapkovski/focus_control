from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
from random import choice
from string import ascii_uppercase
from otree.db.models import Model, ForeignKey

doc = """
This is a standard 2-player trust game where the amount sent by player 1 gets
tripled. The trust game was first proposed by
<a href="http://econweb.ucsd.edu/~jandreon/Econ264/papers/Berg%20et%20al%20GEB%201995.pdf" target="_blank">
    Berg, Dickhaut, and McCabe (1995)
</a>.
"""


class Constants(BaseConstants):
    name_in_url = 'trust'
    players_per_group = 2
    num_rounds = 1

    instructions_template = 'trust/Instructions.html'

    # Initial amount allocated to each player
    amount_allocated = c(100)
    multiplication_factor = 3


class Subsession(BaseSubsession):
    pass

    def before_session_starts(self):   # called each round
        """For each player, create a fixed number of "decision stubs" with random values to be decided upon later."""
        pass 
        # for p in self.get_players():
        #     for _ in range(6):
        #         focus = p.focus_set.create()    # create a new Decision object as part of the player's decision set
        #         focus.infocus = random.randint(1, 10)
        #         focus.timefocus = ''.join(choice(ascii_uppercase) for i in range(12))
        #         print('success')
        #         focus.save()   # important: save to DB!

class Group(BaseGroup):
    pass

class Group(BaseGroup):

    sent_amount = models.CurrencyField(
        min=0, max=Constants.amount_allocated,
        doc="""Amount sent by P1""",
    )

    sent_back_amount = models.CurrencyField(
        doc="""Amount sent back by P2""",
        min=c(0),
    )

    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p1.payoff = Constants.amount_allocated - self.sent_amount + self.sent_back_amount
        p2.payoff = self.sent_amount * Constants.multiplication_factor - self.sent_back_amount


class Player(BasePlayer):
    curpage=models.CharField()
    def role(self):
        return {1: 'A', 2: 'B'}[self.id_in_group]


class Focus(Model):   # our custom model inherits from Django's base class "Model"

    whenhappens = models.CharField()
    whathappens = models.CharField()
    wherehappens = models.CharField()

    player = ForeignKey(Player)    # creates 1:m relation -> this decision was made by a certain player

    def __str__(self):
        return 'haha'
