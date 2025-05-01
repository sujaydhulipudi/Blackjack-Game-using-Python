import random

suits =("Hearts","Diamonds","Spades","Clubs")
ranks =("Two","Three","Four","Five","Six","Seven","Eight","Nine","Ten","Jack","Queen","King","Ace")
values={"Two":2,"Three":3,"Four":4,"Five":5,"Six":6,"Seven":7,"Eight":8,"Nine":9,"Ten":10,"Jack":10,"Queen":10,"King":10,"Ace":1}

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        self.all_cards=[]
        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal(self):
        return self.all_cards.pop()
    def reset_deck(self):
        self.__init__()

class Player:
    def __init__(self,bet,balance):
        self.original_balance=balance

        self.player_cards=[]
        self.bet=bet
        self.balance=balance

    @property
    def total(self):
        total = sum(card.value for card in self.player_cards)
        aces = sum(1 for card in self.player_cards if card.rank == 'Ace')

        # Try to upgrade Aces from 1 to 11 without busting
        while aces > 0 and total + 10 <= 21:
            total += 10
            aces -= 1

        return total

    def remove_card(self):
        return self.player_cards.pop(0)

    def add_card(self,new_card):
        if type(new_card)==type([]):
            self.player_cards.extend(new_card)
        else:
            self.player_cards.append(new_card)

    def reset(self):
        self.player_cards.clear()

    def __str__(self):
        return ',\n '.join(str(card) for card in self.player_cards)


bal=int(input("How much would you like to deposit? "))

user=Player(0,bal)
dealer=Player(0,int(bal*1.5))
new_deck=Deck()
new_deck.shuffle()

game_on=True
while game_on:
    new_deck.reset_deck()
    new_deck.shuffle()
    user.reset()
    dealer.reset()

    print(f"Your balance is {user.balance}")

    while True:
        x = int(input("How much would you like to bet? "))
        if x <=user.balance:
            user.bet=x
            dealer.bet=x
            break
        else:
            print("You don't have enough money, decrease the bet")


    for i in range(2):
        dealer.add_card(new_deck.deal())
        user.add_card(new_deck.deal())

    while True:
        if user.total==21:
            print(f"Your total is {user.total}. You win!")
            user.balance += dealer.bet
            dealer.balance -= dealer.bet
            break

        elif dealer.total==21:
            print(f"Dealer total is {dealer.total}. You lose!")
            dealer.balance += user.bet
            user.balance -= user.bet
            break

        elif user.total<22:
            print(f"Dealer's cards:\n Hidden Card,\n {dealer.player_cards[-1]}")
            print("Player's cards:\n", user)
            print(f"Your total value: {user.total}")
            choice=input("Do you want to Hit or Stand? (hit or stand): ")
            if choice=="hit":
                print("Hit!!")
                user.add_card(new_deck.deal())
                print(f"New card dealt is {user.player_cards[-1]}")
            elif choice=="stand":
                print("Stand!!")
                while True:
                    print("Dealer cards:\n", dealer)
                    print(f"Dealer total value: {dealer.total}")
                    if 22 > dealer.total > user.total:
                        print("Dealer wins!")
                        dealer.balance+=user.bet
                        user.balance-=user.bet
                        break
                    elif 22 > dealer.total < user.total:
                        dealer.add_card(new_deck.deal())
                    elif 22 > dealer.total==user.total:
                        print("Draw!!")
                        break
                    else:
                        print("Dealer BUST!!\nYou win!")
                        user.balance+=dealer.bet
                        dealer.balance-=dealer.bet
                        break
                break
            else:
                print("Invalid choice! Retry")
        else:
            print(f"Your total card value is {user.total}\n BUST!! You lost!")
            dealer.balance += user.bet
            user.balance -= user.bet
            break

    while True:
        cont=input("Do you want to continue? (yes or no): ")
        if cont=="yes":
            break
        elif cont=="no":
            print(f"Thank you for playing. Your total balance is {user.balance}")
            game_on=False
            break
        else:
            print("Invalid choice! Retry")