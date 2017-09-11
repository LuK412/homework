from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Instructions(Page):

	def is_displayed(self):
		return self.round_number == 1


class Decision_red(Page):
	form_model = models.Group
	form_fields = ["decision_red"]

	def is_displayed(self):
		return self.player.role() == "red" and self.round_number == 1


class Decision_blue(Page):
	form_model = models.Group
	form_fields = ["decision_blue"]

	def is_displayed(self):
		return self.player.role() == "blue" and self.round_number == 1

class Decision_green(Page):
	form_model = models.Group
	form_fields = ["decision_green"]

	def is_displayed(self):
		return self.player.role() == "green" and self.round_number == 1

class RevelationWaitPage(WaitPage):

	wait_for_all_groups = True

class Revelation(Page):

	def is_displayed(self):
		return self.session.config['treatment'] == "public"


class WaitPage(WaitPage):

	def after_all_players_arrive(self):
		self.group.calculate_payoffs()


class Results(Page):
	
	def is_displayed(self):
		return self.round_number == len(self.subsession.get_groups())


class Questionnaire(Page):

	def is_displayed(self):
		return self.round_number == len(self.subsession.get_groups())


	form_model = models.Player
	form_fields = ["age", "gender", "studies", "studies2", "risk", "country"]

	def error_message(self, values):
		if values["studies"] == "" and values["studies2"] != True:
			return "Are you a non-student?"
		if values["studies"] != "" and values["studies2"] == True:
			return "You stated a field of studies, but indicated that you are a non-student."

class LastPage(Page):
	def is_displayed(self):
		return self.round_number == len(self.subsession.get_groups())


page_sequence = [
	Instructions,
	Decision_red,
	Decision_blue,
	Decision_green,
	RevelationWaitPage,
	Revelation,
	WaitPage,
	Results,
	Questionnaire,
	LastPage,
]
