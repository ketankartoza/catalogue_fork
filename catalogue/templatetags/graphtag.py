from django import template

#Pie3D chart
from pygooglechart import PieChart3D

register = template.Library()

@register.simple_tag
def gPieChart(data,labels):
  #parseData
  mydata,mykeys = parseData(data,labels)

  chart = PieChart3D(600, 200)
  # Add some data
  chart.add_data(mydata[1:])
  # Assign the labels to the pie data
  chart.set_pie_labels(mykeys[1:])

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
