import random
from prettytable import PrettyTable
import time
from itertools import combinations

# Data Pool
# All the teams in the game apart from the user, this block of code should be able to be modified w/o altering the programs execution

TEAM_TABLE = [
    {"name": "Manchester City", "games_played": 0, "points": 0, "goals_for": 0, "goals_against": 0,
     "goal_difference": 0},
    {"name": "Bayern Munich", "games_played": 0, "points": 0, "goals_for": 0, "goals_against": 0, "goal_difference": 0},
    {"name": "Liverpool FC", "games_played": 0, "points": 0, "goals_for": 0, "goals_against": 0, "goal_difference": 0},
    {"name": "Real Madrid", "games_played": 0, "points": 0, "goals_for": 0, "goals_against": 0, "goal_difference": 0},
    {"name": "Arsenal", "games_played": 0, "points": 0, "goals_for": 0, "goals_against": 0, "goal_difference": 0},
    {"name": "Barcelona", "games_played": 0, "points": 0, "goals_for": 0, "goals_against": 0, "goal_difference": 0},
    {"name": "Newcastle", "games_played": 0, "points": 0, "goals_for": 0, "goals_against": 0, "goal_difference": 0},
    {"name": "Napoli", "games_played": 0, "points": 0, "goals_for": 0, "goals_against": 0, "goal_difference": 0},
    {"name": "Dortmund", "games_played": 0, "points": 0, "goals_for": 0, "goals_against": 0, "goal_difference": 0},
    {"name": "PSG", "games_played": 0, "points": 0, "goals_for": 0, "goals_against": 0, "goal_difference": 0}
]


# CLASSES
# create your own team at the start of the game
class Team:
    def __init__(self, team_name, manager_name, overall=60, off_rating=60, def_rating=60, PGPG=0.0, PCPG=0.0,
                 manager_rating=60):
        # all the values are default when you start the game but as you progress and wih or lose games the values can either increase or decrease
        self.name = team_name  # The name of your team you want to create
        self.manager = manager_name  # The name of your manager, this could be your name or an arbitrary
        self.manager_rating = manager_rating
        self.overall = overall
        self.off_rating = off_rating
        self.def_rating = def_rating
        self.PGPG = PGPG
        self.PCPG = PCPG


class Game:
    def calculate_difficulty(self, other_team):
        # Weights for each parameter
        # Weights for each parameter
        overall_weight = 0.3
        PGPG_weight = 0.2
        PCPG_weight = 0.2
        manager_rating_weight = 0.3
        # Calculating the difficulty of the match
        my_team_overall = select_team().overall
        other_team_overall = get_other_overall(other_team)

        my_team_PGPG = select_team().PGPG
        other_team_PGPG = get_other_PGPG(other_team)

        my_team_PCPG = select_team().PCPG
        other_team_PCPG = get_other_PCPG(other_team)

        my_team_manager_rating = select_team().manager_rating
        other_team_manager_rating = get_manager_rating(other_team)

        overall_difficulty = (other_team_overall - my_team_overall) * overall_weight
        PGPG_difficulty = (other_team_PGPG - my_team_PGPG) * PGPG_weight
        PCPG_difficulty = (other_team_PCPG - my_team_PCPG) * PCPG_weight
        manager_rating_difficulty = (other_team_manager_rating - my_team_manager_rating) * manager_rating_weight

        # Combine the scores into a single difficulty score
        difficulty_score = overall_difficulty + PGPG_difficulty + PCPG_difficulty + manager_rating_difficulty
        if 0 >= difficulty_score < -1:
            return "above 90% chances of winning"
        elif 0 <= difficulty_score < 2:
            return "below 80% chances of winning"
        else:
            return "below 60% chances of winning"


class Season:
    def __init__(self):
        self.teams = TEAM_TABLE
        self.sigma = random.uniform(0, 4)

    def calculate_avg_scores(self, team1, team2):
        self.team1_avg_score = max(0, round(random.normalvariate(team1.PGPG, self.sigma)))
        self.team2_avg_score = max(0, round(random.normalvariate(team2.PGPG, self.sigma)))

    def match_winner(self, team1, team2):
        # Calculate average scores only once at the beginning of the match
        self.calculate_avg_scores(team1, team2)

        team1_score = max(self.team1_avg_score, team2.PCPG * 4)
        team2_score = max(self.team2_avg_score, team1.PCPG * 4)

        team1_score_f = round(max(0, team1_score))
        team2_score_f = round(max(0, team2_score))

        if team1_score_f > team2_score_f:
            return team1.name
        elif team2_score_f > team1_score_f:
            return team2.name
        else:
            return "Draw"

    def calculate_scores(self, team1, team2):
        # Use the precalculated average scores
        team1_score = max(self.team1_avg_score, team2.PCPG * 4)
        team2_score = max(self.team2_avg_score, team1.PCPG * 4)

        team1_score_f = round(max(0, team1_score))
        team2_score_f = round(max(0, team2_score))

        return team1_score_f, team2_score_f

    def goals_for_team1(self, team1, team2):
        team1_score_f, _ = self.calculate_scores(team1, team2)
        return team1_score_f

    def goals_for_team2(self, team1, team2):
        _, team2_score_f = self.calculate_scores(team1, team2)
        return team2_score_f

    def goals_against_team1(self, team1, team2):
        _, team2_score_f = self.calculate_scores(team1, team2)
        return team2_score_f

    def goals_against_team2(self, team1, team2):
        team1_score_f, _ = self.calculate_scores(team1, team2)
        return team1_score_f

    def display_initial_table(self):
        table = PrettyTable()
        table.field_names = ["Team", "Games Played", "Points", "Goals For(GF)", "Goals Against(GA)",
                             "Goal Difference(GD)"]
        sorted_teams = sorted(self.teams, key=lambda x: x['points'], reverse=True)

        for team in sorted_teams:
            table.add_row(
                [team['name'], team["games_played"], team['points'], team['goals_for'], team['goals_against'],
                 team['goal_difference']])
        print(table)

    def update_table(self, team1, team2):
        winner = self.match_winner(team1, team2)
        for teams in self.teams:
            if teams["name"] == team1.name:
                if winner == team1.name:
                    teams["points"] += 3
                    teams["goals_for"] += self.goals_for_team1(team1, team2)
                    teams["goals_against"] += self.goals_against_team1(team1, team2)
                    teams["games_played"] += 1
                    teams["goal_difference"] = teams["goals_for"] - teams["goals_against"]
                elif (winner == "Draw") and (self.goals_for_team1(team1, team2) == self.goals_against_team1(team1, team2)) :
                    teams["points"] += 1
                    teams["goals_for"] += self.goals_for_team1(team1, team2)
                    teams["goals_against"] += self.goals_against_team1(team1, team2)
                    teams["games_played"] += 1
                    teams["goal_difference"] = teams["goals_for"] - teams["goals_against"]
                else:
                    teams["points"] += 0
                    teams["goals_for"] += self.goals_for_team1(team1, team2)
                    teams["goals_against"] += self.goals_against_team1(team1, team2)
                    teams["games_played"] += 1
                    teams["goal_difference"] = teams["goals_for"] - teams["goals_against"]


            elif teams["name"] == team2.name:
                if winner == team2.name:
                    teams["points"] += 3
                    teams["goals_for"] += self.goals_for_team2(team1, team2)
                    teams["goals_against"] += self.goals_against_team2(team1, team2)
                    teams["games_played"] += 1
                    teams["goal_difference"] = teams["goals_for"] - teams["goals_against"]
                elif (winner == "Draw") and (self.goals_for_team2(team1, team2) == self.goals_against_team2(team1, team2)):
                    teams["points"] += 1
                    teams["goals_for"] += self.goals_for_team2(team1, team2)
                    teams["goals_against"] += self.goals_against_team2(team1, team2)
                    teams["games_played"] += 1
                    teams["goal_difference"] = teams["goals_for"] - teams["goals_against"]
                else:
                    teams["points"] += 0
                    teams["goals_for"] += self.goals_for_team2(team1, team2)
                    teams["goals_against"] += self.goals_against_team2(team1, team2)
                    teams["games_played"] += 1
                    teams["goal_difference"] = teams["goals_for"] - teams["goals_against"]


Manchester_City = Team("Manchester City", "Pep Guardiola", 96, 96, 98, 2.8, 0.3, 90)
Bayern_Munich = Team("Bayern Munich", "Thomas Tuchel", 96, 98, 94, 3.0, 0.6, 86)
Liverpool_FC = Team("Liverpool FC", "Jurgen Klopp", 95, 95, 95, 2.7, 0.6, 88)
Real_Madrid = Team("Real Madrid", "Carlo Ancelotti", 95, 96, 94, 2.8, 0.6, 88)
Arsenal = Team("Arsenal", "Mikel Arteta", 94, 93, 95, 2.5, 0.6, 85)
Barcelona_FC = Team("Barcelona", "Xavi Hernandez", 93, 93, 97, 2.5, 0.4, 84)
Newcastle = Team("Newcastle", "Eddie Howe", 92, 91, 92, 2.5, 0.7, 82)
Napoli = Team("Napoli", "Rudi Garcia", 91, 91, 92, 2.5, 0.8, 82)
Dortmund = Team("Dortmund", "Edin Terzić", 91, 91, 92, 2.3, 1.75, 81)
PSG = Team("PSG", "Luis Enrique", 90, 91, 92, 2.4, 0.75)

ALL_TEAMS = [
    Manchester_City, Bayern_Munich, Liverpool_FC, Real_Madrid, Arsenal, Barcelona_FC, Newcastle, Napoli, Dortmund, PSG
]


# Function Pool
def get_other_overall(team_name):
    return team_name.overall


def get_other_PGPG(team_name):
    return team_name.PGPG


def get_other_PCPG(team_name):
    return team_name.PCPG


def get_manager_rating(team_name):
    return team_name.manager_rating


def display_team_menu():
    print("These are the list of teams:")
    for i, team in enumerate(ALL_TEAMS, 1):
        print(f"{i}. {team.name}")



def clear_screen():
    print('\n' * 500)


def select_team(choice):
    while True:
        try:
            if 1 <= choice <= len(ALL_TEAMS):
                return ALL_TEAMS[choice - 1]
            else:
                print("Invalid choice. Please enter a number between 1 and {}.".format(
                    len(ALL_TEAMS)))
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            break



def play_match(choice, team):
    print(f"{select_team(choice).name} vs. {team.name}")
    # Simulate the match logic here
    time.sleep(5)

def main():
    print("""
    
                    ··························································································
                    :                                                                                        :
                    :  ▄█     █▄     ▄████████  ▄█        ▄████████  ▄██████▄    ▄▄▄▄███▄▄▄▄      ▄████████  :
                    : ███     ███   ███    ███ ███       ███    ███ ███    ███ ▄██▀▀▀███▀▀▀██▄   ███    ███  :
                    : ███     ███   ███    █▀  ███       ███    █▀  ███    ███ ███   ███   ███   ███    █▀   :
                    : ███     ███  ▄███▄▄▄     ███       ███        ███    ███ ███   ███   ███  ▄███▄▄▄      :
                    : ███     ███ ▀▀███▀▀▀     ███       ███        ███    ███ ███   ███   ███ ▀▀███▀▀▀      :
                    : ███     ███   ███    █▄  ███       ███    █▄  ███    ███ ███   ███   ███   ███    █▄   :
                    : ███ ▄█▄ ███   ███    ███ ███▌    ▄ ███    ███ ███    ███ ███   ███   ███   ███    ███  :
                    :  ▀███▀███▀    ██████████ █████▄▄██ ████████▀   ▀██████▀   ▀█   ███   █▀    ██████████  :
                    :                                                                                        :
                    ··························································································   
    """)
    time.sleep(2)
    print("""
                                                    ······················
                                                    :                    :
                                                    :   █████            :
                                                    :  ░░███             :
                                                    :  ███████   ██████  :
                                                    : ░░░███░   ███░░███ :
                                                    :   ░███   ░███ ░███ :
                                                    :   ░███ ██░███ ░███ :
                                                    :   ░░█████░░██████  :
                                                    :    ░░░░░  ░░░░░░   :
                                                    :                    :
                                                    ······················  
    """)
    time.sleep(2)
    print("""
                    ·················································································································
                    :   ▄████████  ▄██████▄   ▄██████▄      ███     ▀█████████▄     ▄████████  ▄█        ▄█                         :
                    :  ███    ███ ███    ███ ███    ███ ▀█████████▄   ███    ███   ███    ███ ███       ███                         :
                    :  ███    █▀  ███    ███ ███    ███    ▀███▀▀██   ███    ███   ███    ███ ███       ███                         :
                    : ▄███▄▄▄     ███    ███ ███    ███     ███   ▀  ▄███▄▄▄██▀    ███    ███ ███       ███                         :
                    :▀▀███▀▀▀     ███    ███ ███    ███     ███     ▀▀███▀▀▀██▄  ▀███████████ ███       ███                         :
                    :  ███        ███    ███ ███    ███     ███       ███    ██▄   ███    ███ ███       ███                         :
                    :  ███        ███    ███ ███    ███     ███       ███    ███   ███    ███ ███▌    ▄ ███▌    ▄                   :
                    :  ███         ▀██████▀   ▀██████▀     ▄████▀   ▄█████████▀    ███    █▀  █████▄▄██ █████▄▄██                   :
                    :                                                                         ▀         ▀                           :
                    :   ▄████████ ███    █▄     ▄███████▄    ▄███████▄  ▄██████▄     ▄████████     ███        ▄████████    ▄████████:
                    :  ███    ███ ███    ███   ███    ███   ███    ███ ███    ███   ███    ███ ▀█████████▄   ███    ███   ███    ███:
                    :  ███    █▀  ███    ███   ███    ███   ███    ███ ███    ███   ███    ███    ▀███▀▀██   ███    █▀    ███    ███:
                    :  ███        ███    ███   ███    ███   ███    ███ ███    ███  ▄███▄▄▄▄██▀     ███   ▀  ▄███▄▄▄      ▄███▄▄▄▄██▀:
                    :▀███████████ ███    ███ ▀█████████▀  ▀█████████▀  ███    ███ ▀▀███▀▀▀▀▀       ███     ▀▀███▀▀▀     ▀▀███▀▀▀▀▀  :
                    :         ███ ███    ███   ███          ███        ███    ███ ▀███████████     ███       ███    █▄  ▀███████████:
                    :   ▄█    ███ ███    ███   ███          ███        ███    ███   ███    ███     ███       ███    ███   ███    ███:
                    : ▄████████▀  ████████▀   ▄████▀       ▄████▀       ▀██████▀    ███    ███    ▄████▀     ██████████   ███    ███:
                    :                                                               ███    ███                            ███    ███:
                    ·················································································································
    """)
    time.sleep(4)
    clear_screen()
    time.sleep(2)
    display_team_menu()
    choice = int(input("""
    You're a supporter of a football team and youre trying to monitor your teams stats
    
    Select the team you want to support from the menu
    """))
    clear_screen()
    print(f"You're now a supporter of {select_team(choice).name}")
    time.sleep(5)
    clear_screen()
    print("This is your table. You'll see it after every game and know which team is currently on top")
    season = Season()
    season.display_initial_table()
    user = input("To go next click (return) ").upper()
    clear_screen()
    game = Game()

    #First Week
    print("""
    
                           ···················································
                           : ▄█     █▄     ▄████████    ▄████████    ▄█   ▄█▄:
                           :███     ███   ███    ███   ███    ███   ███ ▄███▀:
                           :███     ███   ███    █▀    ███    █▀    ███▐██▀  :
                           :███     ███  ▄███▄▄▄      ▄███▄▄▄      ▄█████▀   :
                           :███     ███ ▀▀███▀▀▀     ▀▀███▀▀▀     ▀▀█████▄   :
                           :███     ███   ███    █▄    ███    █▄    ███▐██▄  :
                           :███ ▄█▄ ███   ███    ███   ███    ███   ███ ▀███▄:
                           : ▀███▀███▀    ██████████   ██████████   ███   ▀█▀:
                           :                                        ▀        :
                           ···················································
                                              ········
                                              : ████ :
                                              :░░███ :
                                              : ░███ :
                                              : ░███ :
                                              : ░███ :
                                              : ░███ :
                                              : █████:
                                              :░░░░░ :
                                              ········
    """)
    user = input("To start click (return) ").upper()
    clear_screen()
    #My game
    print("First match up !!!")
    print("Manchester City vs PSG")
    season.match_winner(Manchester_City, PSG)
    season.update_table(Manchester_City, PSG)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Bayern Munich vs Dortmund")
    season.match_winner(Bayern_Munich, Dortmund)
    season.update_table(Bayern_Munich, Dortmund)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()



    #Other Games
    clear_screen()
    print("Next Match Liverpool vs Napoli")
    season.match_winner(Liverpool_FC, Napoli)
    season.update_table(Liverpool_FC, Napoli)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Real Madrid vs Newcastle")
    season.match_winner(Real_Madrid, Newcastle)
    season.update_table(Real_Madrid, Newcastle)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()


    clear_screen()
    print("Next Match Arsenal vs Barcelona")
    season.match_winner(Arsenal, Barcelona_FC)
    season.update_table(Arsenal, Barcelona_FC)
    season.display_initial_table()
    user = input("To go to week 2 click (return) ").upper()


    print("""
    
                            ···················································
                           : ▄█     █▄     ▄████████    ▄████████    ▄█   ▄█▄:
                           :███     ███   ███    ███   ███    ███   ███ ▄███▀:
                           :███     ███   ███    █▀    ███    █▀    ███▐██▀  :
                           :███     ███  ▄███▄▄▄      ▄███▄▄▄      ▄█████▀   :
                           :███     ███ ▀▀███▀▀▀     ▀▀███▀▀▀     ▀▀█████▄   :
                           :███     ███   ███    █▄    ███    █▄    ███▐██▄  :
                           :███ ▄█▄ ███   ███    ███   ███    ███   ███ ▀███▄:
                           : ▀███▀███▀    ██████████   ██████████   ███   ▀█▀:
                           :                                        ▀        :
                           ···················································
                                           ·············
                                           :  ████████ :
                                           : ███░░░░███:
                                           :░░░    ░███:
                                           :   ███████ :
                                           :  ███░░░░  :
                                           : ███      █:
                                           :░██████████:
                                           :░░░░░░░░░░ :
                                           ·············   
    
    """)
    user = input("To start click (return) ").upper()
    clear_screen()
    print("Manchester City vs Dortmund")
    season.match_winner(Manchester_City, Dortmund)
    season.update_table(Manchester_City, Dortmund)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match PSG vs Napoli")
    season.match_winner(PSG, Napoli)
    season.update_table(PSG, Napoli)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Bayern Munich vs Newcastle")
    season.match_winner(Bayern_Munich, Newcastle)
    season.update_table(Bayern_Munich, Newcastle)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Liverpool vs Barcelona")
    season.match_winner(Liverpool_FC, Barcelona_FC)
    season.update_table(Liverpool_FC, Barcelona_FC)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Real Madrid vs Arsenal")
    season.match_winner(Real_Madrid, Arsenal)
    season.update_table(Real_Madrid, Arsenal)
    season.display_initial_table()
    user = input("To see go to week 3 click (return) ").upper()

    print("""

                                ···················································
                               : ▄█     █▄     ▄████████    ▄████████    ▄█   ▄█▄:
                               :███     ███   ███    ███   ███    ███   ███ ▄███▀:
                               :███     ███   ███    █▀    ███    █▀    ███▐██▀  :
                               :███     ███  ▄███▄▄▄      ▄███▄▄▄      ▄█████▀   :
                               :███     ███ ▀▀███▀▀▀     ▀▀███▀▀▀     ▀▀█████▄   :
                               :███     ███   ███    █▄    ███    █▄    ███▐██▄  :
                               :███ ▄█▄ ███   ███    ███   ███    ███   ███ ▀███▄:
                               : ▀███▀███▀    ██████████   ██████████   ███   ▀█▀:
                               :                                        ▀        :
                               ···················································
                                                   ·············
                                                   :  ████████ :
                                                   : ███░░░░███:
                                                   :░░░    ░███:
                                                   :   ██████░ :
                                                   :  ░░░░░░███:
                                                   : ███   ░███:
                                                   :░░████████ :
                                                   : ░░░░░░░░  :
                                                   ·············
                               
    """)
    user = input("To start click (return) ").upper()
    clear_screen()
    print("Manchester City vs Napoli")
    season.match_winner(Manchester_City, Napoli)
    season.update_table(Manchester_City, Napoli)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Dortmund vs Newcastle")
    season.match_winner(Dortmund, Newcastle)
    season.update_table(Dortmund, Newcastle)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next PSG vs Barcelona")
    season.match_winner(PSG, Barcelona_FC)
    season.update_table(PSG, Barcelona_FC)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Bayern Munich vs Arsenal")
    season.match_winner(Bayern_Munich, Arsenal)
    season.update_table(Bayern_Munich, Arsenal)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Liverpool vs Real Madrid")
    season.match_winner(Liverpool_FC, Real_Madrid)
    season.update_table(Liverpool_FC, Real_Madrid)
    season.display_initial_table()
    user = input("To see go to week 4 click (return) ").upper()

    print("""
    
                               ···················································
                               : ▄█     █▄     ▄████████    ▄████████    ▄█   ▄█▄:
                               :███     ███   ███    ███   ███    ███   ███ ▄███▀:
                               :███     ███   ███    █▀    ███    █▀    ███▐██▀  :
                               :███     ███  ▄███▄▄▄      ▄███▄▄▄      ▄█████▀   :
                               :███     ███ ▀▀███▀▀▀     ▀▀███▀▀▀     ▀▀█████▄   :
                               :███     ███   ███    █▄    ███    █▄    ███▐██▄  :
                               :███ ▄█▄ ███   ███    ███   ███    ███   ███ ▀███▄:
                               : ▀███▀███▀    ██████████   ██████████   ███   ▀█▀:
                               :                                        ▀        :
                               ···················································
                                               ···············
                                               : █████ █████ :
                                               :░░███ ░░███  :
                                               : ░███  ░███ █:
                                               : ░███████████:
                                               : ░░░░░░░███░█:
                                               :       ░███░ :
                                               :       █████ :
                                               :      ░░░░░  :
                                               ···············
    
    """)
    user = input("To start click (return) ").upper()
    clear_screen()
    print("Manchester City vs Newcastle")
    season.match_winner(Manchester_City, Newcastle)
    season.update_table(Manchester_City, Newcastle)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Napoli vs Barcelona")
    season.match_winner(Napoli, Barcelona_FC)
    season.update_table(Napoli, Barcelona_FC)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Dortmund vs Arsenal")
    season.match_winner(Dortmund, Arsenal)
    season.update_table(Dortmund, Arsenal)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match PSG vs Real Madrid")
    season.match_winner(PSG, Real_Madrid)
    season.update_table(PSG, Real_Madrid)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Bayern Munich vs Liverpool")
    season.match_winner(Bayern_Munich, Liverpool_FC)
    season.update_table(Bayern_Munich, Liverpool_FC)
    season.display_initial_table()
    user = input("To see go to week 5 click (return) ").upper()


    print("""
    
                               ···················································
                               : ▄█     █▄     ▄████████    ▄████████    ▄█   ▄█▄:
                               :███     ███   ███    ███   ███    ███   ███ ▄███▀:
                               :███     ███   ███    █▀    ███    █▀    ███▐██▀  :
                               :███     ███  ▄███▄▄▄      ▄███▄▄▄      ▄█████▀   :
                               :███     ███ ▀▀███▀▀▀     ▀▀███▀▀▀     ▀▀█████▄   :
                               :███     ███   ███    █▄    ███    █▄    ███▐██▄  :
                               :███ ▄█▄ ███   ███    ███   ███    ███   ███ ▀███▄:
                               : ▀███▀███▀    ██████████   ██████████   ███   ▀█▀:
                               :                                        ▀        :
                               ···················································
                                                 ·············
                                                 : ██████████:
                                                 :░███░░░░░░█:
                                                 :░███     ░ :
                                                 :░█████████ :
                                                 :░░░░░░░░███:
                                                 : ███   ░███:
                                                 :░░████████ :
                                                 : ░░░░░░░░  :
                                                 ·············    
    
    """)
    user = input("To start click (return) ").upper()
    clear_screen()
    print("Manchester City vs Barcelona")
    season.match_winner(Manchester_City, Barcelona_FC)
    season.update_table(Manchester_City, Barcelona_FC)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Newcastle vs Arsenal")
    season.match_winner(Newcastle, Arsenal)
    season.update_table(Newcastle, Arsenal)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Napoli vs Real Madrid")
    season.match_winner(Napoli, Real_Madrid)
    season.update_table(Napoli, Real_Madrid)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Dortmund vs Liverpool")
    season.match_winner(Dortmund, Liverpool_FC)
    season.update_table(Dortmund, Liverpool_FC)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match PSG vs Bayern Munich")
    season.match_winner(PSG, Bayern_Munich)
    season.update_table(PSG, Bayern_Munich)
    season.display_initial_table()
    user = input("To see go to week 6 click (return) ").upper()



    print("""

                                   ···················································
                                   : ▄█     █▄     ▄████████    ▄████████    ▄█   ▄█▄:
                                   :███     ███   ███    ███   ███    ███   ███ ▄███▀:
                                   :███     ███   ███    █▀    ███    █▀    ███▐██▀  :
                                   :███     ███  ▄███▄▄▄      ▄███▄▄▄      ▄█████▀   :
                                   :███     ███ ▀▀███▀▀▀     ▀▀███▀▀▀     ▀▀█████▄   :
                                   :███     ███   ███    █▄    ███    █▄    ███▐██▄  :
                                   :███ ▄█▄ ███   ███    ███   ███    ███   ███ ▀███▄:
                                   : ▀███▀███▀    ██████████   ██████████   ███   ▀█▀:
                                   :                                        ▀        :
                                   ···················································
                                                     ·············
                                                     :  ████████ :
                                                     : ███░░░░███:
                                                     :░███   ░░░ :
                                                     :░█████████ :
                                                     :░███░░░░███:
                                                     :░███   ░███:
                                                     :░░████████ :
                                                     : ░░░░░░░░  :
                                                     ·············

        """)
    user = input("To start click (return) ").upper()
    clear_screen()
    print("Manchester City vs Arsenal")
    season.match_winner(Manchester_City, Arsenal)
    season.update_table(Manchester_City, Arsenal)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Barcelona vs Real Madrid")
    season.match_winner(Barcelona_FC, Real_Madrid)
    season.update_table(Barcelona_FC, Real_Madrid)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Newcastle vs Liverpool")
    season.match_winner(Newcastle, Liverpool_FC)
    season.update_table(Newcastle, Liverpool_FC)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Napoli vs Bayern Munich")
    season.match_winner(Napoli, Bayern_Munich)
    season.update_table(Napoli, Bayern_Munich)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Dortmund vs PSG")
    season.match_winner(Dortmund, PSG)
    season.update_table(Dortmund, PSG)
    season.display_initial_table()
    user = input("To see go to week 7 click (return) ").upper()

    print("""

                                   ···················································
                                   : ▄█     █▄     ▄████████    ▄████████    ▄█   ▄█▄:
                                   :███     ███   ███    ███   ███    ███   ███ ▄███▀:
                                   :███     ███   ███    █▀    ███    █▀    ███▐██▀  :
                                   :███     ███  ▄███▄▄▄      ▄███▄▄▄      ▄█████▀   :
                                   :███     ███ ▀▀███▀▀▀     ▀▀███▀▀▀     ▀▀█████▄   :
                                   :███     ███   ███    █▄    ███    █▄    ███▐██▄  :
                                   :███ ▄█▄ ███   ███    ███   ███    ███   ███ ▀███▄:
                                   : ▀███▀███▀    ██████████   ██████████   ███   ▀█▀:
                                   :                                        ▀        :
                                   ···················································
                                                    ·············
                                                    : ██████████:
                                                    :░███░░░░███:
                                                    :░░░    ███ :
                                                    :      ███  :
                                                    :     ███   :
                                                    :    ███    :
                                                    :   ███     :
                                                    :  ░░░      :
                                                    ·············

        """)
    user = input("To start click (return) ").upper()
    clear_screen()
    print("Manchester City vs Real Madrid")
    season.match_winner(Manchester_City, Real_Madrid)
    season.update_table(Manchester_City, Real_Madrid)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Arsenal vs Liverpool")
    season.match_winner(Arsenal, Liverpool_FC)
    season.update_table(Arsenal, Liverpool_FC)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Barcelona vs Bayern Munich")
    season.match_winner(Barcelona_FC, Bayern_Munich)
    season.update_table(Barcelona_FC, Bayern_Munich)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Newcastle vs PSG")
    season.match_winner(Newcastle, PSG)
    season.update_table(Newcastle, PSG)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Napoli vs Dortmund")
    season.match_winner(Napoli, Dortmund)
    season.update_table(Napoli, Dortmund)
    season.display_initial_table()
    user = input("To see go to week 8 click (return) ").upper()

    print("""

                                       ···················································
                                       : ▄█     █▄     ▄████████    ▄████████    ▄█   ▄█▄:
                                       :███     ███   ███    ███   ███    ███   ███ ▄███▀:
                                       :███     ███   ███    █▀    ███    █▀    ███▐██▀  :
                                       :███     ███  ▄███▄▄▄      ▄███▄▄▄      ▄█████▀   :
                                       :███     ███ ▀▀███▀▀▀     ▀▀███▀▀▀     ▀▀█████▄   :
                                       :███     ███   ███    █▄    ███    █▄    ███▐██▄  :
                                       :███ ▄█▄ ███   ███    ███   ███    ███   ███ ▀███▄:
                                       : ▀███▀███▀    ██████████   ██████████   ███   ▀█▀:
                                       :                                        ▀        :
                                       ···················································
                                                       ·············
                                                       :  ████████ :
                                                       : ███░░░░███:
                                                       :░███   ░███:
                                                       :░░████████ :
                                                       : ███░░░░███:
                                                       :░███   ░███:
                                                       :░░████████ :
                                                       : ░░░░░░░░  :
                                                      ·············

            """)
    user = input("To start click (return) ").upper()
    clear_screen()
    print("Manchester City vs Liverpool")
    season.match_winner(Manchester_City, Liverpool_FC)
    season.update_table(Manchester_City, Liverpool_FC)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Real Madrid vs Bayern Munich")
    season.match_winner(Real_Madrid, Bayern_Munich)
    season.update_table(Real_Madrid, Bayern_Munich)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Arsenal vs PSG")
    season.match_winner(Arsenal, PSG)
    season.update_table(Arsenal, PSG)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Barcelona vs Dortmund")
    season.match_winner(Barcelona_FC, Dortmund)
    season.update_table(Barcelona_FC, Dortmund)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Newcastle vs Napoli")
    season.match_winner(Newcastle, Napoli)
    season.update_table(Newcastle, Napoli)
    season.display_initial_table()
    user = input("To see go to week 9 click (return) ").upper()

    print("""

                                           ···················································
                                           : ▄█     █▄     ▄████████    ▄████████    ▄█   ▄█▄:
                                           :███     ███   ███    ███   ███    ███   ███ ▄███▀:
                                           :███     ███   ███    █▀    ███    █▀    ███▐██▀  :
                                           :███     ███  ▄███▄▄▄      ▄███▄▄▄      ▄█████▀   :
                                           :███     ███ ▀▀███▀▀▀     ▀▀███▀▀▀     ▀▀█████▄   :
                                           :███     ███   ███    █▄    ███    █▄    ███▐██▄  :
                                           :███ ▄█▄ ███   ███    ███   ███    ███   ███ ▀███▄:
                                           : ▀███▀███▀    ██████████   ██████████   ███   ▀█▀:
                                           :                                        ▀        :
                                           ···················································
                                                          ·············
                                                          :  ████████ :
                                                          : ███░░░░███:
                                                          :░███   ░███:
                                                          :░░█████████:
                                                          : ░░░░░░░███:
                                                          : ███   ░███:
                                                          :░░████████ :
                                                          : ░░░░░░░░  :
                                                          ·············
                """)
    user = input("To start click (return) ").upper()
    clear_screen()
    print("Manchester City vs Bayern Munich")
    season.match_winner(Manchester_City, Bayern_Munich)
    season.update_table(Manchester_City, Bayern_Munich)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Liverpool vs PSG")
    season.match_winner(Liverpool_FC, PSG)
    season.update_table(Liverpool_FC, PSG)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Real Madrid vs Dortmund")
    season.match_winner(Real_Madrid, Dortmund)
    season.update_table(Real_Madrid, Dortmund)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Arsenal vs Napoli")
    season.match_winner(Arsenal, Napoli)
    season.update_table(Arsenal, Napoli)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Barcelona vs Newcastle")
    season.match_winner(Barcelona_FC, Newcastle)
    season.update_table(Barcelona_FC, Newcastle)
    season.display_initial_table()
    user = input("To see go to week 10 click (return) ").upper()

    print("""

                               ···················································
                               : ▄█     █▄     ▄████████    ▄████████    ▄█   ▄█▄:
                               :███     ███   ███    ███   ███    ███   ███ ▄███▀:
                               :███     ███   ███    █▀    ███    █▀    ███▐██▀  :
                               :███     ███  ▄███▄▄▄      ▄███▄▄▄      ▄█████▀   :
                               :███     ███ ▀▀███▀▀▀     ▀▀███▀▀▀     ▀▀█████▄   :
                               :███     ███   ███    █▄    ███    █▄    ███▐██▄  :
                               :███ ▄█▄ ███   ███    ███   ███    ███   ███ ▀███▄:
                               : ▀███▀███▀    ██████████   ██████████   ███   ▀█▀:
                               :                                        ▀        :
                               ···················································
                                                 ····················
                                                 : ████     █████   :
                                                 :░░███   ███░░░███ :
                                                 : ░███  ███   ░░███:
                                                 : ░███ ░███    ░███:
                                                 : ░███ ░███    ░███:
                                                 : ░███ ░░███   ███ :
                                                 : █████ ░░░█████░  :
                                                 :░░░░░    ░░░░░░   :
                                                 ····················
        """)
    user = input("To start click (return) ").upper()
    clear_screen()
    # My game
    print("First match up !!!")
    print("Manchester City vs PSG")
    season.match_winner(Manchester_City, PSG)
    season.update_table(Manchester_City, PSG)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Bayern Munich vs Dortmund")
    season.match_winner(Bayern_Munich, Dortmund)
    season.update_table(Bayern_Munich, Dortmund)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    # Other Games
    clear_screen()
    print("Next Match Liverpool vs Napoli")
    season.match_winner(Liverpool_FC, Napoli)
    season.update_table(Liverpool_FC, Napoli)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Real Madrid vs Newcastle")
    season.match_winner(Real_Madrid, Newcastle)
    season.update_table(Real_Madrid, Newcastle)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Arsenal vs Barcelona")
    season.match_winner(Arsenal, Barcelona_FC)
    season.update_table(Arsenal, Barcelona_FC)
    season.display_initial_table()
    user = input("To go to week 11"
                 " click (return) ").upper()

    print("""

                                ···················································
                               : ▄█     █▄     ▄████████    ▄████████    ▄█   ▄█▄:
                               :███     ███   ███    ███   ███    ███   ███ ▄███▀:
                               :███     ███   ███    █▀    ███    █▀    ███▐██▀  :
                               :███     ███  ▄███▄▄▄      ▄███▄▄▄      ▄█████▀   :
                               :███     ███ ▀▀███▀▀▀     ▀▀███▀▀▀     ▀▀█████▄   :
                               :███     ███   ███    █▄    ███    █▄    ███▐██▄  :
                               :███ ▄█▄ ███   ███    ███   ███    ███   ███ ▀███▄:
                               : ▀███▀███▀    ██████████   ██████████   ███   ▀█▀:
                               :                                        ▀        :
                               ···················································
                                               ··············
                                               : ████  ████ :
                                               :░░███ ░░███ :
                                               : ░███  ░███ :
                                               : ░███  ░███ :
                                               : ░███  ░███ :
                                               : ░███  ░███ :
                                               : █████ █████:
                                               :░░░░░ ░░░░░ :
                                               ··············

        """)
    user = input("To start click (return) ").upper()
    clear_screen()
    print("Manchester City vs Dortmund")
    season.match_winner(Manchester_City, Dortmund)
    season.update_table(Manchester_City, Dortmund)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match PSG vs Napoli")
    season.match_winner(PSG, Napoli)
    season.update_table(PSG, Napoli)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Bayern Munich vs Newcastle")
    season.match_winner(Bayern_Munich, Newcastle)
    season.update_table(Bayern_Munich, Newcastle)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Liverpool vs Barcelona")
    season.match_winner(Liverpool_FC, Barcelona_FC)
    season.update_table(Liverpool_FC, Barcelona_FC)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Real Madrid vs Arsenal")
    season.match_winner(Real_Madrid, Arsenal)
    season.update_table(Real_Madrid, Arsenal)
    season.display_initial_table()
    user = input("To see go to week 12 click (return) ").upper()

    print("""

                                    ···················································
                                   : ▄█     █▄     ▄████████    ▄████████    ▄█   ▄█▄:
                                   :███     ███   ███    ███   ███    ███   ███ ▄███▀:
                                   :███     ███   ███    █▀    ███    █▀    ███▐██▀  :
                                   :███     ███  ▄███▄▄▄      ▄███▄▄▄      ▄█████▀   :
                                   :███     ███ ▀▀███▀▀▀     ▀▀███▀▀▀     ▀▀█████▄   :
                                   :███     ███   ███    █▄    ███    █▄    ███▐██▄  :
                                   :███ ▄█▄ ███   ███    ███   ███    ███   ███ ▀███▄:
                                   : ▀███▀███▀    ██████████   ██████████   ███   ▀█▀:
                                   :                                        ▀        :
                                   ···················································
                                                     ···················
                                                     : ████   ████████ :
                                                     :░░███  ███░░░░███:
                                                     : ░███ ░░░    ░███:
                                                     : ░███    ███████ :
                                                     : ░███   ███░░░░  :
                                                     : ░███  ███      █:
                                                     : █████░██████████:
                                                     :░░░░░ ░░░░░░░░░░ :
                                                     ···················

        """)
    user = input("To start click (return) ").upper()
    clear_screen()
    print("Manchester City vs Napoli")
    season.match_winner(Manchester_City, Napoli)
    season.update_table(Manchester_City, Napoli)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Dortmund vs Newcastle")
    season.match_winner(Dortmund, Newcastle)
    season.update_table(Dortmund, Newcastle)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next PSG vs Barcelona")
    season.match_winner(PSG, Barcelona_FC)
    season.update_table(PSG, Barcelona_FC)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Bayern Munich vs Arsenal")
    season.match_winner(Bayern_Munich, Arsenal)
    season.update_table(Bayern_Munich, Arsenal)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Liverpool vs Real Madrid")
    season.match_winner(Liverpool_FC, Real_Madrid)
    season.update_table(Liverpool_FC, Real_Madrid)
    season.display_initial_table()
    user = input("To see go to week 13 click (return) ").upper()

    print("""

                                   ···················································
                                   : ▄█     █▄     ▄████████    ▄████████    ▄█   ▄█▄:
                                   :███     ███   ███    ███   ███    ███   ███ ▄███▀:
                                   :███     ███   ███    █▀    ███    █▀    ███▐██▀  :
                                   :███     ███  ▄███▄▄▄      ▄███▄▄▄      ▄█████▀   :
                                   :███     ███ ▀▀███▀▀▀     ▀▀███▀▀▀     ▀▀█████▄   :
                                   :███     ███   ███    █▄    ███    █▄    ███▐██▄  :
                                   :███ ▄█▄ ███   ███    ███   ███    ███   ███ ▀███▄:
                                   : ▀███▀███▀    ██████████   ██████████   ███   ▀█▀:
                                   :                                        ▀        :
                                   ···················································
                                                  ···················
                                                  : ████   ████████ :
                                                  :░░███  ███░░░░███:
                                                  : ░███ ░░░    ░███:
                                                  : ░███    ██████░ :
                                                  : ░███   ░░░░░░███:
                                                  : ░███  ███   ░███:
                                                  : █████░░████████ :
                                                  :░░░░░  ░░░░░░░░  :
                                                  ···················

        """)
    user = input("To start click (return) ").upper()
    clear_screen()
    print("Manchester City vs Newcastle")
    season.match_winner(Manchester_City, Newcastle)
    season.update_table(Manchester_City, Newcastle)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Napoli vs Barcelona")
    season.match_winner(Napoli, Barcelona_FC)
    season.update_table(Napoli, Barcelona_FC)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Dortmund vs Arsenal")
    season.match_winner(Dortmund, Arsenal)
    season.update_table(Dortmund, Arsenal)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match PSG vs Real Madrid")
    season.match_winner(PSG, Real_Madrid)
    season.update_table(PSG, Real_Madrid)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Bayern Munich vs Liverpool")
    season.match_winner(Bayern_Munich, Liverpool_FC)
    season.update_table(Bayern_Munich, Liverpool_FC)
    season.display_initial_table()
    user = input("To see go to week 14 click (return) ").upper()

    print("""

                                   ···················································
                                   : ▄█     █▄     ▄████████    ▄████████    ▄█   ▄█▄:
                                   :███     ███   ███    ███   ███    ███   ███ ▄███▀:
                                   :███     ███   ███    █▀    ███    █▀    ███▐██▀  :
                                   :███     ███  ▄███▄▄▄      ▄███▄▄▄      ▄█████▀   :
                                   :███     ███ ▀▀███▀▀▀     ▀▀███▀▀▀     ▀▀█████▄   :
                                   :███     ███   ███    █▄    ███    █▄    ███▐██▄  :
                                   :███ ▄█▄ ███   ███    ███   ███    ███   ███ ▀███▄:
                                   : ▀███▀███▀    ██████████   ██████████   ███   ▀█▀:
                                   :                                        ▀        :
                                   ···················································
                                                    ·····················
                                                    : ████  █████ █████ :
                                                    :░░███ ░░███ ░░███  :
                                                    : ░███  ░███  ░███ █:
                                                    : ░███  ░███████████:
                                                    : ░███  ░░░░░░░███░█:
                                                    : ░███        ░███░ :
                                                    : █████       █████ :
                                                    :░░░░░       ░░░░░  :
                                                    ·····················    

        """)
    user = input("To start click (return) ").upper()
    clear_screen()
    print("Manchester City vs Barcelona")
    season.match_winner(Manchester_City, Barcelona_FC)
    season.update_table(Manchester_City, Barcelona_FC)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Newcastle vs Arsenal")
    season.match_winner(Newcastle, Arsenal)
    season.update_table(Newcastle, Arsenal)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Napoli vs Real Madrid")
    season.match_winner(Napoli, Real_Madrid)
    season.update_table(Napoli, Real_Madrid)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Dortmund vs Liverpool")
    season.match_winner(Dortmund, Liverpool_FC)
    season.update_table(Dortmund, Liverpool_FC)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match PSG vs Bayern Munich")
    season.match_winner(PSG, Bayern_Munich)
    season.update_table(PSG, Bayern_Munich)
    season.display_initial_table()
    user = input("To see go to week 15 click (return) ").upper()

    print("""

                                       ···················································
                                       : ▄█     █▄     ▄████████    ▄████████    ▄█   ▄█▄:
                                       :███     ███   ███    ███   ███    ███   ███ ▄███▀:
                                       :███     ███   ███    █▀    ███    █▀    ███▐██▀  :
                                       :███     ███  ▄███▄▄▄      ▄███▄▄▄      ▄█████▀   :
                                       :███     ███ ▀▀███▀▀▀     ▀▀███▀▀▀     ▀▀█████▄   :
                                       :███     ███   ███    █▄    ███    █▄    ███▐██▄  :
                                       :███ ▄█▄ ███   ███    ███   ███    ███   ███ ▀███▄:
                                       : ▀███▀███▀    ██████████   ██████████   ███   ▀█▀:
                                       :                                        ▀        :
                                       ···················································
                                                         ···················
                                                         : ████  ██████████:
                                                         :░░███ ░███░░░░░░█:
                                                         : ░███ ░███     ░ :
                                                         : ░███ ░█████████ :
                                                         : ░███ ░░░░░░░░███:
                                                         : ░███  ███   ░███:
                                                         : █████░░████████ :
                                                         :░░░░░  ░░░░░░░░  :
                                                         ···················

            """)
    user = input("To start click (return) ").upper()
    clear_screen()
    print("Manchester City vs Arsenal")
    season.match_winner(Manchester_City, Arsenal)
    season.update_table(Manchester_City, Arsenal)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Barcelona vs Real Madrid")
    season.match_winner(Barcelona_FC, Real_Madrid)
    season.update_table(Barcelona_FC, Real_Madrid)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Newcastle vs Liverpool")
    season.match_winner(Newcastle, Liverpool_FC)
    season.update_table(Newcastle, Liverpool_FC)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Napoli vs Bayern Munich")
    season.match_winner(Napoli, Bayern_Munich)
    season.update_table(Napoli, Bayern_Munich)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Dortmund vs PSG")
    season.match_winner(Dortmund, PSG)
    season.update_table(Dortmund, PSG)
    season.display_initial_table()
    user = input("To see go to week 16 click (return) ").upper()

    print("""

                                       ···················································
                                       : ▄█     █▄     ▄████████    ▄████████    ▄█   ▄█▄:
                                       :███     ███   ███    ███   ███    ███   ███ ▄███▀:
                                       :███     ███   ███    █▀    ███    █▀    ███▐██▀  :
                                       :███     ███  ▄███▄▄▄      ▄███▄▄▄      ▄█████▀   :
                                       :███     ███ ▀▀███▀▀▀     ▀▀███▀▀▀     ▀▀█████▄   :
                                       :███     ███   ███    █▄    ███    █▄    ███▐██▄  :
                                       :███ ▄█▄ ███   ███    ███   ███    ███   ███ ▀███▄:
                                       : ▀███▀███▀    ██████████   ██████████   ███   ▀█▀:
                                       :                                        ▀        :
                                       ···················································
                                                        ···················
                                                        : ████   ████████ :
                                                        :░░███  ███░░░░███:
                                                        : ░███ ░███   ░░░ :
                                                        : ░███ ░█████████ :
                                                        : ░███ ░███░░░░███:
                                                        : ░███ ░███   ░███:
                                                        : █████░░████████ :
                                                        :░░░░░  ░░░░░░░░  :
                                                        ···················

            """)
    user = input("To start click (return) ").upper()
    clear_screen()
    print("Manchester City vs Real Madrid")
    season.match_winner(Manchester_City, Real_Madrid)
    season.update_table(Manchester_City, Real_Madrid)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Arsenal vs Liverpool")
    season.match_winner(Arsenal, Liverpool_FC)
    season.update_table(Arsenal, Liverpool_FC)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Barcelona vs Bayern Munich")
    season.match_winner(Barcelona_FC, Bayern_Munich)
    season.update_table(Barcelona_FC, Bayern_Munich)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Newcastle vs PSG")
    season.match_winner(Newcastle, PSG)
    season.update_table(Newcastle, PSG)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Napoli vs Dortmund")
    season.match_winner(Napoli, Dortmund)
    season.update_table(Napoli, Dortmund)
    season.display_initial_table()
    user = input("To see go to week 17 click (return) ").upper()

    print("""

                                           ···················································
                                           : ▄█     █▄     ▄████████    ▄████████    ▄█   ▄█▄:
                                           :███     ███   ███    ███   ███    ███   ███ ▄███▀:
                                           :███     ███   ███    █▀    ███    █▀    ███▐██▀  :
                                           :███     ███  ▄███▄▄▄      ▄███▄▄▄      ▄█████▀   :
                                           :███     ███ ▀▀███▀▀▀     ▀▀███▀▀▀     ▀▀█████▄   :
                                           :███     ███   ███    █▄    ███    █▄    ███▐██▄  :
                                           :███ ▄█▄ ███   ███    ███   ███    ███   ███ ▀███▄:
                                           : ▀███▀███▀    ██████████   ██████████   ███   ▀█▀:
                                           :                                        ▀        :
                                           ···················································
                                                           ···················
                                                           : ████  ██████████:
                                                           :░░███ ░███░░░░███:
                                                           : ░███ ░░░    ███ :
                                                           : ░███       ███  :
                                                           : ░███      ███   :
                                                           : ░███     ███    :
                                                           : █████   ███     :
                                                           :░░░░░   ░░░      :
                                                           ···················

                """)
    user = input("To start click (return) ").upper()
    clear_screen()
    print("Manchester City vs Liverpool")
    season.match_winner(Manchester_City, Liverpool_FC)
    season.update_table(Manchester_City, Liverpool_FC)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Real Madrid vs Bayern Munich")
    season.match_winner(Real_Madrid, Bayern_Munich)
    season.update_table(Real_Madrid, Bayern_Munich)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Arsenal vs PSG")
    season.match_winner(Arsenal, PSG)
    season.update_table(Arsenal, PSG)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Barcelona vs Dortmund")
    season.match_winner(Barcelona_FC, Dortmund)
    season.update_table(Barcelona_FC, Dortmund)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Newcastle vs Napoli")
    season.match_winner(Newcastle, Napoli)
    season.update_table(Newcastle, Napoli)
    season.display_initial_table()
    user = input("To see go to week 18 click (return) ").upper()

    print("""

                                               ···················································
                                               : ▄█     █▄     ▄████████    ▄████████    ▄█   ▄█▄:
                                               :███     ███   ███    ███   ███    ███   ███ ▄███▀:
                                               :███     ███   ███    █▀    ███    █▀    ███▐██▀  :
                                               :███     ███  ▄███▄▄▄      ▄███▄▄▄      ▄█████▀   :
                                               :███     ███ ▀▀███▀▀▀     ▀▀███▀▀▀     ▀▀█████▄   :
                                               :███     ███   ███    █▄    ███    █▄    ███▐██▄  :
                                               :███ ▄█▄ ███   ███    ███   ███    ███   ███ ▀███▄:
                                               : ▀███▀███▀    ██████████   ██████████   ███   ▀█▀:
                                               :                                        ▀        :
                                               ···················································
                                                              ···················
                                                              : ████   ████████ :
                                                              :░░███  ███░░░░███:
                                                              : ░███ ░███   ░███:
                                                              : ░███ ░░████████ :
                                                              : ░███  ███░░░░███:
                                                              : ░███ ░███   ░███:
                                                              : █████░░████████ :
                                                              :░░░░░  ░░░░░░░░  :
                                                              ···················
                    """)
    user = input("To start click (return) ").upper()
    clear_screen()
    print("Manchester City vs Bayern Munich")
    season.match_winner(Manchester_City, Bayern_Munich)
    season.update_table(Manchester_City, Bayern_Munich)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Liverpool vs PSG")
    season.match_winner(Liverpool_FC, PSG)
    season.update_table(Liverpool_FC, PSG)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Real Madrid vs Dortmund")
    season.match_winner(Real_Madrid, Dortmund)
    season.update_table(Real_Madrid, Dortmund)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Arsenal vs Napoli")
    season.match_winner(Arsenal, Napoli)
    season.update_table(Arsenal, Napoli)
    season.display_initial_table()
    user = input("To see other Games click (return) ").upper()

    clear_screen()
    print("Next Match Barcelona vs Newcastle")
    season.match_winner(Barcelona_FC, Newcastle)
    season.update_table(Barcelona_FC, Newcastle)
    season.display_initial_table()
main()
# Help Document
# The function normalvariate generates a random possible goal value that makes up the average.
#  Using a random range of standard deviation values that go from low to high.
# Standard deviation is the spread of the values from the mean
# So a higher standard deviation will mean some of your possible goals will be further from the teams predicted goals per game(PGPG)
# But this is essential cause most often than not teams don't always score or win the predicted games
# They either don't score the predicted goals or don't win the predicted games
