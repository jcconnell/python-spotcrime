import datetime
from spotcrime import SpotCrime

sc = SpotCrime((28.869508, -81.296004), 30, miles=True)
print("got here")
for incident in sc.get_incidents(datetime.datetime.now().date(), None, ['Community Policing']):
  print(incident)
