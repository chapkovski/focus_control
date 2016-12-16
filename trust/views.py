from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from . import models
from .models import Constants, Focus


from collections import OrderedDict
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


class MyPage(Page):
    def vars_for_template(self):
        curgrouppls =  self.player.get_others_in_group()
        for p in curgrouppls:
            print('==============')
            print (p.participant.code)
            print (p.participant._index_in_pages)
            print (p.participant._max_page_index)
            print('==============')
        print(self.__class__.__name__)
        self.player.curpage = str(self.__class__.__name__)
        return self.extra_vars_for_template()
    def extra_vars_for_template(self):
        pass
class Introduction(MyPage):
    def extra_vars_for_template(self):
        focus_qs = Focus.objects.filter(player__exact=self.player)
        for f in focus_qs:
            print(f.infocus)
        return{'somevar':6789,
        'focuses':[f for f in focus_qs],
        }


class Send(Page):
    """This page is only for P1
    P1 sends amount (all, some, or none) to P2
    This amount is tripled by experimenter,
    i.e if sent amount by P1 is 5, amount received by P2 is 15"""

    form_model = models.Group
    form_fields = ['sent_amount']

    def is_displayed(self):
        return self.player.id_in_group == 1
class MyWaitPage(WaitPage):
    template_name = 'trust/newwaitpage.html'

class SendBack(Page):
    """This page is only for P2
    P2 sends back some amount (of the tripled amount received) to P1"""

    form_model = models.Group
    form_fields = ['sent_back_amount']

    def is_displayed(self):
        return self.player.id_in_group == 2

    def vars_for_template(self):
        tripled_amount = self.group.sent_amount * Constants.multiplication_factor

        return {
                'tripled_amount': tripled_amount,
                'prompt':
                    'Please enter a number from 0 to %s:' % tripled_amount}

    def sent_back_amount_max(self):
        return self.group.sent_amount * Constants.multiplication_factor


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    """This page displays the earnings of each player"""

    def vars_for_template(self):
        return {
            'tripled_amount': self.group.sent_amount * Constants.multiplication_factor
        }

@login_required
def export_view_json(request):
    """
    Custom view function to export full results for this game as JSON file
    """

    def create_odict_from_object(obj, fieldnames):
        """
        Small helper function to create an OrderedDict from an object <obj> using <fieldnames>
        as attributes.
        """
        data = OrderedDict()
        for f in fieldnames:
            data[f] = getattr(obj, f)

        return data

    # get the complete result data from the database
    qs_results = models.Player.objects.select_related('subsession', 'subsession__session', 'group', 'participant')\
                                      .prefetch_related('decision_set')\
                                      .all()

    session_fieldnames = []  # will be defined by get_field_names_for_csv
    subsess_fieldnames = []  # will be defined by get_field_names_for_csv
    group_fieldnames = []    # will be defined by get_field_names_for_csv
    player_fieldnames = []   # will be defined by get_field_names_for_csv
    decision_fieldnames = ['value', 'player_decision', 'reason']

    # get all sessions, order them by label
    sessions = sorted(set([p.subsession.session for p in qs_results]), key=lambda x: x.label)

    # this will be a list that contains data of all sessions
    output = []

    # loop through all sessions
    for sess in sessions:
        session_fieldnames = session_fieldnames or get_field_names_for_csv(sess.__class__)
        sess_output = create_odict_from_object(sess, session_fieldnames)
        sess_output['subsessions'] = []

        # loop through all subsessions (i.e. rounds) ordered by round number
        subsessions = sorted(sess.get_subsessions(), key=lambda x: x.round_number)
        for subsess in subsessions:
            subsess_fieldnames = subsess_fieldnames or get_field_names_for_csv(subsess.__class__)
            subsess_output = create_odict_from_object(subsess, subsess_fieldnames)
            subsess_output['groups'] = []

            # loop through all groups ordered by ID
            groups = sorted(subsess.get_groups(), key=lambda x: x.id_in_subsession)
            for g in groups:
                group_fieldnames = group_fieldnames or get_field_names_for_csv(g.__class__)
                g_output = create_odict_from_object(g, group_fieldnames)
                g_output['players'] = []

                # loop through all players ordered by ID
                players = sorted(g.get_players(), key=lambda x: x.participant.id_in_session)
                for p in players:
                    player_fieldnames = player_fieldnames or get_field_names_for_csv(p.__class__)
                    p_output = create_odict_from_object(p, player_fieldnames)

                    # add some additional player information
                    p_output['participant_id_in_session'] = p.participant.id_in_session
                    p_output['decisions'] = []

                    # loop through all decisions ordered by ID
                    decisions = p.decision_set.order_by('id')
                    for dec in decisions:
                        dec_output = create_odict_from_object(dec, decision_fieldnames)
                        p_output['decisions'].append(dec_output)

                    g_output['players'].append(p_output)

                subsess_output['groups'].append(g_output)

            sess_output['subsessions'].append(subsess_output)

        output.append(sess_output)

    return JsonResponse(output, safe=False)

    
page_sequence = [
    Introduction,
    Send,
    MyWaitPage,
    SendBack,
    ResultsWaitPage,
    Results,
]
