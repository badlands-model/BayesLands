import numpy as np
import random
import time
import math
import cmocean as cmo
from pylab import rcParams
import fnmatch
import shutil
from PIL import Image
from io import StringIO
from cycler import cycler
import os

import matplotlib as mpl
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

from scipy.spatial import cKDTree
from scipy import stats 
from pyBadlands.model import Model as badlandsModel
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.mplot3d import Axes3D

def plotPosterior(fname, pos_rmse, pos_rain, pos_erod):
		nb_bins=30
		slen = np.arange(0,len(pos_rmse),1)
		font = 9
		width = 1

		#Rain#
		rainmin, rainmax = min(pos_rain), max(pos_rain)
		print rainmin, rainmax, len(pos_rmse)
		rainspace = np.linspace(rainmin,rainmax,len(pos_rmse))
		rainm,rains = stats.norm.fit(pos_rain)
		pdf_rain = stats.norm.pdf(rainspace,rainm,rains)
		rain_real_value = 0

		fig = plt.figure(figsize=(6,8))
		ax = fig.add_subplot(111)
		ax.spines['top'].set_color('none')
		ax.spines['bottom'].set_color('none')
		ax.spines['left'].set_color('none')
		ax.spines['right'].set_color('none')
		ax.tick_params(labelcolor='w', top='off', bottom='off', left='off', right='off')
		ax.set_title(' Rain Parameter', fontsize=  font+2)#, y=1.02)
		ax1 = fig.add_subplot(211)
		ax1.set_facecolor('#f2f2f3')
		ax1.hist(pos_rain, bins=25, alpha=0.5, facecolor='sandybrown', normed=True)
		#ax1.axvline(rainmode,linestyle='-', color='orangered', linewidth=1,label=None)

		# ax1.plot(mspace,pdf_m,label='Best fit',color='orangered',linestyle='--')
		ax1.grid(True)
		ax1.set_ylabel('Frequency',size= font+1)
		ax1.set_xlabel(r'$\varepsilon$', size= font+1)
		ax2 = fig.add_subplot(212)
		ax2.set_facecolor('#f2f2f3')
		ax2.plot(slen,pos_rain,linestyle='-', linewidth= width, color='k', label=None)
		ax2.set_title(r'Trace of $\varepsilon$',size= font+2)
		ax2.set_xlabel('Samples',size= font+1)
		ax2.set_ylabel(r'$\varepsilon$', size= font+1)
		ax2.set_xlim([0,np.amax(slen)])
		fig.tight_layout()
		fig.subplots_adjust(top=0.88)
		plt.savefig('%srain.png'% (fname), bbox_inches='tight', dpi=300, transparent=False)
		plt.clf()

		#Erod#
		erodmin, erodmax = min(pos_erod), max(pos_erod)
		erodspace = np.linspace(erodmin,erodmax,len(pos_erod))
		erodm,erods = stats.norm.fit(pos_erod)
		pdf_erod = stats.norm.pdf(erodspace,erodm,erods)
		erodmean=np.mean(pos_erod)
		erodmedian=np.median(pos_erod)
		#erodmode, count= stats.mode(pos_erod)
	
		fig = plt.figure(figsize=(6,8))
		ax = fig.add_subplot(111)
		ax.spines['top'].set_color('none')
		ax.spines['bottom'].set_color('none')
		ax.spines['left'].set_color('none')
		ax.spines['right'].set_color('none')
		ax.tick_params(labelcolor='w', top='off', bottom='off', left='off', right='off')
		ax.set_title(' Erosion Parameter', fontsize=  font+2)#, y=1.02)
		ax1 = fig.add_subplot(211)
		ax1.set_facecolor('#f2f2f3')
		ax1.hist(pos_erod, bins=25, alpha=0.5, facecolor='sandybrown', normed=True)
		#ax1.axvline(erodmode,linestyle='-', color='orangered', linewidth=1,label=None)

		# ax1.plot(mspace,pdf_m,label='Best fit',color='orangered',linestyle='--')
		ax1.grid(True)
		ax1.set_ylabel('Frequency',size= font+1)
		ax1.set_xlabel(r'$\varepsilon$', size= font+1)
		ax2 = fig.add_subplot(212)
		ax2.set_facecolor('#f2f2f3')
		ax2.plot(slen,pos_erod,linestyle='-', linewidth= width, color='k', label=None)
		ax2.set_title(r'Trace of $\varepsilon$',size= font+2)
		ax2.set_xlabel('Samples',size= font+1)
		ax2.set_ylabel(r'$\varepsilon$', size= font+1)
		ax2.set_xlim([0,np.amax(slen)])
		fig.tight_layout()
		fig.subplots_adjust(top=0.88)
		plt.savefig('%serod.png'% (fname), bbox_inches='tight', dpi=300, transparent=False)
		plt.clf()

		# RMSE #
		rmsemin, rmsemax = min(pos_rmse), max(pos_rmse)
		rmsespace = np.linspace(rmsemin,rmsemax,len(pos_rmse))
		rmsem,rmses = stats.norm.fit(pos_rmse)
		pdf_rmse = stats.norm.pdf(rmsespace,rmsem,rmses)
		rmsemean=np.mean(pos_rmse)
		rmsemedian=np.median(pos_rmse)
		#erodmode, count= stats.mode(pos_erod)
	
		fig = plt.figure(figsize=(6,8))
		ax = fig.add_subplot(111)
		ax.spines['top'].set_color('none')
		ax.spines['bottom'].set_color('none')
		ax.spines['left'].set_color('none')
		ax.spines['right'].set_color('none')
		ax.tick_params(labelcolor='w', top='off', bottom='off', left='off', right='off')
		ax.set_title(' RMSE', fontsize=  font+2)#, y=1.02)
		ax1 = fig.add_subplot(211)
		ax1.set_facecolor('#f2f2f3')
		
		#ax1.plot(pos_rmse)
		ax1.plot(slen,pos_rmse,color='orangered', linestyle='-', linewidth= width, label=None)
		ax1.grid(True)
		ax1.set_ylabel('RMSE',size= font+1)
		ax1.set_xlabel('Accepted samples', size= font+1)
		ax1.set_xlim([0,np.amax(slen)])
		fig.tight_layout()
		plt.savefig('%srmse.png'% (fname), bbox_inches='tight', dpi=300, transparent=False)
		plt.clf()

def main():

	run_nb = input('Please enter the folder number i.e. mcmcresults_% ')

	fname = 'mcmcresults_%s/' % (run_nb)
	rmse_filename = 'mcmcresults_%s/accept_rmse.txt' % (run_nb)
	rain_filename = 'mcmcresults_%s/accept_rain.txt' % (run_nb)
	erod_filename = 'mcmcresults_%s/accept_erod.txt' % (run_nb)
	#m_filename = 'mcmcresults_%s/accept_m.txt' % (run_nb)
	#n_filename = 'mcmcresults_%s/accept_n.txt' % (run_nb)
	
	filename_list = []
	filename_list.append(rmse_filename)
	filename_list.append(rain_filename)
	filename_list.append(erod_filename)
	#filename_list.append(m_filename)
	#filename_list.append(n_filename)

	rmse = []
	rain = []
	erod = []
	#m = []
	#n = []

	for list_name in filename_list:
		with open(list_name) as f:
			next(f)
			for line in f:
				words = line.split()
				error = words[2]
				lname =  list_name[-8:-4]
				if lname == 'rmse':
					rmse.append(error)
				elif lname == 'rain':
					rain.append(error)
				elif lname == 'erod':
					erod.append(error)	

	print 'length of rmse', len(rmse)
	print 'length of rain', len(rain)
	print 'length of erod', len(erod)

	rmse_ = np.asarray(rmse, dtype = float)
	rain_ = np.asarray(rain, dtype = float)
	erod_ = np.asarray(erod, dtype = float)

	print len(rmse)
	print rmse_.shape
	plotPosterior(fname, rmse_, rain_, erod_)
	
	print '\nFinished plotting'

if __name__ == "__main__": main()

