SELECT date(time) as date, max(mag) as magnitude
from earthquakes
group by date(time)