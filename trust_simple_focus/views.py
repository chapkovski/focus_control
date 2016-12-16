from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from . import models
from .models import Constants


class Send(Page):
    timeout_seconds = 10
    form_model = models.Player
    form_fields = ['sent_amount']



class WaitForP1(Page):
    timeout_seconds = 10
    template_name = 'trust_simple_focus/MyWait.html'

class SendBack(Page):
    pass

class ResultsWaitPage(Page):
    timeout_seconds = 10
    template_name = 'trust_simple_focus/MyWait.html'
    def before_next_page(self):
        self.player.set_payoffs()


class Results(Page):

    def vars_for_template(self):
        return {
            'tripled_amount': self.player.sent_amount * Constants.multiplication_factor
        }


page_sequence = [
    Send,
    # WaitForP1,
    # SendBack,
    ResultsWaitPage,
    Results,
]
