import datetime
from spotcrime import SpotCrime

sc = SpotCrime((28.869508, -81.296004), 0.03)
print(sc.get_map_url())
for incident in sc.get_incidents(datetime.datetime.now().date(), None, ['Community Policing']):
  print(incident)
