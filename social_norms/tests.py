from otree.api import Currency as c, currency_range
from otree.api import SubmissionMustFail
from otree.api import Submission
from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

	cases = [
	{"red_decision": "A", "red_payoff": 12, "blue_payoff": 8, "green_payoff": 0},
	{"red_decision": "B", "red_payoff": 10, "blue_payoff": 10, "green_payoff": 2},
	{"red_decision": "C", "red_payoff": 8, "blue_payoff": 12, "green_payoff": 4},
	{"red_decision": "D", "red_payoff": 6, "blue_payoff": 12, "green_payoff": 6},
	{"red_decision": "E", "red_payoff": 4, "blue_payoff": 10, "green_payoff": 8},
	{"red_decision": "F", "red_payoff": 2, "blue_payoff": 8, "green_payoff": 10}
	]

	def play_round(self):
		case = self.case

		# check role assignment
		if self.player.id_in_group == 1:
			assert self.player.role() == "red"
		
		if self.player.id_in_group == 2:
			assert self.player.role() == "blue"

		if self.player.id_in_group == 3:
			assert self.player.role() == "green"

		# page 1
		if self.round_number == 1:
			# Make sure that the correct information is displayed in each treatment
			if self.session.config['treatment'] == "private":
				assert ("Your role and decision in the experiment will remain private." in self.html)
			if self.session.config['treatment'] == "public":
				assert ("At the end of the experiment, participants will have to stand up, say their group number and the decision they took." in self.html)
			yield (views.Instructions)

		# page 2
			if self.player.role() == "red":
				# red's decision page
				assert ("Your color in the experiment is <strong>red</strong>." in self.html)
				yield SubmissionMustFail(views.Decision_red, {"decision_red": 5 })
				yield SubmissionMustFail(views.Decision_red, {"decision_red": "Z" })

				yield (views.Decision_red, {"decision_red": case['red_decision']})
			
				#assert self.group.proposer_share == c(60) payoff

		# page 2
			if self.player.role() == "blue":
				# blue's decision page
				assert ("Your color in the experiment is <strong>blue</strong>." in self.html)
				yield SubmissionMustFail(views.Decision_blue, {"decision_blue": 5 })
				yield SubmissionMustFail(views.Decision_blue, {"decision_blue": "Z" })

				yield (views.Decision_blue, {"decision_blue": "C" })
			
				#assert self.group.proposer_share == c(60) payoff

		# page 2
			if self.player.role() == "green":
			# green's decision page
				assert ("Your color in the experiment is <strong>green</strong>." in self.html)
				yield SubmissionMustFail(views.Decision_green, {"decision_green": 5 })
				yield SubmissionMustFail(views.Decision_green, {"decision_green": "Z" })

				yield (views.Decision_green, {"decision_green": "C" })
			
				#assert self.group.proposer_share == c(60) payoff

		yield (views.Revelation)

		if self.round_number == len(self.subsession.get_groups()):

		# page 4	
			yield (views.Results)
			if self.player.role() == "red":
				players_payoff = case["red_payoff"]
			if self.player.role() == "blue":
				players_payoff = case["blue_payoff"]
			if self.player.role() == "green":
				players_payoff = case["green_payoff"]

			assert self.player.payoff == players_payoff

			invalid_age_data = {
			"age": -1,
			"gender": "male",
			"studies": "Economics",
			"studies2": False,
			"risk": "neutral",
			"country": "Australia"
			}

			yield SubmissionMustFail(views.Questionnaire, invalid_age_data)

			invalid_gender_data = {
			"age": 25,             
			"gender": 5, 
			"studies": "Economics",
			"studies2": False,
			"risk": "neutral",
			"country": "Australia"
			}

			yield SubmissionMustFail(views.Questionnaire, invalid_gender_data)

			# Here we name a field of studies but say that we are not a student.
			invalid_studies_1 = {
			"age": 25,
			"gender": "other",
			"studies": "English",
			"studies2": True,
			"risk": "risk averse",
			"country": "Australia"
			}

			yield SubmissionMustFail(views.Questionnaire, invalid_studies_1)

			# Here we name no field of studies and don't say that we are a non-student.
			invalid_studies_2 = {
			"age": 25,
			"gender": "other",
			"studies": "",
			"studies2": False,
			"risk": "risk averse",
			"country": "Australia"
			}

			yield SubmissionMustFail(views.Questionnaire, invalid_studies_2)

			invalid_risk = {
			"age": 25,
			"gender": "other",
			"studies": "French",
			"studies2": False,
			"risk": "",
			"country": "Australia"
			}

			yield SubmissionMustFail(views.Questionnaire, invalid_risk)

			# Now check whether "a correct one" passes.
			# Remark: It is allowed to leave the country of origin blank.
			valid_survey_data = {
			"age": 25,
			"gender": "male",
			"studies": "Economics",
			"studies2": False,
			"risk": "neutral",
			"country": ""
			}

			yield (views.Questionnaire, valid_survey_data)


	