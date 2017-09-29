from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class WaitPage_1(WaitPage):
	group_by_arrival_time = True

	def is_displayed(self):
		return self.round_number == 1


class Instructions(Page):

	timeout_seconds = 480

	# The pages Instructions, Example, Decision_red/blue/green and Intro_Part_II are only displayed in the fist round.
	def is_displayed(self):
		return self.round_number == 1

	def before_next_page(self):
		self.subsession.assign_group_id()


class Example(Page):

	timeout_seconds = 120

	def is_displayed(self):
		return self.round_number == 1


class Decision_red(Page):

	# The timeout on the decision pages can be varied. If you run this experiment in the lab, it might be sensible to give participants
	# more time or even use no timeout. Running this experiment in a lecture, it might be important that participants don't get bored
	# and drop out. Therefore, rather short decision time might be useful in this case.

	timeout_seconds = 120
	def before_next_page(self):
		# If the red player fails to make a decision...
		if self.timeout_happened:
			# ...the advice is going to be implemented
			self.group.decision_red = self.player.advice
			# ...red_timeout turns 1
			self.group.red_timeout = 1
		else:
			# otherwise red_timeout is 0.
			self.group.red_timeout = 0

	form_model = models.Group
	form_fields = ["decision_red"]

	def is_displayed(self):
		return self.player.role() == "red" and self.round_number == 1

class Decision_blue(Page):

	timeout_seconds = 120
	def before_next_page(self):
		# If the blue player fails to make a decision...
		if self.timeout_happened:
			# ...blue_timeout turns 1
			self.group.blue_timeout = 1
		# otherwise blue_timeout is 0.
		else:
			self.group.blue_timeout = 0

	form_model = models.Group
	form_fields = ["decision_blue"]

	def is_displayed(self):
		return self.player.role() == "blue" and self.round_number == 1


class Decision_green(Page):

	timeout_seconds = 120
	def before_next_page(self):
		# If the green player fails to make a decision...
		if self.timeout_happened:
			# ...green_timeout turns 1
			self.group.green_timeout = 1
		# otherwise green_timeout is 0.
		else:
			self.group.green_timeout = 0

	form_model = models.Group
	form_fields = ["decision_green"]

	def is_displayed(self):
		return self.player.role() == "green" and self.round_number == 1

class Intro_Part_II(Page):

	timeout_seconds = 120

	# The pages Intro_Part_II and Revelation are only displayed in the public treatment.
	def is_displayed(self):
		return self.session.config["treatment"] == "public" and self.round_number == 1 

class RevelationWaitPage(WaitPage):

	wait_for_all_groups = True

	def is_displayed(self):
		return self.round_number <= len(self.subsession.get_groups())

class Revelation(Page):

	timeout_seconds = 20

	# This page is only displayed if the round number is less than the number of groups in the experiment.
	# Remember that num_rounds in models.py is set to a large number.
	# Going without this is no problem but would mean that participants arrive on Last_Page when the round number equals the group number
	# and stay there forever, because the next button is missing. Otree, however, "would like" to play all rounds indicated in models.py.
	def is_displayed(self):
		return self.session.config["treatment"] == "public" and self.round_number <= len(self.subsession.get_groups())


class WaitPage_2(WaitPage):

	def after_all_players_arrive(self):
		self.group.calculate_payoffs()

	# I added the following because otherwise the payments on the screen "$ Payments" (I have no idea how to call it, but I mean the screen
	# when we created a session which we as experimenters can see and use to pay participants) were the actual payoff times
	# number of groups (= number of rounds actually played).
	# Remark: The variable payoff took the correct number because I refer only to payoff in round 1. However, it's better to see the "correct"
	# payoffs when actually running the experiment ;)
	def is_displayed(self):
		return self.round_number == len(self.subsession.get_groups())


class Results(Page):

	timeout_seconds = 60
	
	# The pages Results, Questionnaire and Last_Page are only displayed in the last round (that is in the round with round number
	# being equal to the number of groups).
	def is_displayed(self):
		return self.round_number == len(self.subsession.get_groups())


class Questionnaire(Page):

	timeout_seconds = 120

	form_model = models.Player
	form_fields = ["age", "gender", "studies", "studies2", "risk", "country"]

	# returns an error message if a participant...
	def error_message(self, values):
		# ... indicates no field of studies and does not tick the box "non-student".
		if values["studies"] == "" and values["studies2"] != True:
			return "You indicated no field of studies. Are you a non-student?"
		# ... states a field of studies and claimed to be a non-student.
		elif values["studies"] != "" and values["studies2"] == True:
			return "You stated a field of studies, but indicated that you are a non-student."

	def is_displayed(self):
		return self.round_number == len(self.subsession.get_groups())


class Last_Page(Page):
	def is_displayed(self):
		return self.round_number == len(self.subsession.get_groups())


page_sequence = [
	WaitPage_1,
	Instructions,
	Example,
	Decision_red,
	Decision_blue,
	Decision_green,
	Intro_Part_II,
	RevelationWaitPage,
	Revelation,
	WaitPage_2,
	Results,
	Questionnaire,
	Last_Page,
]
