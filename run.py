import datetime
from spotcrime import SpotCrime

sc = SpotCrime((28.869508, -81.296004), 0.03, None, ['Other'], days=10)
print(sc.get_map_url())
for incident in sc.get_incidents():
  print(incident)
