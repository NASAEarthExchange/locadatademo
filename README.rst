LOCA Data Access Demonstration
====================================

Introduction
-----------
In this tutorial we’re going to look at a very simple way to build a list of LOCA [#]_ data urls that point to files, or 
objects, in the opennex amazon web services S3 bucket [#]_. We will also show how to programmatically download one data 
object, find a point location of interest in that data object, extract a time series of data for the point of interest 
and then build a rudimentary time-series plot. Finally, using the same data object we've retrieved, we will choose and 
extract single time step and do a plot of that time step over the full spatial domain. This tutorial is really focused 
on how to quickly find and get direct access to data objects or files on amazon web services and tailored to those that 
may be building more comprehensive scripts in the future. The examples here could be combined and modified so one can
easily gain access to the full data-set and so some analytics tasks. 

For these examples, we will use two different programming languages, python [#]_ and R [#]_. More information on 
these can be found by following the links listed below. 

See the short `YouTube <https://www.youtube.com/channel/UCctSyxWU6w86es5UiudUhTA>`_ video for the full accompany presentation.


Demonstration Dependencies and Assumptions
--------------------------------------------
We make a few assumptions about you and your system environment here: you have a basic understanding of how to work in 
a terminal and run commands from a command line. On Mac-OS (used to illustrate the steps in this tutorial) the 
Terminal.app [#]_ works well. Linux or Unix users should be familiar with a standard terminal and shell, such as bash [#]_, 
and windows users will need to use something like powershell [#]_. You should already have python (version 2 or 3) installed 
along with a few library dependencies, the requests [#]_ package, matplotlib [#]_, numpy [#]_ and the netCDF4 [#]_ 
packages; again, see the links below if you need more information on how to install these on your system or refer to your 
system documentation if you don’t already have these packages working. If you want to execute the R example you will need the 
R application and you must be a little familiar with how to run basic R commands. You will need the additional R package 
jsonlite [#]_. Also, You should have the git [#]_ [#]_ application installed on your system. Git will be used to copy or 
clone the example scripts from github [#]_ to your local system. You can skip this step if you want and just directly download the 
scripts to a local folder using a browser if that is easier for you. 

A few other things worth mentioning, all objects, or files, are located on amazon web services S3 object store [#]_ that is 
physically located in Oregon, the us-west-2 region [#]_. Depending on where you are accessing both the data and the
simple index json files from, what your network connect is, and your system capabilities you will see different performance 
with download speeds and demonstration responsiveness. Ideally, one would spin up an EC2 instance(s) [#]_ in the us-west-2 
region to do any processing there, but that is not a requirement for this tutorial. 

Demonstration Steps and discussion
----------------------------------

* First, clone the repository that is posted on github and change to the repo directory.

  ::

    $ git clone https://github.com/NASAEarthExchange/locadatademo.git
    $ cd locaaccessdemo

  Or, you can directly download the `zip file here <https://github.com/NASAEarthExchange/locadatademo/archive/master.zip>`_ .

* Open the file *locaS3find.py* in your favorite text editor and take a look.

  ::

    $ vim locaS3find.py

  Note the routines *get_json* and *select_loca_data*. 

* Run the script *locaS3find.py*

  ::

    $ python ./locaS3find.py

* If you wish take a look at the simple `json based index file <http://nasanex.s3.amazonaws.com/LOCA/loca-s3-files.json>`_ that 
  was posted in the S3 bucket that enabled the basic select routine. Download it and open it in your favorite text editor, e.g.
  
  ::

    $ vim loca-s3-files.json

  As you can see this is very basic but effective structure in that we can retrieve a listing of files, or object, by model name, representative 
  pathway (often said rcp), variable name like maximum temperature or minimum temperature, over a valid time span, e.g. year 2006 to 2100. We can 
  also the prepend the historical runs, 1950 to 2100 to our list. Our trivial select routine in *locaS3find.py* simplifies the process of getting 
  all links based on our parameters through a simple routine without the need of sql or nosql database servers or web services. 

* Next open the file *locaS3find.r* in your favorite text editor and take a look.

  ::

    $ vim locaS3find.r

  The rscript is answering the same question as the python script, namely: we want the list of loca data objects of maximum temperature for 
  some random model, for rcp45, from 1950 to 2100. Run the rscript:

  ::

    $ Rscript ./locaS3find.r 


* Next, open the file *locaS3Peek.py* in your favorite text editor.
  
  ::

    $ vim locaS3Peek.py

  This script will download one data object, a netcdf file [#]_, from the S3 object store (if it hasn't already been downloaded), it will pick a 
  time step and extract the full spatial domain at that step and plot the full map. Next, the script will extract the data for a point, our point 
  is given at the top of the script, which is the latitude and longitude of the NIST Net-Zero energy building [#]_ experiment. You can take a look
  at the building, our point of interest, via `google maps <https://goo.gl/maps/PfHsAJH8iZx>`_ if your interested. Run the python script:
  
  ::

    $ python ./locaS3Peek.py


Final Discussion
----------------
This basic tutorial should give you an idea on how one might find and generate a url list for a given model, rcp, variable and valid 
time range. You also should have an understanding on how to open a data file or object, find a time step or location of interest, and then
extract the relevant data. As mentioned earlier, the discussion here is intended for those that would take these examples, join and modify them,
and then include the derivative script(s) into something larger and more interesting. 




References:
^^^^^^^^^^^

.. [#] http://loca.ucsd.edu 
.. [#] https://aws.amazon.com/nasa/nex/
.. [#] https://www.python.org
.. [#] https://www.r-project.org
.. [#] `https://en.wikipedia.org/wiki/Terminal_(macOS)`
.. [#] https://en.wikipedia.org/wiki/Unix_shell
.. [#] https://en.wikipedia.org/wiki/PowerShell 
.. [#] http://docs.python-requests.org/en/master/
.. [#] http://matplotlib.org
.. [#] http://www.numpy.org
.. [#] http://unidata.github.io/netcdf4-python/
.. [#] https://cran.r-project.org/web/packages/jsonlite/index.html
.. [#] https://git-scm.com
.. [#] https://en.wikipedia.org/wiki/Git
.. [#] https://github.com
.. [#] https://aws.amazon.com/s3/
.. [#] http://docs.aws.amazon.com/general/latest/gr/rande.html#s3_region
.. [#] https://aws.amazon.com/ec2/
.. [#] http://www.unidata.ucar.edu/software/netcdf/
.. [#] https://www.nist.gov/el/net-zero-energy-residential-test-facility

