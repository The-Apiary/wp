"""@package wp.palette
Palette generation scripts
"""

import numpy as np
import time
import os                   # for abspath
from PIL import Image
from sklearn.cluster import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt    

class PaletteGenerator:
    """The palette generator class takes an image and maintains the resources
    used for deconstruction, partitioning, and palette selection. """

    # public
    colors = []             # colors extracted from image
    palette = []            # dominant colors from image

    # private-ish
    src_ = None             # string used to load image
    verbosity_ = 0          # verbosity level [0-2]
    image_ = None           # image loaded
    estimator_ = None       # estimator obj used to partition
    clusters_ = []          # a partitioning on self.colors
    centroids_ = []         # averages of the colors in each cluster

    def __init__(self, verbosity=0):
        self.verbosity_=verbosity

    def __extractColors(self):
        w,h = self.image_.size
        colors = []
        for n,c in self.image_.getcolors(w*h):
            for i in range(n):
                colors.append(list(c))
     
        self.colors = colors

    def __extractCentroids(self):
        centroids = []
        for cl in self.clusters_:
            mean = [0,0,0]
            size = len(cl)
            for c in cl:
                mean[0] += float(c[0])/size
                mean[1] += float(c[1])/size
                mean[2] += float(c[2])/size

            centroids.append([int(mean[0]),int(mean[1]),int(mean[2])])

        self.centroids_ = centroids

    def colorSpread(self, nbins):
        bins = [False for i in range(nbins*nbins*nbins)]
        for c in self.colors:
            x = min(c[0]*nbins/255, nbins-1)
            y = min(c[1]*nbins/255, nbins-1)
            z = min(c[2]*nbins/255, nbins-1)
            bins[x + y*nbins + z*nbins*nbins] = True

        filled = 0
        for b in bins:
            if b == True:
                filled += 1

        return float(filled)/len(bins)

    def colorDistribution(self, nbins=16):
        if nbins < 2 or nbins % 2 != 0:
            print "colorDistribution expects an integer power of two > 2"
            return

        nbins_coarse = nbins / 2
        bins = [0 for i in range(pow(nbins,3))]
        bins_coarse = [0 for i in range(pow(nbins_coarse,3))]
        
        cfull = 0
        cfullcoarse = 0
        for c in self.colors:
            x = c[0]*nbins/256
            y = c[1]*nbins/256
            z = c[2]*nbins/256
            bins[x + y*nbins + z*nbins*nbins] += 1
            if bins[x + y*nbins + z*nbins*nbins] == 1:
                cfull += 1

            xf = c[0]*nbins_coarse/256
            yf = c[1]*nbins_coarse/256
            zf = c[2]*nbins_coarse/256
            bins_coarse[xf + yf*nbins_coarse + zf*nbins_coarse*nbins_coarse] += 1
            if bins_coarse[xf + yf*nbins_coarse + zf*nbins_coarse*nbins_coarse] == 1:
                cfullcoarse += 1

        subset = [0 for x in range(cfullcoarse*2*2*2)]
        csub = 0
        for x in bins_coarse:
            if x != 0:
                subset[csub] = x
                csub += 1

        mean = np.mean(subset)
        std = np.std(subset)

        return mean, std

    def __DBSCAN(self, args=None):
        """cluster color data using the DBSCAN algorithm"""
        if args == None:
            best_eps = 8

            n = 1.0 # number of std deviations
            mean,std = self.colorDistribution(256/best_eps)

            best_min_samples = mean + n * std
            best_metric = 'euclidean'
            best_random_state = np.random

            self.estimator_ = DBSCAN(
                eps = best_eps,
                min_samples = best_min_samples,
                metric = best_metric,
                random_state = best_random_state,
            )
        else:
            self.estimator_ = DBSCAN(**args)
    
    def __K_MEANS(self, args=None):
        """culster color data using the k-means algorithm"""
        if args == None:
            best_n_clusters = 8
            best_max_iter = 100 
            best_n_init = 10
            best_init = 'k-means++'
            best_precompute_distances = True
            best_n_jobs= -1
            best_random_state = np.random

            self.estimator_ = KMeans(
                n_clusters = best_n_clusters,
                max_iter = best_max_iter,
                n_init = best_n_init,
                init = best_init,
                precompute_distances = best_precompute_distances,
                n_jobs = best_n_jobs,
                random_state = best_random_state,
            )
        else:
            self.estimator_ = KMeans(**args)
    
    def load(self, path):
        """load image from path"""
        self.src_=os.path.abspath(path)
        self.image_=Image.open(self.src_)
        self.__extractColors()

    def resize(self, size):
        """resize image"""
        self.image_.thumbnail(size, Image.ANTIALIAS)
        self.__extractColors()

    def partitionColors(self, alg, args=None):
        """partitions image colors"""
        
        # step one: setup estimator
        setup_estimator = {
            'DBSCAN':self.__DBSCAN,
            'KMeans':self.__K_MEANS,
        }.get(alg)

        setup_estimator(args)

        if self.verbosity_ > 0:
            print(":: estimator = %s" % self.estimator_)

        # step two: perform clustering
        self.estimator_.fit(np.array(self.colors))

        # step three: ascertain partitioning from clustering output
        labels = self.estimator_.labels_
        unique_labels = list(set(labels))
        label_map = {}
        clusters = []
        for i in range(len(unique_labels)):
            clusters.append([])
            label_map[unique_labels[i]] = i

        for i in range(len(self.colors)):
            clusters[label_map[labels[i]]].append(list(self.colors[i]))

        self.clusters_ = clusters
        
        if self.verbosity_ > 0:
            print(':: n_clusters = %d' % len(self.clusters_))

        # step four: extract centroids from partitions
        self.__extractCentroids()

    def showColors(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for c in self.colors:
            nc=[float(c[0])/255,float(c[1])/255,float(c[2])/255]
            ax.scatter(c[0],c[1],c[2],c=nc)

        ax.set_xlabel('Red')
        ax.set_ylabel('Green')
        ax.set_zlabel('Blue')

        plt.show()

    def showPartitions(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        labels = list(set(self.estimator_.labels_))
        for i in range(len(self.clusters_)):
            if labels[i] == -1.0:
                continue
                
            nc=[
                float(self.centroids_[i][0])/255,
                float(self.centroids_[i][1])/255,
                float(self.centroids_[i][2])/255
            ]
            for c in self.clusters_[i]:
                ax.scatter(c[0],c[1],c[2],c=nc)

        ax.set_xlabel('Red')
        ax.set_ylabel('Green')
        ax.set_zlabel('Blue')

        plt.show()
        if self.verbose:
            print "[DONE]"