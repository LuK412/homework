from otree.api import Currency as c, currency_range
from otree.api import SubmissionMustFail
from otree.api import Submission
from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

	cases = [
	{"red_decision": "A"},
	{"red_decision": "B"},
	{"red_decision": "C"},
	{"red_decision": "D"},
	{"red_decision": "E"},
	{"red_decision": "F"},
	"timeout_red",	# only the red player has a timeout
	"timeout"		# all players have a timeout
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

		# page 1: Introduction
		if self.round_number == 1:
			# Make sure that the correct information is displayed in each treatment
			if self.session.config['treatment'] == "private":
				assert ("Your role and decision in the experiment will remain private." in self.html)
			if self.session.config['treatment'] == "public":
				assert ("This experiment consists of two parts which are described below." in self.html)
				assert ("After all players took their decision, the <strong> red </strong> players of each group have to stand up one after another, say their group number and their decision." in self.html)
			yield (views.Instructions)

		# page 2: Example
			yield (views.Example)

		# page 3: Decision_red
			if self.player.role() == "red":
				# red's decision page
				assert ("Your color in the experiment: <strong> red </strong>" in self.html)
				assert ("Advice formulated by other students: <strong> " + str(self.player.advice) +" </strong>" in self.html)
				yield SubmissionMustFail(views.Decision_red, {"decision_red": 5 })
				yield SubmissionMustFail(views.Decision_red, {"decision_red": "Z" })

				# check that the advice is implemented if red has a timeout
				if self.case == "timeout_red" or self.case == "timeout":
					yield Submission(views.Decision_red, timeout_happened=True)
					assert self.group.decision_red == self.session.config["advice"]
				else:
					yield (views.Decision_red, {"decision_red": case['red_decision']})
				

		# page 3: Decision_blue
			if self.player.role() == "blue":
				# blue's decision page
				assert ("Your color in the experiment: <strong> blue </strong>" in self.html)
				assert ("Advice formulated by other students: <strong> " + str(self.player.advice) +" </strong>" in self.html)
				yield SubmissionMustFail(views.Decision_blue, {"decision_blue": 5 })
				yield SubmissionMustFail(views.Decision_blue, {"decision_blue": "Z" })

				# check that the advice is implemented if blue has a timeout
				if self.case == "timeout":
					yield Submission(views.Decision_blue, timeout_happened=True)
				else:
					yield (views.Decision_blue, {"decision_blue": "C" })
			

		# page 3: Decision_green
			if self.player.role() == "green":
			# green's decision page
				assert ("Your color in the experiment: <strong> green </strong>" in self.html)
				assert ("Advice formulated by other students: <strong> " + str(self.player.advice) +" </strong>" in self.html)
				yield SubmissionMustFail(views.Decision_green, {"decision_green": 5 })
				yield SubmissionMustFail(views.Decision_green, {"decision_green": "Z" })

				# check that the advice is implemented if green has a timeout
				if self.case == "timeout":
					yield Submission(views.Decision_green, timeout_happened=True)
				else:
					yield (views.Decision_green, {"decision_green": "C" })
			

		# page 4: Intro Part II
			if self.session.config["treatment"] == "public":
				if self.player.role() == "red":
					assert ("Your color in the experiment is <strong> red </strong>." in self.html)
				if self.player.role() == "blue":
					assert ("Your color in the experiment is <strong> blue </strong>." in self.html)
				if self.player.role() == "green":
					assert ("Your color in the experiment is <strong> green </strong>." in self.html)

				yield (views.Intro_Part_II)

		# page 5: Revelation
		if self.round_number <= len(self.subsession.get_groups()):

			if self.session.config["treatment"] == "public":

				# For red players who have to stand up "now"
				if self.player.role() == "red" and self.player.return_group_id() == self.player.round_number:
					# if they failed to take a decision
					if self.group.return_red_timeout() == 1:
						assert ("Therefore the advice of the other students was implemented: <strong>" + str(self.subsession.return_red_decision()) +"</strong> <br>" in self.html)
						assert ("Your group number: <strong> "+ str(self.player.round_number) + " </strong>" in self.html)
					# if they took a decision
					else:
						assert ("Your group number: <strong> " + str(self.player.round_number) + " </strong> <br>" in self.html)
						assert ("Your choice: <strong>" + str(self.subsession.return_red_decision()) + "</strong>" in self.html)

				# For blue and green players in groups with the red player standing up "now"
				elif self.player.role() != "red" and self.player.return_group_id() == self.player.round_number:
					# if the red players failed to take a decision:
					if self.group.return_red_timeout() == 1:
						assert ("The red player in your group did not indicate any decision." in self.html)
						assert ("Therefore the advice of the other students was implemented: <strong>" + str(self.subsession.return_red_decision()) + "</strong> <br>" in self.html)
					# if they took a decision 
					else:
						assert ("The red player in your group chose option <strong>" + str(self.subsession.return_red_decision()) + "</strong>." in self.html)

				# For all others in the subsession 
				else:
					# if the current red player failed to take a decision:
					if self.subsession.returns_red_timeout() == 1:
						assert ("The red player in group " +str(self.player.round_number) + " did not make a decision. <br>" in self.html)
					# If he took a decision:
					else:
						assert ("The red player in group " + str(self.player.round_number) + " chose option " + str(self.subsession.return_red_decision()) in self.html)

				yield (views.Revelation)

		
		if self.round_number == len(self.subsession.get_groups()):

		# page 6: Results	
			# check if payoffs are calculated correctly
			yield (views.Results)

			# if all players have a timeout, they get a payoff of 0
			if self.case == "timeout":
				players_payoff = c(0)
				
			# if only red has a timeout, s/he should get no payoff
			elif self.case == "timeout_red":
				if self.player.role() == "red":
					players_payoff = c(0)
				if self.player.role() == "blue":
					players_payoff = Constants.endowment + Constants.payoff_matrix["blue"][self.session.config['advice']]
				if self.player.role() == "green":
					players_payoff = Constants.endowment + Constants.payoff_matrix["green"][self.session.config['advice']]

			# If no player failed to make a decision
			else:
				if self.player.role() == "red":
					players_payoff = Constants.endowment + Constants.payoff_matrix["red"][self.group.in_round(1).decision_red]
				if self.player.role() == "blue":
					players_payoff = Constants.endowment + Constants.payoff_matrix["blue"][self.group.in_round(1).decision_red]
				if self.player.role() == "green":
					players_payoff = Constants.endowment + Constants.payoff_matrix["green"][self.group.in_round(1).decision_red]

			assert self.player.payoff == players_payoff

			# page 7: Questionnaire
			invalid_age_data = {
			"age": -1,
			"gender": "male",
			"studies": "Economics",
			"studies2": False,
			"risk": "neutral",
			"country": "DK"
			}

			yield SubmissionMustFail(views.Questionnaire, invalid_age_data)

			invalid_gender_data = {
			"age": 25,             
			"gender": 5, 
			"studies": "Economics",
			"studies2": False,
			"risk": "neutral",
			"country": "DK"
			}

			yield SubmissionMustFail(views.Questionnaire, invalid_gender_data)

			# Here we indicate a field of studies but say that we are not a student.
			invalid_studies_1 = {
			"age": 25,
			"gender": "other",
			"studies": "English",
			"studies2": True,
			"risk": "risk averse",
			"country": "DK"
			}

			yield SubmissionMustFail(views.Questionnaire, invalid_studies_1)

			# Here we indicate no field of studies and don't say that we are a non-student.
			invalid_studies_2 = {
			"age": 25,
			"gender": "other",
			"studies": "",
			"studies2": False,
			"risk": "risk averse",
			"country": "DK"
			}

			yield SubmissionMustFail(views.Questionnaire, invalid_studies_2)

			invalid_risk = {
			"age": 25,
			"gender": "other",
			"studies": "French",
			"studies2": False,
			"risk": "",
			"country": "DK"
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
			"country": "DK"
			}

			yield (views.Questionnaire, valid_survey_data)
