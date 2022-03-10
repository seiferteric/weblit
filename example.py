
from weblit import Weblit

MARS_G=3.721
EARTH_G=9.807

app = Weblit("Weight on Mars")

@app.Form
def weight_on_mars(weight_on_earth: float=0):
	return (MARS_G/EARTH_G)*float(weight_on_earth)

if __name__ == '__main__':
	app.run()