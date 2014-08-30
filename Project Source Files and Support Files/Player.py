class Player(object):

    def __init__(self, color, countries = set(), nosArmy = 0, cards = set(),
                 typeOfPlayer = 0):
        #string
        self.color = color
        #set
        self.countries = countries
        #integer
        self.nosArmy = nosArmy
        #set
        self.cards = cards
        #number
        #0 = Human
        #1 = AI
        self.typeOfPlayer = typeOfPlayer

    def __repr__(self):
        return "Player: %r %r %d %d" % (self.color,self.cards,self.nosArmy,
                                        self.typeOfPlayer)
