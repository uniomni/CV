#!/usr/bin/env python
# 
#
#  Program cpt2rgb:
#  Convert GMT *.cpt color palette file to *.rgb format used by NCL/PyNGL.
# 
# Creation date: Wed Jan 12 16:23:31 EST 2005 
# Author: 
# Derrick Snowden
# Physical Oceanography Division
# NOAA/AOML


import os, sys
import string
#from optik import OptionParser	# Newer Pythons might rename this to optparse																														  
import scipy as ML
import Numeric as N

def readcpt(name):
	f = open(name,'r')
	lines = f.readlines()
	f.close()
	return lines
	
def gmtcolormap(lines,nColors=None):
	import colorsys
	# f = open('/sw/share/'+ name +'.cpt')
	# Pass already parsed lines rather than a filename
	# so that a default length can be used.
	# lines = f.readlines()
	# f.close()

	x = []
	r = []
	g = []
	b = []
	colorModel = 'RGB'
	for l in lines:
		ls = l.split()
		if l[0] == '#':
		   if ls[-1] == 'HSV':
			   colorModel = 'HSV'
			   continue
		   else:
			   continue
		if ls[0] == 'B' or ls[0] == 'F' or ls[0] == 'N':
		   pass
		else:
			x.append(float(ls[0]))
			r.append(float(ls[1]))
			g.append(float(ls[2]))
			b.append(float(ls[3]))
			xtemp = float(ls[4])
			rtemp = float(ls[5])
			gtemp = float(ls[6])
			btemp = float(ls[7])
		
	x.append(xtemp)
	r.append(rtemp)
	g.append(gtemp)
	b.append(btemp)

	nTable = len(r)	   
	x = N.array( x , N.Float)
	r = N.array( r , N.Float)
	g = N.array( g , N.Float)
	b = N.array( b , N.Float)
	xmin = x[0]
	rangeOfX = x[-1] - x[0]
	x = (x - xmin)/rangeOfX
	
	# How long will the new colormap be?
	if not nColors:
		nColors = len(r)
	
	xx = ML.linspace(x[0], x[-1], nColors)
	xx = N.array( xx, N.Float)
	if colorModel == 'HSV':
	   for i in range(r.shape[0]):
		   rr,gg,bb = colorsys.hsv_to_rgb(r[i]/360.,g[i],b[i])
		   r[i] = rr ; g[i] = gg ; b[i] = bb

	rxx = xx*0.0
	gxx = xx*0.0
	bxx = xx*0.0
	for i in range(nColors):
		j = N.searchsorted(x,xx[i])
		if j == 0:
			rxx[i] = r[0] ; gxx[i] = g[0] ;bxx[i] = b[0]
		elif j == x.shape[0]:
			rxx[i] = r[-1] ; gxx[i] = g[-1] ;bxx[i] = b[-1]
		else:
			rxx[i] = r[j-1] + (r[j] - r[j-1])*(xx[i]-x[j-1])/(x[j]-x[j-1])
			gxx[i] = g[j-1] + (g[j] - g[j-1])*(xx[i]-x[j-1])/(x[j]-x[j-1])
			bxx[i] = b[j-1] + (b[j] - b[j-1])*(xx[i]-x[j-1])/(x[j]-x[j-1])
			
	# This was originally written for Matlab which wants rgb in 
	# 0.0-1.0, NCL uses 0-255
	#if colorModel == 'RGB':
		#rxx = rxx/255.
		#gxx = gxx/255.
		#bxx = bxx/255.
		
	rxx = rxx.tolist()
	gxx = gxx.tolist()
	bxx = bxx.tolist()
		
	return (rxx, gxx, bxx)

def main ():

	usage = "\n%prog: Converts GMT *.cpt color palette file to *.rgb format used by NCL/PyNGL.\n\n\
	This program will convert between an RGB or HSV colormap stored in a *.cpt file \n \
	used by GMT (Generic Mapping Tools http://gmt.soest.hawaii.edu) \n \
	into an RGB colormap which is then written to a *.rgb ascii text file.  The *.rgb files \n \
	can then be used with NCL or PyNGL (NCAR Command Language or its Python \n \
	extensions http://www.ncl.ucar.edu/index.shtml).  Optionally, the length \n \
	of the colormap can be changed using linear interpolation into the colorspace.  \n \n\
	$> %prog [options] <cptfilename> \n \
	\n \
	<cptfilename>  Input cpt file to translate (cpt extension is optional).\n"
	parser = OptionParser(usage,version="%prog 1.0")
	parser.add_option("-o", "--outputfile", type="string", dest="rgbfilename",
		default="stdout",help="Output rgb file to write (rgb extension is optional) [default stdout].")
	parser.add_option("-n", "--numcolors",
		default=None, dest="n_colors",type="int",help="Length of new colormap calculated using linear interpolation. [default to length of colormap in file.]")
	parser.add_option("-v", "--verbose",
		action="store_true", dest="verbose",help="Execute in verbose mode")
	parser.add_option("-q", "--quiet",
		action="store_false", dest="verbose",help="Cancel verbose mode")
	#[... more options ...]
																														  
	(options, cptfilename) = parser.parse_args()
	
	if len(cptfilename) != 1:
		parser.print_help()
		print "\nERROR: No cpt file name was found on the command line.\n" 
		sys.exit(-1)
		
	# Change cptfilename from list to string
	cptfilename = cptfilename[0]
																															  
	if options.verbose:
		print "reading %s..." % cptfilename
																														  
	cpt = readcpt(cptfilename)
	
	if not options.n_colors:
		r,g,b = gmtcolormap(cpt) # Use full cmap
	else:
		r,g,b = gmtcolormap(cpt,nColors=options.n_colors)

	# Where to write the output?
	if options.rgbfilename=='stdout':
		rgbfilename = sys.stdout
	else:
		if options.rgbfilename.endswith('rgb'):
			outfile = options.rgbfilename
		else:
			outfile = options.rgbfilename+'.rgb'
		rgbfilename = file(outfile,'w')
		
	rgbfilename.write('ncolors= %d\n' % len(r))
	for i in range(len(r)):
		rgbfilename.write('%d %d %03.0d\n' % (r[i], g[i], b[i]))
	
	rgbfilename.close()
	sys.exit(1)
	
	
if __name__ == "__main__":
	main()



#
#
# :mode=python:tabSize=4:indentSize=4:noTabs=false:
# :folding=indent:collapseFolds=3:wrap=soft:maxLineLen=150:
#
#



