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
        
    def play_hand(self):
        """Dealer must hit on 16 and stand on 17"""
        while self.hand.get_total() < 17:
            self.pick_card()

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
        self.game_over = False
        self.player = Player('lucho')
        self.dealer = Dealer()
        self.play_game()

    def show_hands(self, hide_dealer_first_card=False):
        print(f"\nHere's your {GREEN}Hand:{RESET}")
        print(self.player.hand.cards, f"total player: {YELLOW}{self.player.hand.get_total()}{RESET}")
        
        print(f"\nDealer's Hand:")
        if hide_dealer_first_card:
            hidden_hand = ['<Hidden>'] + self.dealer.hand.cards[1:]
            print(hidden_hand, f"total shown: {RED}{self.dealer.hand.cards[1].value if isinstance(self.dealer.hand.cards[1].value, int) else 10}{RESET}")
        else:
            print(self.dealer.hand.cards, f"total dealer: {RED}{self.dealer.hand.get_total()}{RESET}")

    def check_winner(self):
        player_total = self.player.hand.get_total()
        dealer_total = self.dealer.hand.get_total()

        if player_total > 21:
            print(f"{RED}Bust! You went over 21. House wins!{RESET}")
            return True
            
        if dealer_total > 21:
            print(f"{GREEN}Dealer busts! You win!{RESET}")
            return True
            
        if player_total > dealer_total:
            print(f"{GREEN}You win with {player_total} against dealer's {dealer_total}!{RESET}")
            return True
            
        elif dealer_total > player_total:
            print(f"{RED}Dealer wins with {dealer_total} against your {player_total}!{RESET}")
            return True
            
        else:  # Equal totals
            if len(self.player.hand.cards) < len(self.dealer.hand.cards):
                print(f"{GREEN}Push with {player_total}, but you win with fewer cards!{RESET}")
            elif len(self.player.hand.cards) > len(self.dealer.hand.cards):
                print(f"{RED}Push with {player_total}, but dealer wins with fewer cards!{RESET}")
            else:
                print(f"{YELLOW}Push! It's a tie with {player_total}!{RESET}")
            return True

    def play_game(self):
        # Initial deal
        print(f"Welcome {GREEN}{self.player.name}{RESET} to {RED}Blackjack!{RESET}\n")
        
        self.player.receive_card(self.dealer.deal())
        self.dealer.pick_card()
        self.player.receive_card(self.dealer.deal())
        self.dealer.pick_card()
        
        # Show initial hands (hiding dealer's first card)
        self.show_hands(hide_dealer_first_card=True)

        # Check for natural blackjack
        if self.dealer.hand.get_total() == 21:
            self.show_hands(hide_dealer_first_card=False)
            print(f"{RED}Dealer has Blackjack! House wins!{RESET}")
            return
            
        if self.player.hand.get_total() == 21:
            self.show_hands(hide_dealer_first_card=False)
            print(f"{GREEN}Blackjack! You win!{RESET}")
            return

        # Player's turn
        while not self.game_over:
            response = input(f"\nWhat do you want to do next:\nPress (h) to {RED}Hit{RESET} or (s) to {YELLOW}Stay:{RESET} ").lower()

            if response not in ['h', 's']:
                print("Your only options are (h) and (s) keys")
                continue

            if response == 'h':
                self.player.hit(self.dealer.deal())
                self.show_hands(hide_dealer_first_card=True)
                
                if self.player.hand.get_total() > 21:
                    self.show_hands(hide_dealer_first_card=False)
                    print(f"{RED}Bust! You went over 21. House wins!{RESET}")
                    self.game_over = True
                    break
            
            if response == 's':
                # Dealer's turn
                self.dealer.play_hand()
                self.show_hands(hide_dealer_first_card=False)
                self.check_winner()
                self.game_over = True

if __name__ == "__main__":
    game = Blackjack()