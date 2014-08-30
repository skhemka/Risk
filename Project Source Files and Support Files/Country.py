#Country class
class Country(object):

    def __init__(self,coor,continent,neighbours,player,nosArmy,weight=0):
        #string
        self.continent = continent
        #set of strings
        self.neighbours = neighbours
        #tuple
        self.position = coor
        #integer or none
        self.player = player
        #integer
        self.nosArmy = nosArmy
        #integer
        self.weight = 0
        
    def getContinent(self):
        #returns string
        return self.continent

    def getNeighbours(self):
        #returns a set of string
        return self.neighbours

    def getPosition(self):
        #returns list of two tuples
        return self.position

    def getPlayer(self):
        return self.Player

    def getNosArmy(self):
        return self.nosArmy
