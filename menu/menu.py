import os
class Menu:
    def __init__(self):
        pass
    def clear_screen(self):
        os.system("clear")

    def _show_menu_and_get_selection(self):
        self.clear_screen()
        menu_text = """
    Welcome to the Football App!
    Here you can view all the stats and facts you could possibly want from the
    best league in the world! (yes, the premier league.)
    Please, select an option below by entering a number:
        [1] Top goalscorers this season
        [2] Show table
        [3] Play the quiz!
        [4] Exit
        """
        print(menu_text)
        while True:
            try:
                return int(input("Enter a number: "))
            except ValueError:
                print("Please enter a valid number.")