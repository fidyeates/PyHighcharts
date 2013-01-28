
from chart import Highchart
from common import Formatter

import sys, math, random

example_config = {
    "xAxis": {
        "gridLineWidth": 0,
        "lineWidth": 0,
        "tickLength": 0,
    },
    "yAxis": {
            "gridLineWidth": 0,
    }
}

def pie_example():
	H = Highchart()
	H.title("Pac Man Highchart")
	H.add_data_set([["Does Not Resemble Pac Man",25],["Resembes Pac Man", 75]],series_type="pie",name="",startAngle=45)
	H.colors(["#99CCFF","#FFFF66"])
	H.set_options(example_config)
	H.show()


def spline_example():
	H = Highchart()
	data = [math.sin(x/100.0) for x in range(0,int(4*math.pi*100),int(math.pi/16*100))]
	H.title("Sin Spline")
	H.add_data_set(data,series_type="spline",name="Sin")
	H.set_options(example_config)
	H.show()


def area_example():
	H = Highchart()
	data = [i**2 for i in range(10)]
	H.title("Area Example")
	H.add_data_set(data,series_type="area",name="Area")
	H.set_options(example_config)
	H.show()


def multiple_example():
	H = Highchart()
	revenue = [random.randint(1000,7000) for i in range(24)]
	spend = [random.randint(2000,4000) for i in range(24)]
	profit = [r - spend[i] for i, r in enumerate(revenue)]
	cumulative_profit = [sum(profit[:i])+5000 for i, v in enumerate(profit)]
	H.title("Multiple Example")
	H.add_data_set(revenue,series_type="line",name="Revenue",index=2)
	H.add_data_set(spend,series_type="line",name="Spend",index=3)
	H.add_data_set(cumulative_profit,series_type="area",name="Balance",index=1)
	H.set_options(example_config)
	H.show()






















if __name__ == '__main__':
	print sys.argv
	multiple_example()