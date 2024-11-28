from abc import ABC, abstractmethod
from rich.console import Console
from time import sleep


console = Console()

class Notebook:
    def __init__(self):
        self.logs = []
        self.clues = []
        self.statements = []

    def itemsLog(self, message: str):
        self.logs.append(message)

    def add_clue(self, clue):
        self.clues.append(clue)

    def statementLog(self, statement):
        self.statements.append(statement)

    def print_log(self):
        console.print("[bold italic white]----Items----[/]")
        for item in self.logs:
            print(item)
        console.print("[bold italic white]----Clues----[/]")
        for clue in self.clues:
            print(f"- {clue}")
        console.print("[bold italic white]----Statements----[/]")
        for statement in self.statements:
            print(statement)

    def clues_count(self):
        """ Returns the number of clues collected """
        return len(self.clues)

class Character(ABC):
    def __init__(self, name, dialogue):
        self.name = name
        self.dialogue = dialogue
        self.interacted = False

    def interact(self):
        if not self.interacted:
            interaction = f"{self.name}: {self.dialogue}"
            self.interacted = True
        else:
            interaction = f"{self.name} is no longer interested in talking."
        return interaction

class Suspect(Character):
    def __init__(self, name, dialogue, alibi):
        super().__init__(name, dialogue)
        self.alibi = alibi

    def __repr__(self):
        return f"Suspect('{self.name}', '{self.dialogue}', '{self.alibi}')"

    def provide_alibi(self):
        return f"{self.name}'s Alibi: {self.alibi}"

    def perform_action(self):
        return (f"Suspect {self.name} nervously shifts and avoids eye contact.")

class Witness(Character):
    def __init__(self, name, dialogue, observation):
        super().__init__(name, dialogue)
        self.observation = observation

    def share_observation(self):
        print(f"{self.name}'s Observation: {self.observation}")

    def perform_action(self):
        print(f"Witness {self.name} speaks hurriedly and glances around anxiously.")


class Game:
    def __init__(self):
        # Flags to check locked doors
        self.kitchen_access = False
        self.engine_room_access = False

        # Clues held here
        self.playerNotebook = Notebook()

        # Current player location
        self.location = 0

        # Characters
        self.wife = Witness("Owner's Wife",
                            "Hi, thank God you’re here. My husband is missing, and I’m really worried about him. "
                            "The last time I saw him was at the party last night just before the power on board went out. "
                            "I think he was talking with one of the servers. It was pitch black and everyone onboard started to panic. "
                            "We all lost track of each other, and no one has seen him since.",
                            "Husband missing after party blackout.")

        self.chef = Suspect("Chef",
                            "The last time I saw him was early last night before the meal. He seemed to be arguing with his business partner "
                            "over some sort of deal. From what I gather his business partner has been stealing money from the company, and he intends "
                            "to fire him if he does not return the money.",
                            "Saw the owner arguing with business partner.")

        self.captain = Suspect("Captain",
                               "I went to my quarters early in the night before the blackout as I needed to rest for a long day of sailing the next day. "
                               "I didn’t hear or see anything during the night as I was asleep.",
                               "Asleep during the blackout.")

        self.watchman = Witness("Watchman",
                                 "When the power went out, I headed to the captain’s room to see if he could help us figure out how to get the power back on, "
                                 "but he wasn’t there. Maybe he was with the other guests.",
                                 "Captain missing during blackout.")

        self.server = Witness("Server",
                              "I was talking to him right before the blackout. He was shouting at me because he thought the food was terrible. I told him I had "
                              "nothing to do with the food and that he should go to the kitchen to speak with the chef. I swear he is the most horrible and rude man I’ve ever met.",
                              "owner complained about food, went to confront the chef.")

        self.business_partner = Witness("Business Partner",
                                        "I was talking with him last night at the meal. Everything had seemed fine. I’m not sure what could have happened to him.",
                                        "Had a calm conversation with the owner during the meal.")

    def display_main_foyer(self):
        """ Tells player they are in main foyer, main area for movement and checking clues """
        if self.location == 0:
            # Player started game so they have no clues
            print("You are currently standing in the main foyer")
            print("Where would you like to go!\n")
            print("-----------\n"
                  "1. Kitchen\n"
                  "2. Engine Room\n"
                  "3. Captain's Deck\n"
                  "4. Owner's Bedroom\n"
                  "5. Captain's Quarters\n"
                  "6. Security Room\n")
        else:
            # Player is back in main foyer, they can check clues and text has changed
            print("You are back in the main foyer")

            check_clue_list = input("open notebook (y/n): ").upper()
            if check_clue_list == 'Y':
                self.playerNotebook.print_log()
            else:
                print("Where would you like to go!\n")
                print("-----------\n"
                      "1. Kitchen\n"
                      "2. Engine Room\n"
                      "3. Captain's Deck\n"
                      "4. Owner's Bedroom\n"
                      "5. Captain's Quarters\n"
                      "6. Security Room\n")

    def interact(self):
        """ Prompts player with interactive elements, either search or go back """

        task = input("'s' to search | 'i' to interact | 'b' to go back to foyer\n").upper()
        if task == 'S':
            self.search_location()
        elif task == 'I':
            self.talk_to_npc()
        elif task == 'B':
            # Brings player back to main foyer
            self.display_main_foyer()

    def search_location(self):
        """ Handles searching within a specific location """
        if self.location == 1:  # Kitchen
            self.search_kitchen()
        elif self.location == 2:  # Engine Room
            self.search_engine_room()
        elif self.location == 3:  # Captain's Deck
            self.search_captains_deck()
        elif self.location == 4:  # Owner's Bedroom
            self.search_owners_bedroom()
        elif self.location == 5:  # Captain's Quarters
            self.search_captains_quarters()
        elif self.location == 6:  # Security Room
            self.search_security_room()

    def talk_to_npc(self): # Talks with NPC's based on their location
        if self.location == 1:  # Kitchen
            print(self.server.interact())
            self.server.share_observation()
            self.playerNotebook.statementLog(self.server.observation)

            print(self.chef.interact())
            self.chef.provide_alibi()
            self.playerNotebook.statementLog(self.chef.alibi)

        elif self.location == 2:  # Engine Room
            print(self.business_partner.interact())
            self.business_partner.share_observation()
            self.playerNotebook.statementLog(self.business_partner.observation)

        elif self.location == 4:  # Owner's Bedroom
            print(self.wife.interact())
            self.wife.share_observation()
            self.playerNotebook.statementLog(self.wife.observation)

        elif self.location == 5:  # Captain's Quarters
            print(self.captain.interact())
            self.captain.provide_alibi()
            self.playerNotebook.statementLog(self.captain.alibi)

        elif self.location == 6:  # Security Room
            print(self.watchman.interact())
            self.watchman.share_observation()
            self.playerNotebook.statementLog(self.watchman.observation)

    def search_kitchen(self):
        while True:
            print("\nWhere in the kitchen would you like to look? (Press 0 to return)")
            print("1. Cooking area\n2. Freezer\n3. Washing-up area\n")
            choice = int(input("-> "))

            if choice == 1:
                print("You found a bloody knife!\nWhat could this mean?")
                print("Clue added!")
                self.playerNotebook.add_clue("A bloody knife")
                sleep(3)
            elif choice == 2:
                print("Nothing to be found here")
                sleep(3)
            elif choice == 3:
                print("You found blood splatters")
                print("Clue added!")
                self.playerNotebook.add_clue("Blood Splatter")
                sleep(3)
            elif choice == 0:
                break

    def search_engine_room(self):
        while True:
            print("\nWhere would you like to look in the Engine Room? (Press 0 to return)\n"
                  "1. Behind the Engines\n2. Under the stairs\n")
            choice = int(input("-> "))
            if choice == 1:
                print("You found the owner's dead body!\nTHIS IS NOW A MURDER CASE!!!!")
                print("Clue added!")
                self.playerNotebook.add_clue("Owners Body")
                sleep(3)
            elif choice == 2:
                print("There is nothing here....")
                sleep(3)
            elif choice == 0:
                break

    def search_captains_deck(self):
        while True:
            print("\nWhere in the Captain's Deck would you like to look? (Press 0 to return)\n"
                  "1. Filing Cabinet\n2. Captain's Seat\n")
            choice = int(input("-> "))
            if choice == 1:
                print("You find a neat and organized set of files, the top piece of paper has blood on it!!")
                print("Clue added!")
                self.playerNotebook.add_clue("A bloody piece of paper from the Captain's desk")
                sleep(3)
            elif choice == 2:
                print("You find nothing around the seat, everything is remarkably clean")
                sleep(3)
            elif choice == 0:
                break

    def search_owners_bedroom(self):
        while True:
            print("\nWhere in the Owner's Bedroom would you like to look? (Press 0 to return)\n"
                  "1. Under the Bed\n2. Owner's Wardrobe\n")
            choice = int(input("-> "))
            if choice == 1:
                print("You find a pair of shoes under the bed, everything is remarkably clean")
                sleep(3)
            elif choice == 2:
                print("You find a neat and organized set of clothes. Everything is clean and tidy")
                sleep(3)
            elif choice == 0:
                break
                

    def search_captains_quarters(self):
        while True:
            print("\nWhere in the Captain's Quarters would you like to look? (Press 0 to return)\n"
                  "1. Bedside Table\n2. Wardrobe\n3. Captain's Bed\n")
            choice = int(input("-> "))
            if choice == 1:
                print("You found a combination code! I wonder where it's for?")
                print("Item added!")
                self.playerNotebook.itemsLog("Combination code")
                self.engine_room_access = True
                sleep(3)
            elif choice == 2:
                print("You found a bloody shirt! Is someone trying to frame the captain?")
                print("Clue added!")
                self.playerNotebook.add_clue("A bloody shirt")
                sleep(3)
            elif choice == 3:
                print("Nothing to see here...")
                sleep(3)
            elif choice == 0:
                break

    def search_security_room(self):
        while True:
            print("\nWhere in the Security Room would you like to look? (Press 0 to return)\n"
                  "1. Desk\n2. Safe\n")
            choice = int(input("-> "))
            if choice == 1:
                print("You found a key! What door is it for?")
                print("Item added!")
                self.playerNotebook.itemsLog("Door key")
                self.kitchen_access = True
                sleep(3)
            elif choice == 2:
                print("Its empty, nothing to see here ...")
                sleep(3)
            elif choice == 0:
                break
    
    def play(self):
        """ Main game loop """

        print("You have been summoned to a superyacht off the coast of Monaco.\n" 
              "You have been told about a power cut on board and that supposedly\nthe owner of this superyacht has gone missing.\n" 
              "\nIt is your job to investigate what has happened to the owner and if there is a case, solve it.\n")
        
        print("""                __________________________
                |  [9:41 AM]              | 
                |  LTE         100%       | 
                |-------------------------| 
                |                         | 
                | Them:                   | 
                | We need your help.      | 
                | ◀----------------       | 
                |                         | 
                |-------------------------| 
                |                         | 
                |                   OK    | 
                |       ----------------▶ | 
                |                         | 
                |-------------------------| 
                |                         | 
                |   [      Reply      ]   | 
                |_________________________| 
                """)


        detective_name = input("Detective Name -> ")
        while True:
            self.display_main_foyer()
            self.location = int(input("\nEnter location (1 = Kitchen etc.): "))
            if self.location == 1 and not self.kitchen_access:
                print("It seems this door is locked. You must find the key.")
            elif self.location == 2 and not self.engine_room_access:
                print("It seems this door is locked. It looks like a combination lock!")
            else:
                self.interact()

            # Check if the clues list has 5 items
            if self.playerNotebook.clues_count() == 5:
                print("You have collected the clues!")
                print("Time to catch the killer\n"
                      "1. Owners Wife\n"
                      "2. Captain of yacht\n"
                      "3. Buisness Partner\n"
                      "4. Chef\n")
                killer_guess = int(input("Enter guess here -> "))

                if killer_guess == 2:
                    print("Well done!!\nYou have solidified yourself as a great detective")
                    sleep(4)
                    print(f"""
                            +------------------------------------------------------------+
                            |                      *** DON's NEWSPAPER ***               |
                            |                       "Your Trusted News"                  |
                            +------------------------------------------------------------+
                            |                                                            |
                            |                   ** MURDER MYSTERY SOLVED **              |
                            |                        by {detective_name}                 |
                            +------------------------------------------------------------+
                            |                          OTHER NEWS                        |
                            |  -------------------------------------------------------   |
                            |  * WEATHER: Heavy rain and strong winds expected today.    |
                            |  * SPORTS: Lakers dominate with another stunning victory.  |
                            |  * TECH: New smartphone breaks records for pre-orders.     |
                            +------------------------------------------------------------+
                            """)
                    print("THE END!")
                    break  # Exit the game loop
                else:
                    print("You guessed wrong, the killer got away!")
                    play_again = input("Do you want to play again (y/n)? ").upper()

                    if play_again == 'Y':
                        game = Game()
                        game.play()
                    else:
                        break

# Start the game
game = Game()
game.play()