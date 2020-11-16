from menu.menu import Menu
from settings import Settings
from quiz import SeasonQuiz
import http.client
import json
import time

class FootballApp:
    def __init__(self):
        self.menu = Menu()
        self.settings = Settings()
        self.quiz = SeasonQuiz()
    def get_response(self, selection):
        setting = self.settings.settings[selection - 1]
        connection = http.client.HTTPConnection('api.football-data.org')
        headers = {'X-Auth-Token': '539afaf8de7a49ce82df958926dee1c0'}
        connection.request('GET', f'/v2{setting}', None, headers)
        response = json.loads(connection.getresponse().read().decode())
        return response
    
    def get_top_scorers(self, data):
        goalscorers = {}
        for scorer in data['scorers']:
            goalscorers[scorer['player']['name']] = scorer['numberOfGoals']
        return goalscorers

    def display_scorers(self, data):
        for scorer, goals in data.items():
            print(f'{scorer} has scored {goals} goals this season so far.')
    
    def display_standings(self, data):
        table = data['standings'][0]['table']
        print('POSITION | TEAM | W | D | L | POINTS | GAMES')
        for team in table:
            print(team['position'], team['team']['name'], team['won'], team['draw'], team['lost'], team['points'], team['playedGames'])
    
    def show_more_table_stats_bool(self, data):
        table = data['standings'][0]['table']
        selection2 = input('Would you like to see some more detailed stats? ')
        if selection2 == 'Y':
            print('What would you like to see?')
            selection = self.show_table_menu()
            if selection == 1:
                self.show_team_form(table)
            elif selection == 2:
                self.show_goal_difference(table)
            else:
                return
        else: 
            print('Okay!')
            return
    def show_table_menu(self):
        print("""Please, select an option below by entering a number:
            [1] Form Table
            [2] Goal Difference
            [3] Exit
            """)
        while True:
            try:
                return int(input("Enter a number: "))
            except ValueError:
                print("Please enter a valid number.")

    def show_team_form(self, table):
        form_table = {}
        for team in table:
            form_table[team['team']['name']] = team['form']
        for team, form in form_table.items():
            print(f"{team}'s form is {form} over the last five games.")
        # team = input('Whose form would you like to see? ')
        

    def show_goal_difference(self, table):
        goal_difference = []
        for team in table:
            gd = {
                'Goals Scored': team['goalsFor'],
                'Goals Against': team['goalsAgainst'],
                'Goal Difference': team['goalDifference']
            }
            goal_difference.append(gd)
        for goald in goal_difference:
            print(goald)
        


        

    def run(self):
        while True:
            selection = self.menu._show_menu_and_get_selection()
            if selection == 1:
                scorers = self.get_top_scorers(self.get_response(selection))
                self.display_scorers(scorers)
                input('Please hit enter to return to the main menu: ')
            elif selection == 2:
                table_response = self.get_response(selection)
                standings = self.display_standings(table_response)
                self.show_more_table_stats_bool(table_response)
                input('Please hit enter to return to the main menu: ')
                

            elif selection == 3:
                quiz = self.quiz.run()
                
            elif selection == 4:
                print('Thank you. Bye!')
                time.sleep(1)
                exit()



if __name__ == '__main__':
    football = FootballApp()
    football.run()
