from collections import namedtuple
from PIL import Image
import numpy
import colorsys

Point = namedtuple('Point', ('coord','ct'))
Bin = namedtuple('Bin', ('index','values'))
Sample = namedtuple('Sample', ('avg', 'std'))

class BucketClustering:
    orderedbuckets = None

    def __init__(self, data, bounds, g):
        self.__g = int(g)
        self.__step = 1.0 / g
        self.__bucketlist = [[[[]]*self.__g]*self.__g]*self.__g
        self.__data = data

    def __placeinbucket(self,pt):
        x = min(self.__g-1,int(pt[0]/self.__step))
        y = min(self.__g-1,int(pt[1]/self.__step))
        z = min(self.__g-1,int(pt[2]/self.__step))
        self.__bucketlist[x][y][z].append(pt)      

    def bucketify(self):
        for d in self.__data:
            self.__placeinbucket(d)

        bucket_sort = []
        for x in self.__bucketlist:
            for y in x:
                for z in y:
                    bucket_sort.append((len(z),z))
  
        self.orderedbuckets = sorted(bucket_sort, key=lambda a: a[0])

    def centroid(data):
        print "AHAHAH"

class FileIO:    

    rgb=[]
    hsv=[]
    bins=[]

    def __init__(self, path, resize):
        self.__loadimage(path, resize)
        
    def __loadimage(self, path, resize):
        self.__img = Image.open(path)
        self.__img.thumbnail((resize,resize))
        self.__w, self.__h = self.__img.size
        
        rgb=[]
        for i, c in self.__img.getcolors(self.__w*self.__h):
            rgb += [c]*i

        self.rgb = [(float(x)/255,float(y)/255,float(z)/255) for (x,y,z) in rgb]
        self.hsv = [colorsys.rgb_to_hsv(*c) for c in self.rgb]

class NormalizedClusterEngine:
    data=[]

    # load normalized data
    def loaddata(self, data);
        self.data = data

    # init
    def __init__(self, data):
        self.loaddata(data)

    # voxel subsample clustering (attempt for RGB clustering)
    def voxelcluster(self, n):
        bins = [Bin(index=i, values=[]) for i in range(n*n*n)]
        
        # step one: partition by voxel
        for t in self.data:
            x=int(min(n-1,t[0]/(1.0/n))) # r
            y=int(min(n-1,t[1]/(1.0/n))) # g
            z=int(min(n-1,t[2]/(1.0/n))) # b
            bins[x+n*y+n*n*z].append(t)

        # step two: sort bins by size
        sorted_bins = sorted(bins, reverse=True, key=lambda b: len(b.values))

        # step three: calculate pseudo-centroids
        domcolors=[]
        markers=[False for i in range(n*n*n)]
        changed=True
        radius=1
        while changed:
            changed=False
            for b in sorted_bins:
                if markers[b.index]:
                    continue
                changed=True
                samples=[]

                for x in range(max(0,b.index-radius),min(n,b.index+radius+1)):
                    
                #DLFKSJDFLKJSDLFKJSDLKfJSLKDJFlkj
                for x in range(b.index
                for i in range(b.index-1, b.index+2):
                    markers[i%nbins]=True
                    samples.extend(sortedbins[i%nbins].values)

                h=[]
                s=[]
                v=[]
                for c in samples:
                    h.append(c[0])
                    s.append(c[1])
                    v.append(c[2])

                avg = (numpy.mean(h),numpy.mean(s),numpy.mean(v))
                std = (numpy.std(h),numpy.std(s),numpy.std(v))
                s=Sample(avg=avg,std=std)           
                domcolors.append(s)
                print ":: " + str(s)
          
        # step four: return pseudo-centroids
        return domcolors
         

    # spectral clustering alg (attempt for HSV clustering)
    # ASSUME tuples can be classified by tuple[0]
    # PARTITION tuples into bins by tuple[0]
    # SAMPLE bins w/ local maxima
    def spectralcluster(self, nbins):
        # step one: sort all colors into bins
        bins=[Bin(index=i,values=[]) for i in range(nbins)]
        for t in self.data:
            bins[int(min(nbins-1,t[0]/(1.0/nbins)))].values.append(t)
            
        # step two: sort bins by size
        sortedbins=sorted(bins, reverse=True, key=lambda b: len(b.values))

        # step three: calculate pseudo-centroids
        domcolors=[]
        markers=[False for i in range(nbins)]
        changed=True
        while changed:
            changed=False
            for b in sortedbins:
                if markers[b.index]:
                    continue
                changed=True
                samples=[]
                for i in range(b.index-1, b.index+2):
                    markers[i%nbins]=True
                    samples.extend(sortedbins[i%nbins].values)

                h=[]
                s=[]
                v=[]
                for c in samples:
                    h.append(c[0])
                    s.append(c[1])
                    v.append(c[2])

                avg = (numpy.mean(h),numpy.mean(s),numpy.mean(v))
                std = (numpy.std(h),numpy.std(s),numpy.std(v))
                s=Sample(avg=avg,std=std)           
                domcolors.append(s)
                print ":: " + str(s)
          
        # step four: return pseudo-centroids
        return domcolors
