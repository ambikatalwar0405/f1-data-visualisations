
import matplotlib as mpl
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection

import fastf1


colormap = mpl.cm.plasma



#load the session and extract desired data
session = fastf1.get_session(2025, 'Qatar', 'Q')
weekend = session.event
session.load()
lap = session.laps.pick_drivers('SAI').pick_fastest()

#get telemetry data
x = lap.telemetry['X']              
y = lap.telemetry['Y']              
color = lap.telemetry['Speed']      


points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)


fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))
fig.suptitle(f'Sainz Q3 lap Qatar 2025 speed representation', size=24, y=0.97)

#adjust margins and turn of axis
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
ax.axis('off')



#plot data
ax.plot(lap.telemetry['X'], lap.telemetry['Y'],
        color='black', linestyle='-', linewidth=16, zorder=0)

#normalise to whole values
#create a line collection, which lets us plot multiple lines
#set colours we want to represent speeds
norm = plt.Normalize(color.min(), color.max())
lc = LineCollection(segments, cmap=colormap, norm=norm,
                    linestyle='-', linewidth=5)

#set values used for colormapping
lc.set_array(color)

#merge all line segments together
line = ax.add_collection(lc)


#create legend
cbaxes = fig.add_axes([0.25, 0.05, 0.5, 0.05])
normlegend = mpl.colors.Normalize(vmin=color.min(), vmax=color.max())
legend = mpl.colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=colormap,
                                   orientation="horizontal")


plt.show()
