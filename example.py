from enum import Enum
from weblit import Weblit, Select

class Planet(Enum):
	MERCURY = 3.7
	VENUS   = 8.87
	EARTH   = 9.807 
	MARS    = 3.721
	JUPITER = 24.79
	SATURN  = 10.44
	URANUS  = 8.69


wapp = Weblit("Weight On The Planets")

@wapp.Form#(in_format={'planet': "select"})
def weight_on_planet(planet: Planet=Planet.MERCURY, weight_on_earth: float=0) -> float:
	if isinstance(planet, Planet):
		return (planet.value/Planet.EARTH.value)*float(weight_on_earth)
	
	return (Planet[planet].value/Planet.EARTH.value)*float(weight_on_earth)



# @wapp.Page("/")
# def index(self):
# 	self.text("Hello World!")
# 	self.image("mars.jpg")
# 	self.form("weight_on_mars")


if __name__ == '__main__':
	

	wapp.run()