
# A simple example showing how to extract and plot some of the LOCA downscale 
# climate projections data; data downloaded from the LOCA S3 cache copy. 
# This example does spatial and temporal plots, for entertainment and 
# coding educational purposes only. See http://loca.ucsd.edu for the official 
# distribution and general information about the data.

import sys, os
import random, urllib2
import pprint
import requests
import matplotlib.pyplot as plt 
from matplotlib.dates import DateFormatter
import numpy

NIST_NET_ZERO_RESIDENCE_LOC = (39.138356, -77.219574)
# google maps view: https://goo.gl/maps/PfHsAJH8iZx

# An Assessment of Typical Weather Year Data Impacts vs. Multi-year 
# Weather Data on Net-Zero Energy Building Simulations
# http://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1204.pdf

# Comparing the Energy and Economic Performance of the NIST NZERTF 
# Design across the Mixed-Humid Climate Zone
# http://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1603.pdf

try:
   import netCDF4
except ImportError, e:
   sys.stderr.write(str(e)+"\n\nYou need to install\nhdf5 (https://www.hdfgroup.org/HDF5/),\n"+\
                    "netcdf (http://www.unidata.ucar.edu/software/netcdf/),\n"+\
                    "netCDF4 (https://pypi.python.org/pypi/netCDF4)\nfor this example to run.\n\n")
   sys.exit(1)


def plot_data_temp_spatial(dat, data_min, data_max, fnameout, datlab):
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.imshow(data, vmin=data_min, vmax=data_max, origin='lower', cmap=plt.cm.get_cmap('jet',18))
    plt.colorbar(drawedges=True, ticks=numpy.linspace(data_min,data_max,10), orientation='horizontal', extend='both', pad=0.05, shrink=0.8).set_label(u'\N{DEGREE SIGN}C')
    plt.title('Temp '+str(datlab))
    plt.savefig(fnameout)
    
    
def plot_data_temp_time(dat, tms, fnameout):
    plt.rcParams['figure.figsize'] = (12, 8)
    monthsFmt = DateFormatter("%b '%Y")
    fig, ax = plt.subplots()
    ax.plot_date(tms, dat, '-')
    ax.xaxis.set_major_formatter(monthsFmt)
    ax.autoscale_view()
    fig.autofmt_xdate()
    plt.title('Temp')
    plt.savefig(fnameout)


if __name__ == '__main__':
    # stage a local copy (for simplicity)
    remote = 'http://nasanex.s3.amazonaws.com/LOCA/CESM1-BGC/16th/rcp85/r1i1p1/tasmax/tasmax_day_CESM1-BGC_rcp85_r1i1p1_20500101-20501231.LOCA_2016-04-02.16th.nc'
    localfnm = os.path.split(remote)[1]

    # download the file in chunks, if needed. Note: the file is about 332M
    if not os.path.exists(localfnm):
        wheel, chnksz = ['|', '/', '-', '\\'], 262144
        try:
            localfd = open(localfnm, "wb")
            r = requests.get(remote, stream=True, timeout=1)
            for i, chunk in enumerate(r.iter_content(chunk_size=chnksz)): 
               if chunk: 
                  localfd.write(chunk)
                  sys.stdout.write('\r['+wheel[i%4]+"] "+str((i+1)*chnksz)+' bytes')
                  sys.stdout.flush()
            localfd.close()
            sys.stdout.write('\n')
        except (Exception, KeyboardInterrupt), e:
            if os.path.exists(localfnm): os.unlink(localfnm)
            sys.stderr.write("download failed : "+str(e)+"\n")
            sys.exit(1)

    # now open the local file
    ncfd = netCDF4.Dataset(localfnm)

    # print some metadata
    pprint.pprint(ncfd.variables)
    pprint.pprint(ncfd.dimensions)

    # probe (convert to python datetimes) and print the available time steps for this file
    dtms = netCDF4.num2date(ncfd['time'][:], units=ncfd['time'].units, calendar=ncfd['time'].calendar)
    for i,d in enumerate(dtms):
        print "[%d] %s" % (i, d)

    # randomly choose a time step
    step = random.choice(range(len(dtms)))
    print 'selected step',  step, dtms[step]

    # get variables handle
    var = ncfd.variables['tasmax']

    # get the fill value/no data value
    na = float(var._FillValue)

    rawdata = var[step,:,:]

    # convert var units (kelvin to Celsius)
    print 'var units', var.units
    data = numpy.ma.masked_where(rawdata==na, rawdata-273.15)

    print 'plotting map...'
    plot_data_temp_spatial(data, -10.0, 40.0, localfnm+".%04d.png" % step, dtms[step].strftime("%Y-%m-%d"))

    # now look through the time dimension, but we need to find the location index we're interested in (convert coords) 
    latidx = (numpy.abs(ncfd['lat'][:] - NIST_NET_ZERO_RESIDENCE_LOC[0])).argmin()
    lonidx = (numpy.abs(ncfd['lon'][:] - (360.0 + NIST_NET_ZERO_RESIDENCE_LOC[1])  )).argmin()

    # get the data at y,x over all time steps in this file (convert units)
    rawdatat = var[:,latidx, lonidx]
    data = numpy.ma.masked_where(rawdatat==na, rawdatat-273.15)

    print 'plotting time series...'
    plot_data_temp_time(data, dtms, localfnm+".%04d_%04d.png" % (latidx, lonidx))

    ncfd.close()
#__main__
