import http.client
import json
import time, threading
import random
# from timer import timer, flag, flag_change
flag = False
class SeasonQuiz:
    def __init__(self):
        self.season = self.get_season()
        self.teams = self.load_teams()

    def get_season(self):
        connection = http.client.HTTPConnection('api.football-data.org')
        headers = {'X-Auth-Token': '539afaf8de7a49ce82df958926dee1c0'}
        connection.request('GET', '/v2/competitions/PL/matches/?season=2018', None, headers)
        response = json.loads(connection.getresponse().read().decode())
        return response
    
    def make_game_dicts(self, response):
        games = []
        for game in response['matches']:
            if game['score']['winner'] == 'AWAY_TEAM':
                winner = game['awayTeam']['name']
            else:
                winner = game['homeTeam']['name']
            match = {
                'Matchday': game['matchday'],
                'Home Team': game['homeTeam']['name'],
                'Away Team': game['awayTeam']['name'],
                'Score': f"{game['score']['fullTime']['homeTeam']}:{game['score']['fullTime']['awayTeam']}",
                'Winner': winner
            }
            games.append(match)
        return games
    
    def load_teams(self):
        connection = http.client.HTTPConnection('api.football-data.org')
        headers = {'X-Auth-Token': '539afaf8de7a49ce82df958926dee1c0'}
        connection.request('GET', '/v2/competitions/PL/teams', None, headers)
        teams = json.loads(connection.getresponse().read().decode())
        return teams
    
    def load_players(self, team):
        connection = http.client.HTTPConnection('api.football-data.org')
        headers = {'X-Auth-Token': '539afaf8de7a49ce82df958926dee1c0'}
        connection.request('GET', f'/v2/teams/{team}', None, headers)
        players = json.loads(connection.getresponse().read().decode())
        return players
    
    def get_teams(self, teams):
        teams_list = [x['name'] for x in teams['teams']]
        return teams_list
    
    def get_team_ids(self, teams):
        team_ids = {}
        for team in teams['teams']:
            team_ids[team['name']] = team['id']
        return team_ids



    def timer(self):
        # print(time.ctime())
        t = threading.Timer(25, self.flag_change).start()
        # threading.Timer(90, countdown_warning).start()
    def flag_change(self):
        global flag
        flag = True


    def question_one(self):
        print('Welcome to the 2019 Football Quiz!')
        games = self.make_game_dicts(self.season)
        print('First question: ')

    def question_two(self):
        teams_list = self.get_teams(self.teams)
        teams_ids = self.get_team_ids(self.teams)
        print('Welcome to Round two! The Team Round.')
        print("""In this Round, you will be presented with one random Premier League team. You will have
        five minutes to name as many players from this team as you can!
        """)
        input('When you are ready, hit enter! ')
        team = random.choice(teams_list)
        team_response = self.load_players(teams_ids[team])
        players = [x['name'] for x in team_response['squad']]
        upper_case_players = [x.upper() for x in players]
        print(f'Your team is {team}')

        print('Your time starts in 3....')
        time.sleep(1)
        print('2....')
        time.sleep(1)
        print('1.....')
        time.sleep(1)
        print('GO!')
        points = 0
        self.timer()
        while flag == False:
            answer = input('Enter a players name: ').upper()
            time.sleep(0.5)
            if answer in players:
                points += 1
                print('Correct answer! ')
            else:
                print('Who?')
        input('Times up! Hit enter to return to the main menu: ')

    
    def run(self):
        question_1 = self.question_one()
        question_2 = self.question_two()
