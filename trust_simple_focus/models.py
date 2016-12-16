from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


doc = """
Simple trust game with measuring focus on the tab for mTurk
"""


class Constants(BaseConstants):
    name_in_url = 'trust_simple_focus'
    players_per_group = None
    num_rounds = 10

    endowment = c(10)
    multiplication_factor = 3

    instructions_template = 'trust_simple_focus/Instructions.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    def sent_back_amount_choices(self):
        return currency_range(
            c(0),
            self.sent_amount * Constants.multiplication_factor,
            c(1)
        )
    curpage=models.CharField()    
    sent_amount = models.CurrencyField(
        choices=currency_range(0, Constants.endowment, c(1)),
        doc="""Amount sent by P1""",
    )

    sent_back_amount = models.CurrencyField(
        doc="""Amount sent back by P2""",
    )

    def set_payoffs(self):
        tripled_amount = self.sent_amount * Constants.multiplication_factor
        self.sent_back_amount=random.choice(self.sent_back_amount_choices())
        # p1 = self
        # p2 = self.get_player_by_id(2)
        self.payoff = Constants.endowment - self.sent_amount + self.sent_back_amount
        # p2.payoff = self.sent_amount * Constants.multiplication_factor - self.sent_back_amount
