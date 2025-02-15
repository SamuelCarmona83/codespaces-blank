import random

# ANSI escape sequences for colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

class Card:

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    @classmethod
    def random_card(cls):
        ranks = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J','Q', 'K']
        suits = ['♣','♦', '♥', '♠']

        random_rank = random.choice(ranks)
        random_suit = random.choice(suits)

        return cls(value=random_rank, suit=random_suit)

    def __repr__(self):
        color_value = RED if self.suit in ["♦", "♥"] else BLUE
        return f"<Card {self.value} of {color_value}{self.suit}{RESET}>"
        
class Deck:

    def __init__(self, card_amount=52):
        self.cards = []
        for _ in range(card_amount):
            new_card = Card.random_card()
            self.cards.append(new_card)
    
    def __repr__(self):
        return f"<Deck {len(self.cards)}>"

    def pick_card(self):
        card_dealed = self.cards.pop()
        return card_dealed

class Hand:

    def __init__(self):
        self.cards = []

    def show_hand(self):
        print(self.cards)
    
    def get_total(self):
        total = 0

        for card in self.cards:
            if card.value == 'A':
                total = total + 11
            elif card.value in ['J', 'Q', 'K']:
                total = total + 10
            else:
                total = total + card.value

        aces_amount = self.get_aces_amount()

        if aces_amount > 0:
            for ace in range(aces_amount):
                if total > 21:
                    total = total - 10
        
        return total

    def get_aces_amount(self) -> int:
        """Returns the amount of aces ins a hand"""
        aces_amount = 0
        for card in self.cards:
            if card.value == 'A':
                aces_amount += 1
        return aces_amount


class Dealer:

    def __init__(self):
        self.hand = Hand()
        self.deck = Deck(208)

    def deal(self) -> Card:
        return self.deck.pick_card()

    def pick_card(self):
        self.hand.cards.append(self.deal())
        


class Player:

    def __init__(self, name):
        self.name = name
        self.hand = Hand()

    def receive_card(self, card):
        self.hand.cards.append(card)

    def hit(self, card):
        self.hand.cards.append(card)

    def stays():
        pass

class Blackjack:
    
    def __init__(self):

        game_over = False
        winner = None

        player = Player('lucho')
        dealer = Dealer()

        player.receive_card(dealer.deal())
        player.receive_card(dealer.deal())

        def show_hands():
            print(f"Here's your {GREEN} Hand:{RESET}")
            print(player.hand.cards, f"total player: {YELLOW}{player.hand.get_total()}{RESET}\n")
            print(dealer.hand.cards, f"total dealer hand: {RED}{dealer.hand.get_total()}{RESET}\n")

        print(f"Welcome {GREEN}{player.name}{RESET} to {RED}Blackjack!{RESET}\n")
        print(f"Here's your {GREEN} Hand:{RESET}")
        print(player.hand.cards, f"total player: {YELLOW}{player.hand.get_total()}{RESET}\n")

        dealer.pick_card()
        dealer.pick_card()

        print(dealer.hand.cards, f"total dealer hand: {RED}{dealer.hand.get_total()}{RESET}\n")
        
        
        if dealer.hand.get_total() == 21:
            game_over = True
            print(f"{RED} House always win!{RESET}")
        
        if player.hand.get_total() == 21:
            game_over = True
            print(f"{GREEN}You lucky bastard, you win!{RESET}")

        def check_gameover():
            player_amount = player.hand.get_total()
            dealer_amount = dealer.hand.get_total()

            if player_amount > 21:
                print("Perdiste bobo!")
                game_over = True
                return True

            if player_amount <= 21 and player_amount > dealer_amount:

                print("Coño Ganaste")
                game_over = True
                return True

            if player_amount == dealer_amount:
                if len(player.hand.cards) < len(dealer.hand.cards):
                    print("Coño Ganaste")
                else:
                    print("Perdiste")
                return True

            game_over = False
            return False


        while not game_over:

            print("What do you want to do next:")
            response = input(f"Press (h) key to {RED}Hit{RESET} or (s) to {YELLOW}Stay:{RESET}")
            response = response.lower()

            print("response: ", response)

            if response not in ['h', 's']:
                print("Your only options are (h) and (s) keys")
                continue

            if response == 'h':
                player.hit(dealer.deal())
                print(f"{RESET}New player hand: {player.hand.cards}")

                if not check_gameover():
                    continue
            
            if response =='s':
                check_gameover()
                game_over = True 
                
            check_gameover()
            show_hands()
        

game = Blackjack()