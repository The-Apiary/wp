"""@package wp.palette
"""

import numpy as np
import time
import os
import sys
from threading import Thread
from PIL import Image
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans

def test(alg, args):
    pg = PaletteGenerator(True)
    pg.load("/home/ngvitovitch/.wallpapers/yoko2.jpg")
    pg.resize((200,200))
    pg.partitionColors(alg=alg, args=args)

class PaletteGenerator:
    src = None
    verbose = False
    colors = []

    def __init__(self, verbose=False):
        self.verbose=verbose

    def __extractColors(self):
        w,h = self.image_.size
        self.colors = []
        for n,c in self.image_.getcolors(w*h):
            for i in range(n):
                self.colors.append(c)

    def __DBSCAN(self, args):
        if self.verbose:
            print "Clustering via. DBSCAN"

        # cluster
        X = np.array(self.colors)
        estimator = DBSCAN(**args).fit(X)
        core_samples = estimator.core_sample_indices_
        labels = estimator.labels_
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)

        print('Estimated number of clusters: %d' % n_clusters)

    def __K_MEANS(self, args):
        if self.verbose:
            print "Clustering via. k-means"

        # cluster
        X = np.array(self.colors)
        estimator = KMeans(**args).fit(X)
        labels = estimator.labels_
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        
        print('Estimated number of clusters: %d' % n_clusters)

    def load(self, path):
        """load image from path"""
        self.image_ = Image.open(os.path.abspath(path))
        self.__extractColors()

    def resize(self, size):
        """resize image"""
        self.image_.thumbnail(size, Image.ANTIALIAS)
        self.__extractColors()

    def partitionColors(self, alg, args):
        """partitions image colors"""
        self.partition_ = []
        worker = {
            'DBSCAN':self.__DBSCAN,
            'KMeans':self.__K_MEANS,
        }.get(alg)

        worker(args)

        ### THREADING LATER?!?
        #worker_thread = Thread(target=worker, args=(args,))
        #worker_thread.start()

        #while worker_thread.isAlive():
        #    worker_thread.join(0.5)
        ###

        if self.verbose:
            print "[DONE]"