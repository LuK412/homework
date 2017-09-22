from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
	Currency as c, currency_range
)


from django_countries.fields import CountryField

author = 'Luisa'

doc = """
Social norms experiment.
"""


class Constants(BaseConstants):
	name_in_url = 'social_norms'
	players_per_group = 3								# Requires a number of participants which is neatly divisible by 3
	num_rounds = 10										# Please enter at least #participants/3 

	endowment = c(8)


class Subsession(BaseSubsession):
			
	def before_session_starts(self):
		if self.round_number == 1:
			self.group_randomly()						# Participants are randomized into groups of 3
		for player in self.get_players():
			player.treatment = self.session.config['treatment']
			player.advice = self.session.config['advice']
		group_matrix = self.get_group_matrix()
		for group in group_matrix:
			for player in group:
				player.my_group_id = group_matrix.index(group) + 1

	def ret_red_decision(self):
		all_groups = self.get_groups()
		return all_groups[self.round_number - 1].in_round(1).decision_red

	def ret_red_timeout(self):
		all_groups = self.get_groups()
		return all_groups[self.round_number -1].in_round(1).red_timeout

class Group(BaseGroup):

	def return_old_vars(self):
		return self.in_round(1).decision_red			# I need this in order to have the decision of red (in round 1)

	decision_red = models.CharField(
		choices=["A", "B", "C", "D", "E", "F"],
		widget=widgets.RadioSelectHorizontal(),
		verbose_name="Please make your decision.",
		doc="red player makes his decision."
		)

	decision_blue = models.CharField(
		choices=["A", "B", "C", "D", "E", "F"],
		widget=widgets.RadioSelectHorizontal(),
		verbose_name="Please indicate which allocation you would like red to choose.",
		doc="blue players makes their decision."
		)

	decision_green = models.CharField(
		choices=["A", "B", "C", "D", "E", "F"],
		widget=widgets.RadioSelectHorizontal(),
		verbose_name="Please indicate which allocation you would like red to choose.",
		doc="green players makes their decision."
		)

	red_timeout = models.BooleanField(
		doc="Turns 1 if the red player reaches the timeout on the decision page."
		)

	blue_timeout = models.BooleanField(
		doc="Turns 1 if the blue player reaches the timeout on the decision page."	# I need blue and green timeout as well as return_blue_timeout and green such that they get the information that they did not take a decision on the results screen.
		)

	green_timeout = models.BooleanField(
		doc="Turns 1 if the green player reaches the timeout on the decision page."
		)

	def return_red_timeout(self):
		return self.in_round(1).red_timeout		# I need this because I need a variable if red took no decision (in round 1)

	def return_blue_timeout(self):
		return self.in_round(1).blue_timeout

	def return_green_timeout(self):
		return self.in_round(1).green_timeout

	def calculate_payoffs(self):
		red = self.get_player_by_role("red")
		blue = self.get_player_by_role("blue")
		green = self.get_player_by_role("green")

		if self.in_round(1).decision_red == "A":
			if self.in_round(1).red_timeout == 1:
				red.payoff = c(0)
			else:
				red.payoff = Constants.endowment + c(4)
			if self.in_round(1).blue_timeout == 1:
				blue.payoff = c(0)
			else:
				blue.payoff = Constants.endowment
			if self.in_round(1).green_timeout == 1:
				green.payoff = c(0)
			else:
				green.payoff = Constants.endowment - c(8)
		if self.in_round(1).decision_red == "B":
			if self.in_round(1).red_timeout == 1:
				red.payoff = c(0)
			if self.in_round(1).red_timeout == 0:
				red.payoff = Constants.endowment + c(2)
			if self.in_round(1).blue_timeout == 1:
				blue.payoff = c(0)
			else:
				blue.payoff = Constants.endowment + c(2)
			if self.in_round(1).green_timeout == 1:
				green.payoff = c(0)
			else:
				green.payoff = Constants.endowment - c(6)
		if self.in_round(1).decision_red == "C":
			if self.in_round(1).red_timeout == 1:
				red.payoff = c(0)
			else:
				red.payoff = Constants.endowment
			if self.in_round(1).blue_timeout == 1:
				blue.payoff = c(0)
			else:
				blue.payoff = Constants.endowment + c(4)
			if self.in_round(1).green_timeout == 1:
				green.payoff = c(0)
			else:
				green.payoff = Constants.endowment - c(4)
		if self.in_round(1).decision_red == "D":
			if self.in_round(1).red_timeout == 1:
				red.payoff = c(0)
			else:
				red.payoff = Constants.endowment - c(2)
			if self.in_round(1).blue_timeout == 1:
				blue.payoff = c(0)
			else:
				blue.payoff = Constants.endowment + c(4)
			if self.in_round(1).green_timeout == 1:
				green.payoff = c(0)
			else:
				green.payoff = Constants.endowment - c(2)
		if self.in_round(1).decision_red == "E":
			if self.in_round(1).red_timeout == 1:
				red.payoff = c(0)
			else:
				red.payoff = Constants.endowment - c(4)
			if self.in_round(1).blue_timeout == 1:
				blue.payoff = c(0)
			else:
				blue.payoff = Constants.endowment + c(2)
			if self.in_round(1).green_timeout == 1:
				green.payoff = c(0)
			else:
				green.payoff = Constants.endowment
		if self.in_round(1).decision_red == "F":
			if self.in_round(1).red_timeout == 1:
				red.payoff = c(0)
			else:
				red.payoff = Constants.endowment - c(6)
			if self.in_round(1).blue_timeout == 1:
				blue.payoff = c(0)
			else:
				blue.payoff = Constants.endowment
			if self.in_round(1).green_timeout == 1:
				green.payoff = c(0)
			else:
				green.payoff = Constants.endowment + c(2)


class Player(BasePlayer):

	my_group_id = models.IntegerField(
		doc="Assigns each player a group ID")

	treatment = models.CharField(
		doc="Treatment"
		)

	advice = models.CharField(
		doc="Advice which is given to the players (see settings)."
		)

#	red_timeout = models.BooleanField(
#		doc="Turns 1 if the red player reaches the timeout on the decision page."
#		)

#	def return_red_timeout(self):
#		return self.in_round(1).red_timeout		# I need this because I need a variable if red took no decision (in round 1)

	def role(self):
		if self.id_in_group == 1:
			return "red"
		if self.id_in_group == 2:
			return "blue"
		if self.id_in_group == 3:
			return "green"

#	def assign_timeout(self, yes_no):
#		others = self.get_others_in_group()
#		if yes_no == 'yes': 
#			for player in others:
#				player.red_timeout = 1
#		elif yes_no == 'no':
#			for player in others:
#				player.red_timeout = 0


	# ab hier der Fragebogen:
	age = models.PositiveIntegerField(
		max=100,
		verbose_name="How old are you?",
		doc="We ask participants for their age between 0 and 100 years"
		)

	gender = models.CharField(
		choices=['female', 'male', 'other'],
		widget=widgets.RadioSelect(),
		verbose_name="Please indicate your gender.",
		doc="gender indication"
		)

	studies = models.CharField(
		blank=True,
		verbose_name="Please indicate your field of studies.",
		doc="field of studies indication."
		)

	studies2 = models.BooleanField(
		widget=widgets.CheckboxInput(),
		verbose_name="Non-student",
		doc="Ticking the checkbox means that the participant is a non-student.")

	risk = models.CharField(
		choices=["Highly risk averse", "risk averse", "somewhat risk averse", "neutral", "somewhat risk loving", "risk loving", "highly risk loving"],
		widget=widgets.RadioSelectHorizontal(),
		verbose_name="Please indicate your risk preference.",
		doc="7 point likert scale to measure risk preference."
		)

	country = CountryField(
		blank=True,
		verbose_name="Please indicate your country of birth.") # Kein doc möglich.
