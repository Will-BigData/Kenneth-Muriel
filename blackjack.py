import csv
import random

class Card:
    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def value(self):
        if self.rank in ['Jack', 'Queen', 'King']:
            return 10
        elif self.rank == 'Ace':
            return 11  # Ace can be 1 or 11, handled in hand value calculation
        else:
            return int(self.rank)

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in Card.SUITS for rank in Card.RANKS]
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop() if self.cards else None


class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def value(self):
        value = sum(card.value() for card in self.cards)
        # Adjust for Aces
        aces = sum(1 for card in self.cards if card.rank == 'Ace')
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)


class Player:
    def __init__(self, name, money, wins=0, losses=0):
        self.name = name
        self.money = money
        self.wins = wins
        self.losses = losses
        self.hand = Hand()

    def bet(self, amount):
        if amount > self.money:
            raise ValueError("Bet exceeds available money.")
        self.money -= amount
        return amount

    def win(self, bet):
        self.wins += 1
        self.money += bet * 2  # Winning doubles the bet

    def lose(self):
        self.losses += 1

    def __str__(self):
        return f"{self.name} has ${self.money} (Wins: {self.wins}, Losses: {self.losses})"


class BlackjackGame:
    def __init__(self, players):
        self.deck = Deck()
        self.players = players
        self.dealer_hand = Hand()

    def play(self):
        # Display players and let the user choose one
        print("Available players:")
        for index, player in enumerate(self.players):
            print(f"{index + 1}: {player}")

        # Get player selection
        while True:
            try:
                choice = int(input("Select a player by number: ")) - 1
                if 0 <= choice < len(self.players):
                    selected_player = self.players[choice]
                    break
                else:
                    print("Invalid choice. Please select a valid player number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        # Play the round for the selected player
        self.play_round(selected_player)

    def play_round(self, player):
        print(f"\n{player}'s turn")

        # Get bet amount
        while True:
            try:
                bet = int(input(f"You have ${player.money}. Enter your bet amount: "))
                player.bet(bet)
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")
            except Exception as e:
                print(e)

        player.hand = Hand()
        self.dealer_hand = Hand()

        # Deal cards
        for _ in range(2):
            player.hand.add_card(self.deck.deal_card())
            self.dealer_hand.add_card(self.deck.deal_card())

        print(f"Your hand: {player.hand} (value: {player.hand.value()})")
        print(f"Dealer shows: {self.dealer_hand.cards[0]}")

        while True:
            action = input("Do you want to (H)it or (S)tand? ").strip().lower()
            if action not in ('h', 's'):
                print("Invalid input. Please enter 'H' to hit or 'S' to stand.")
                continue

            if action == 'h':
                player.hand.add_card(self.deck.deal_card())
                print(f"Your hand: {player.hand} (value: {player.hand.value()})")
                if player.hand.value() > 21:
                    print("Bust! You lose.")
                    player.lose()
                    return
            else:
                break

        # Dealer's turn
        while self.dealer_hand.value() < 17:
            self.dealer_hand.add_card(self.deck.deal_card())

        print(f"Dealer's hand: {self.dealer_hand} (value: {self.dealer_hand.value()})")

        player_value = player.hand.value()
        dealer_value = self.dealer_hand.value()

        if dealer_value > 21:
            print("Dealer busts! You win!")
            player.win(bet)
        elif player_value > dealer_value:
            print("You win!")
            player.win(bet)
        elif player_value < dealer_value:
            print("You lose.")
            player.lose()
        else:
            print("It's a push (tie). No one wins.")

    @staticmethod
    def load_players(file_path):
        players = []
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                players.append(Player(row['name'], int(row['money']), int(row['wins']), int(row['losses'])))
        return players

    @staticmethod
    def save_players(file_path, players):
        with open(file_path, mode='w', newline='') as csvfile:
            fieldnames = ['name', 'money', 'wins', 'losses']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for player in players:
                writer.writerow({'name': player.name, 'money': player.money, 'wins': player.wins, 'losses': player.losses})


if __name__ == "__main__":
    players = BlackjackGame.load_players('data.csv')
    game = BlackjackGame(players)

    try:
        game.play()
    finally:
        BlackjackGame.save_players('data.csv', players)
