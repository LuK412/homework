from otree.api import Currency as c, currency_range
from otree.api import SubmissionMustFail
from otree.api import Submission
from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

	def play_round(self):

		# check role assignment
		if self.player.id_in_group == 1:
			assert self.player.role() == 'red'
		
		if self.player.id_in_group == 2:
			assert self.player.role() == 'blue'

		if self.player.id_in_group == 3:
			assert self.player.role() == 'green'

		# page 1
		yield (views.Instructions)    

		# page 2
		if self.player.role() == 'red':
			# proposer page
			yield SubmissionMustFail(views.Decision_red, {'decision_red': 5 }) 
			yield SubmissionMustFail(views.Decision_red, {'decision_red': "Z" })

			yield (views.Decision_red, {'decision_red': "C" })
			
			#assert self.group.proposer_share == c(60) payoff

		# page 2
		if self.player.role() == 'blue':
			# proposer page
			yield SubmissionMustFail(views.Decision_blue, {'decision_blue': 5 }) 
			yield SubmissionMustFail(views.Decision_blue, {'decision_blue': "Z" })

			yield (views.Decision_blue, {'decision_blue': "C" })
			
			#assert self.group.proposer_share == c(60) payoff

		# page 2
		if self.player.role() == 'green':
			# proposer page
			yield SubmissionMustFail(views.Decision_green, {'decision_green': 5 }) 
			yield SubmissionMustFail(views.Decision_green, {'decision_green': "Z" })

			yield (views.Decision_green, {'decision_green': "C" })
			
			#assert self.group.proposer_share == c(60) payoff

		yield (views.Revelation)

		yield (views.Revelation)

		yield (views.Results)

		invalid_age_data = {
			"age": -1,
			"gender": "male",
			"studies": "Economics",
			"studies2": False,
			"risk": "neutral",
			"country": ""
		}

		yield SubmissionMustFail(views.Questionnaire, invalid_age_data)

		invalid_gender_data = {
			'age': 25,             
			'gender': 5, 
			"studies": "Economics",
			"studies2": False,
			"risk": "neutral",
			"country": ""
		}

		yield SubmissionMustFail(views.Questionnaire, invalid_gender_data)

		valid_survey_data = {
			'age': 25,
			'gender': 'male',
			"studies": "Economics",
			"studies2": False,
			"risk": "neutral",
			"country": ""
		}
		yield (views.Questionnaire, valid_survey_data)


		yield (views.LastPage)

	