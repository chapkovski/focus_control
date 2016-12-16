from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

doc = """
This is a one-period public goods game with 3 players.
"""


class Constants(BaseConstants):
    name_in_url = 'public_goods'
    players_per_group = 3
    num_rounds = 2

    instructions_template = 'public_goods/Instructions.html'

    # """Amount allocated to each player"""
    endowment = c(100)
    efficiency_factor = 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField()

    individual_share = models.CurrencyField()

    def set_payoffs(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.individual_share = self.total_contribution * Constants.efficiency_factor / Constants.players_per_group
        for p in self.get_players():
            p.payoff = (Constants.endowment - p.contribution) + self.individual_share




class Player(BasePlayer):
    contribution = models.CurrencyField(
        min=0, max=Constants.endowment,
        doc="""The amount contributed by the player""",
    )
    def set_tot_payoffs(self):
        # print("HELLO")
        cumulative_payoff = sum([p.payoff for p in self.player.in_previous_rounds()])
        return cumulative_payoff
