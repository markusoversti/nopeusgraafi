import json
import numpy as np 
import matplotlib
import matplotlib.pyplot as plt 
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import matplotlib.ticker as ticker
from datetime import datetime, timedelta
#import datetime

tuloslista = []
aikalista = []
latauslista = []
uppauslista = []
nopeuslista = [] 
#kuvalista = []

tuloslaskuri = 0
latausavg = 0
uppausavg = 0
latauska = []
uppauska = []

aikakorjaus = 2

with open('nopeudet.json') as tiedosto:
    for jsonObj in tiedosto:
        tmptulos = json.loads(jsonObj)
        tuloslista.append(tmptulos)

for tulos in tuloslista:
    #print(tulos['timestamp'])
    #print(tulos['download']['bandwidth']/1000000)
    #print(tulos['upload']['bandwidth']/1000000)

    #aikalista.append(tulos['timestamp'])
    tuloslaskuri = tuloslaskuri + 1
    aikalista.append(datetime.strptime(tulos['timestamp'], '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours = aikakorjaus)) 

    latauslista.append(tulos['download']['bandwidth']*0.000008)
    uppauslista.append(tulos['upload']['bandwidth']*0.000008)
    
    if (len(aikalista) >= 4):
        latauska.append((latauslista[tuloslaskuri-1]+latauslista[tuloslaskuri-2]+latauslista[tuloslaskuri-3]+latauslista[tuloslaskuri-4])/4)
        uppauska.append((uppauslista[tuloslaskuri-1]+uppauslista[tuloslaskuri-2]+uppauslista[tuloslaskuri-3]+uppauslista[tuloslaskuri-4])/4)
    else:
        latauska.append(np.nan)
        uppauska.append(np.nan)

    nopeuslista.append([tulos['download']['bandwidth']*0.000008, tulos['upload']['bandwidth']*0.000008])

fig, ax = plt.subplots()
#xfmt = md.date

ax.scatter(aikalista, uppauslista, label='Lähetys', color='green',s=3)
ax.plot(aikalista, uppauska, label='Tunnin ka', color='blue')
ax.scatter(aikalista, latauslista, label='Lataus', color='orange', s=3)
ax.plot(aikalista, latauska, label='Tunnin ka', color='red')

ax.xaxis.set_major_locator(mdates.HourLocator(interval=6))
ax.xaxis.set_minor_locator(mdates.HourLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m %H:%M'))

ax.yaxis.set_major_locator(ticker.MultipleLocator(50))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(5))


#plt.yticks(np.arange(0, 300, 50))

#ax.yaxis.set_major_locator(np.arange[0,400])
#ax.yaxis.set_minor_locator([10])

fig.autofmt_xdate()

#ax.set_xlim([datetime.date(2021,2,9), datetime.date(2021, 2, 10)])


plt.title('Tuloksia: '+ str(tuloslaskuri) + ' Lähetys ka: ' + str( round(sum(uppauslista) / len(uppauslista))) + ' Lataus ka: '+str( round(sum(latauslista) / len(latauslista))))
plt.xlabel('Päivämäärä')
plt.ylabel('Nopeus Mbps')
plt.legend(loc='upper left')

plt.grid()

plt.show()
plt.savefig('/mnt/tiedostot/tiedostot_markus/nopeudet.png')
