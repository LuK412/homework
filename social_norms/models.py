from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
	Currency as c, currency_range
)

#import settings

from django_countries.fields import CountryField

author = 'Luisa'

doc = """
The experiment ends with a survey.
"""


class Constants(BaseConstants):
	name_in_url = 'social_norms'
	players_per_group = 3
	num_rounds = 100
#	number = int(float(settings.SESSION_CONFIGS[0]["num_demo_participants"])/3)
#	num_rounds = number

	endowment = c(8)


class Subsession(BaseSubsession):

	def ret_red_decision(self):
		all_groups = self.get_groups()
		return all_groups[self.round_number - 1].in_round(1).decision_red

	def creating_session(self):
		self.group_randomly


	def before_session_starts(self):
		for player in self.get_players():
			player.treatment = self.session.config['treatment']
			player.advice = self.session.config['advice']
			

	def creating_session(self):
		group_matrix = self.get_group_matrix()
		for group in group_matrix:
			for player in group:
				player.my_group_id = group_matrix.index(group) + 1


class Group(BaseGroup):

	def return_old_vars(self):
		return self.in_round(1).decision_red

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

	def calculate_payoffs(self):
		red = self.get_player_by_role("red")
		blue = self.get_player_by_role("blue")
		green = self.get_player_by_role("green")

		if self.in_round(1).decision_red == "A":
			red.payoff = Constants.endowment + c(4)
			blue.payoff = Constants.endowment
			green.payoff = Constants.endowment - c(8)
		if self.in_round(1).decision_red == "B":
			red.payoff = Constants.endowment + c(2)
			blue.payoff = Constants.endowment + c(2)
			green.payoff = Constants.endowment - c(6)
		if self.in_round(1).decision_red == "C":
			red.payoff = Constants.endowment
			blue.payoff = Constants.endowment + c(4)
			green.payoff = Constants.endowment - c(4)
		if self.in_round(1).decision_red == "D":
			red.payoff = Constants.endowment - c(2)
			blue.payoff = Constants.endowment + c(4)
			green.payoff = Constants.endowment - c(2)
		if self.in_round(1).decision_red == "E":
			red.payoff = Constants.endowment - c(4)
			blue.payoff = Constants.endowment + c(2)
			green.payoff = Constants.endowment
		if self.in_round(1).decision_red == "F":
			red.payoff = Constants.endowment - c(6)
			blue.payoff = Constants.endowment
			green.payoff = Constants.endowment + c(2)


class Player(BasePlayer):

	my_group_id = models.IntegerField()

	treatment = models.CharField()

	advice = models.CharField()

	payoff = models.CurrencyField(
		doc="Payoff for the players"
		)

	def role(self):
		if self.id_in_group == 1:
			return "red"
		if self.id_in_group == 2:
			return "blue"
		if self.id_in_group == 3:
			return "green"


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
		choices=["Extrem risk averse", "risk averse", "somewhat risk averse", "neutral", "somewhat risk loving", "risk loving", "extreme risk loving"],
		widget=widgets.RadioSelectHorizontal(),
		verbose_name="Please indicate your risk preference.",
		doc="7 point likert scale to measure risk preference."
		)

	country = CountryField(
		blank=True,
		verbose_name="Please indicate your country of birth.") # Kein doc und kein models. möglich davor.
