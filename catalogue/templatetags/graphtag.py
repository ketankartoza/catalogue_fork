from django import template

#Pie3D chart
from pygooglechart import PieChart3D

register = template.Library()

@register.simple_tag
def gPieChart(data,labels):
  #parseData
  mydata,mykeys = parseData(data,labels)

  chart = PieChart3D(600, 300)
  # Add some data
  chart.add_data(mydata[1:])
  # Assign the labels to the pie data
  chart.set_pie_labels(mykeys[1:])

  #set google chart set of colours
  chart.set_colours_within_series(('3366CC','DC3912','FF9900','109618','990099','0099C6','DD4477','66AA00','B82E2E','316395','994499','22AA99','AAAA11','6633CC','E47100','8B0707','651067','329262'))
  
  #return chart URL
  return chart.get_url()

def parseData(data,labels):
  keys = [key for key in labels]
  mydata=[]
  mylabels=[]
  for row in data:
    mydata.append(row['count'])
    mylabels.append(row[labels[keys[0]]])

  return mydata,mylabels
