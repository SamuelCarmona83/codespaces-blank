from dataclasses import dataclass
from enum import Enum
from typing import List
import random

class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    @staticmethod
    def colorize(text: str, color: str) -> str:
        return f"{color}{text}{Colors.RESET}"

class Suit(Enum):
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"
    SPADES = "♠"

    @property
    def is_red(self) -> bool:
        return self in (Suit.HEARTS, Suit.DIAMONDS)

@dataclass
class Card:
    rank: str
    suit: Suit

    @property
    def value(self) -> int:
        if self.rank == 'A':
            return 11
        return 10 if self.rank in ('J', 'Q', 'K') else int(self.rank)

    def __str__(self) -> str:
        color = Colors.RED if self.suit.is_red else Colors.BLUE
        return Colors.colorize(f"{self.rank}{self.suit.value}", color)

class Deck:
    RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    def __init__(self, num_decks: int = 4):
        self.cards = [
            Card(rank, suit)
            for _ in range(num_decks)
            for suit in Suit
            for rank in self.RANKS
        ]
        random.shuffle(self.cards)

    def draw(self) -> Card:
        return self.cards.pop()

class Hand:
    def __init__(self):
        self.cards: List[Card] = []

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    @property
    def total(self) -> int:
        total = sum(card.value for card in self.cards)
        num_aces = sum(1 for card in self.cards if card.rank == 'A')
        
        while total > 21 and num_aces:
            total -= 10
            num_aces -= 1
        
        return total

    def __str__(self) -> str:
        return " ".join(str(card) for card in self.cards)

class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()

    def initial_deal(self) -> None:
        for _ in range(2):
            self.player_hand.add_card(self.deck.draw())
            self.dealer_hand.add_card(self.deck.draw())

    def show_hands(self, hide_dealer: bool = True) -> None:
        # Player's hand display
        player_total = Colors.colorize(str(self.player_hand.total), Colors.GREEN)
        print(f"\n{Colors.BOLD}Your hand ({player_total}): {self.player_hand}{Colors.RESET}")
        
        # Dealer's hand display
        if hide_dealer:
            print(f"{Colors.BOLD}Dealer shows: {Colors.PURPLE}?? {self.dealer_hand.cards[1]}{Colors.RESET}")
        else:
            dealer_total = Colors.colorize(str(self.dealer_hand.total), Colors.RED)
            print(f"{Colors.BOLD}Dealer hand ({dealer_total}): {self.dealer_hand}{Colors.RESET}")

    def play_dealer_hand(self) -> None:
        while self.dealer_hand.total < 17:
            self.dealer_hand.add_card(self.deck.draw())

    def check_winner(self) -> str:
        player_total = self.player_hand.total
        dealer_total = self.dealer_hand.total

        if player_total > 21:
            return Colors.colorize("Bust! Dealer wins.", Colors.RED)
        if dealer_total > 21:
            return Colors.colorize("Dealer busts! You win!", Colors.GREEN)
        if player_total > dealer_total:
            return Colors.colorize(f"You win with {player_total}!", Colors.GREEN)
        if dealer_total > player_total:
            return Colors.colorize(f"Dealer wins with {dealer_total}!", Colors.RED)
        return Colors.colorize("Push! It's a tie.", Colors.YELLOW)

    def play(self) -> None:
        title = Colors.colorize("Welcome to Blackjack!", Colors.CYAN)
        print(f"\n{Colors.BOLD}{title}{Colors.RESET}")
        
        self.initial_deal()
        self.show_hands()

        # Check for natural blackjack
        if self.dealer_hand.total == 21 or self.player_hand.total == 21:
            self.show_hands(hide_dealer=False)
            winner = "Blackjack!" if self.player_hand.total == 21 else "Dealer Blackjack!"
            color = Colors.GREEN if self.player_hand.total == 21 else Colors.RED
            print(Colors.colorize(winner, color))
            return

        # Player's turn
        while self.player_hand.total < 21:
            prompt = Colors.colorize("\nHit (h) or Stand (s)? ", Colors.YELLOW)
            action = input(prompt).lower()
            if action not in ['h', 's']:
                print(Colors.colorize("Invalid input! Please enter 'h' or 's'", Colors.RED))
                continue

            if action == 'h':
                self.player_hand.add_card(self.deck.draw())
                self.show_hands()
            else:
                break

        # Dealer's turn
        if self.player_hand.total <= 21:
            self.play_dealer_hand()
        
        # Show final hands and winner
        self.show_hands(hide_dealer=False)
        print("\n" + self.check_winner())

if __name__ == "__main__":
    game = BlackjackGame()
    game.play()