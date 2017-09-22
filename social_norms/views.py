from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Instructions(Page):

	timeout_seconds = 480

	def is_displayed(self):
		return self.round_number == 1

class Example(Page):

	timeout_seconds = 120

	def is_displayed(self):
		return self.round_number == 1


class Decision_red(Page):

	timeout_seconds = 120											# The timeout on the decision pages can be varied. If you run this
	def before_next_page(self):										# experiment in the lab, it might be sensible to give participants 
		if self.timeout_happened:									# more time or even use no timeout.	
			self.group.decision_red = self.player.advice			# Running this experiment in a lecture, it might be important that
			self.group.red_timeout = 1								# participants don't get bored and drop out. Therefore, rather short
#			self.player.assign_timeout("yes")						# decision time might be useful in this case.
		else:
			self.group.red_timeout = 0
#			self.player.assign_timeout("no")

	form_model = models.Group
	form_fields = ["decision_red"]

	def is_displayed(self):
		return self.player.role() == "red" and self.round_number == 1

class Decision_blue(Page):

	timeout_seconds = 120
	def before_next_page(self):
		if self.timeout_happened:
			self.group.blue_timeout = 1
		else:
			self.group.blue_timeout = 0

	form_model = models.Group
	form_fields = ["decision_blue"]

	def is_displayed(self):
		return self.player.role() == "blue" and self.round_number == 1


class Decision_green(Page):

	timeout_seconds = 120
	def before_next_page(self):
		if self.timeout_happened:
			self.group.green_timeout = 1
		else:
			self.group.green_timeout = 0

	form_model = models.Group
	form_fields = ["decision_green"]

	def is_displayed(self):
		return self.player.role() == "green" and self.round_number == 1

class Intro_Part_II(Page):

	timeout_seconds = 120

	def is_displayed(self):
		return self.session.config["treatment"] == "public" and self.round_number == 1 

class RevelationWaitPage(WaitPage):

	wait_for_all_groups = True

	def is_displayed(self):
		return self.round_number <= len(self.subsession.get_groups())

class Revelation(Page):

	timeout_seconds = 20

	def is_displayed(self):
		return self.session.config['treatment'] == "public" and self.round_number <= len(self.subsession.get_groups())


class WaitPage(WaitPage):

	def after_all_players_arrive(self):
		self.group.calculate_payoffs()


class Results(Page):

	timeout_seconds = 60
	
	def is_displayed(self):
		return self.round_number == len(self.subsession.get_groups())


class Questionnaire(Page):

	timeout_seconds = 120

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
	Example,
	Decision_red,
	Decision_blue,
	Decision_green,
	Intro_Part_II,
	RevelationWaitPage,
	Revelation,
	WaitPage,
	Results,
	Questionnaire,
	LastPage,
]
