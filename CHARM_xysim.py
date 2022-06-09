# Create 1d position spectra based upon Gaussian shapes projected onto a wire grid
# Does fine structure arise

import matplotlib.pyplot as plt
import numpy as np
import math

# Plot either the final position spectra or the individual events
plot_spectra = False
# Subtract the threshold from the amplitude value - artifacts will appear in the position spectra without this
threshold_subtract = False

# Define a Gaussian distribution with a sensible width and amplitude
g_amp = 1000.
g_width = 2.

# Define threshold and calculate width of Gaussian at this level
thresh = 150.
delta = math.sqrt( -2 * g_width**2 * math.log(thresh/g_amp) )

# Range of positions to generate
xmin = 0.
xmax = 10.

# Simulate events uniformly
num_events = 10000
pos_x = np.random.uniform(xmin,xmax,num_events)
if (plot_spectra==False):
  num_events = 10
  pos_x = np.linspace(xmin,xmin+1,num_events)

#pos_x = np.linspace(2.7, 3.1, num_events)

# Create np array of zeros for filling with calculated values
calc_x = np.zeros(num_events)

plt.close()

#for entry in pos_x:
for i in range (0,num_events):
  entry = pos_x[i]
  # First channel is centroid - delta rounded up, last is centroid + delta rounded down
  xstart = int(math.ceil(entry - delta))
  xend = int(math.floor(entry + delta))
  total = 0
  valsum = 0
  
  # Loop over participating channels
  for chan in range (xstart, xend+1):
    
    val = g_amp * math.exp( -( (chan-entry)**2 ) / (2*g_width**2) ) 
    if (subtract_threshold==True):
      val -= thresh
    valsum += val
    total += val*chan
    # If event plotting is on add points
    if(plot_spectra==False):
      plt.plot(chan, val, 'ro')
      print("\n" + str(chan) + " " + str(val))
  
  # Get the centroid and store it in the results array
  calc_val = total/valsum
  calc_x[i] = calc_val
  
  if(plot_spectra==False):
    # Plot the generated Gaussian together with the individual wire values
    print("Centroid: " + str(round(entry,2)) + " Calculated: " + str(round(calc_val,2)))
    plt.grid()
    xvals = np.linspace(entry-2*delta,entry+2*delta,100)
    yvals = g_amp * np.exp( -( (entry-xvals)**2 ) / (2*g_width**2) )
    plt.plot(xvals,yvals)
    plt.axhline(y=thresh, color='r', linestyle='dotted')
    
    plt.show()

    plt.clf()
  
  
# Plot results
if (plot_spectra):
  nbins = int((xmax-xmin)*100)
  f, (ax1, ax2) = plt.subplots(2, 1, sharex=False)
  ax1.hist(pos_x, nbins)
  ax2.hist(calc_x, nbins)
  ax1.set_title("Amp: " + str(g_amp) + " Width: " + str(g_width) + "\nThresh: " + str(thresh) + " Mult: " + str(round(delta*2,1)))
  plt.show()
