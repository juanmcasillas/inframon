##!/usr/bin/env bash
# -*- coding: utf-8 -*-
# /////////////////////////////////////////////////////////////////////////////
# //
# // helpers.py 
# //
# // 
# //
# // 19/11/2024 09:46:13  
# // (c) 2024 Juan M. Casillas <juanm.casillas@gmail.com>
# //
# /////////////////////////////////////////////////////////////////////////////

import unicodedata

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii.decode('utf-8')


# import math
# import os
# import glob
# import hashlib
# import shutil
# import re
# import os
# import time
# import datetime
# import json
# import decimal
# import unicodedata
# from decimal import *

# class C:
#     def __init__(self, **kargs):
#         for i in kargs:
#             self.__setattr__(i, kargs[i])

#     def __str__(self):
#         s= ""
#         for i in self.__dict__.keys():
#             s += "<%s: %s>, " % (i, self.__dict__[i])
#         return s
    
#     def __iter__(self):
#         for attr, value in self.__dict__.items():
#             if isinstance(value, datetime.datetime):
#                 iso = value.isoformat()
#                 yield attr, iso
#             elif isinstance(value, decimal.Decimal):
#                 yield attr, str(value)
#             elif isinstance(value, C):
#                 yield attr, dict(value)
#             elif(hasattr(value, '__iter__')):
#                 if(hasattr(value, 'pop')):
#                     a = []
#                     for subval in value:
#                         if(hasattr(subval, '__iter__')):
#                             print(subval)
#                             a.append(dict(subval))
#                         else:
#                             a.append(subval)
#                     yield attr, a
#                 else:
#                     yield attr, value
#             else:
#                 yield attr, value

#     def json(self):
#         return json.dumps(dict(self))


# class CacheManager:
#     def __init__(self, cachedir):
#         self.cachedir = cachedir

#     def store(self, fname, force=False):
#         if not os.path.exists(fname) or not os.path.isfile(fname):
#             raise FileExistsError("file %s doesn't exists" % fname)

#         tgt = self.map_object(fname)
#         if not force:
#             if os.path.exists(tgt):
#                 return None

#         # default: store file in the cache directory
#         try:
#             os.makedirs(os.path.dirname(tgt),exist_ok=True)
#             shutil.copyfile(fname, tgt)
#         except Exception as e:
#             raise IOError("can't store %s in cache" % fname)
        
#         return tgt


#     def retrieve(self, fname):
#         "if not found on cache, store it and retrieve"
#         tgt = self.map_object(fname)
#         if not os.path.exists(tgt):
#             tgt = self.store(fname)
        
#         return tgt
        
#     def remove(self, fname):
#         tgt = self.map_object(fname)
#         if os.path.exists(tgt):
#             try:
#                 os.remove(tgt)
#             except Exception as e:
#                 raise IOError("Can't delete file from cache%s" % fname)
#             return True
#         return False
    

#     def map_object(self, fpath, create_dirs=False, relative=False):
#         fid = hashlib.md5(str(fpath).encode('utf-8')).hexdigest()
#         tgt = os.sep.join([self.cachedir, fid[0:2].upper(), fid[2:4].upper(),fid])
#         if create_dirs:
#             d = os.path.dirname(tgt)
#             os.makedirs(d,exist_ok=True)
#         if relative:
#             # remove the cache directory, return only the relative one.
#             tgt = os.sep.join([fid[0:2].upper(), fid[2:4].upper(),fid])
#         return tgt

# # def test_cache():
# #     cm = CacheManager("cache")
# #     print("hola")
# #     print(cm.retrieve("file.txt"))



# def point_inside_polygon(point,poly):

#     getcontext().prec = 6

#     x = Decimal(point.longitude)
#     y = Decimal(point.latitude)

#     # check if point is a vertex
#     #if (x,y) in poly: return True
#     for p in poly:
#         px = Decimal(p[0])
#         py = Decimal(p[1])
#         if x == px and y == py:
#             return True

#     # check if point is on a boundary
#     for i in range(len(poly)):
#         p1 = None
#         p2 = None
#         if i==0:
#             p1 = poly[0]
#             p2 = poly[1]
#         else:
#             p1 = poly[i-1]
#             p2 = poly[i]
#         if Decimal(p1[1]) == Decimal(p2[1]) and Decimal(p1[1]) == y and x > min(Decimal(p1[0]), Decimal(p2[0])) and x < max(Decimal(p1[0]), Decimal(p2[0])):
#             return True

#     n = len(poly)
#     inside = False

#     p1x,p1y,d= poly[0]

#     p1x = Decimal(p1x)
#     p1y = Decimal(p1y)

#     for i in range(n+1):
#         p2x,p2y,d = poly[i % n]

#         p2x = Decimal(p2x)
#         p2y = Decimal(p2y)

#         if y > min(p1y,p2y):
#             if y <= max(p1y,p2y):
#                 if x <= max(p1x,p2x):
#                     if p1y != p2y:
#                         xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
#                     if p1x == p2x or x <= xints:
#                         inside = not inside
#         p1x,p1y = p2x,p2y


#     return inside



        

# def  glob_filelist(files):
#     found_files = []
#     # ('./**/'): .\app.py import_files .\data\Cartography\**\*.gpx
#     for fname in files:
#         for f in glob.glob(fname, recursive=True):
#             if f not in found_files:
#                 found_files.append(f)
#         # if fname is a real file, and not in found file, add it, also.
#         if os.path.exists(fname) and os.path.isfile(fname) and not fname in found_files:
#             found_files.append(fname)
#     return found_files


# def manhattan_distance(a,b):
#     # Σ|Ai – Bi|
#     return sum(abs(val1-val2) for val1, val2 in zip(a,b))

# def manhattan_point(p1,p2):
#     a = [p1.latitude, p1.longitude, p1.elevation]
#     b = [p2.latitude, p2.longitude, p2.elevation]
#     return sum(abs(val1-val2) for val1, val2 in zip(a,b))


# def module(vector):
#     return math.sqrt(sum(v**2 for v in vector))

# def add_similarity_helpers(track, radius=0.001):
#     track._trk_ls = LineString([[p.latitude,p.longitude] for p in track.points])
#     track._trk_buff = track._trk_ls.buffer(radius)

# def del_similarity_helpers(track, radius=0.001):
#     del track._trk_ls
#     del track._trk_buff


# def same_track(trk1, trk2, radius=0.001, debug=False, use_cache=False):
#     # https://gis.stackexchange.com/questions/81551/matching-gps-tracks

#     if use_cache:
#         print("before")
#         match1=trk2._trk_buff.intersection(trk1._trk_ls).buffer(radius)
#         print("match1",  len(trk1._trk_buff.coords ))
#         match2=trk1._trk_buff.intersection(trk2._trk_ls).buffer(radius)
#         print("match2",  len(trk2._trk_buff.coords ))
#         match=match1.intersection(match2)
#         print("intersection")

#         if debug:
#             fig=plt.figure()
#             ax = fig.add_subplot(111)
#             x,y=trk1._trk_ls.xy
#             ax.plot(x,y,'b.')
#             x,y=trk2._trk_ls.xy
#             ax.plot(x,y,'g.')
#             fig.savefig("same_track_cache.png")

#         if match.is_empty:
#             ret = False
#         else:
#             mb = match.buffer(radius)
#             print("contains-before")
#             ret = mb.contains(trk1._trk_ls) and mb.contains(trk2._trk_ls)
#             print("contains-after")
#         return ret
    
#     # standard version (calculated each time)
#     track1=LineString([[p.latitude,p.longitude] for p in trk1.points])
#     track2=LineString([[p.latitude,p.longitude] for p in trk2.points])
    
#     # track1_buffered=track1.buffer(BUFFER_SZ)
#     # fig=plt.figure()
#     # ax = fig.add_subplot(111)
#     # # fix descartes patch
#     # https://stackoverflow.com/questions/75287534/indexerror-descartes-polygonpatch-wtih-shapely
#     # patch.py:62 fix
#     # vertices = concatenate([
#     #    concatenate([asarray(t.exterior.coords)[:, :2]] +
#     #                [asarray(r.coords)[:, :2] for r in t.interiors])
#     #    for t in polygon])
#     # patch.py:46            polygon = [Polygon(p) for p in list(polygon.geoms)]

#     if debug:
#         fig=plt.figure()
#         ax = fig.add_subplot(111)
#         x,y=track1.xy
#         ax.plot(x,y,'b.')
#         x,y=track2.xy
#         ax.plot(x,y,'g.')
#         fig.savefig("same_track.png")

#     match1=track2.buffer(radius).intersection(track1).buffer(radius)
#     match2=track1.buffer(radius).intersection(track2).buffer(radius)
#     match=match1.intersection(match2)
    
#     if match.is_empty:
#         ret = False
#     else:
#         ret = match.buffer(radius).contains(track1) and match.buffer(radius).contains(track2)
    
#     del match1
#     del match2
#     del match
#     del track1
#     del track2 
#     return ret 


# def track_similarity(trk1, trk2):
#     # iterate the track with less points, and calculate
#     # the sum of the manhattan_distance between points.
#     len_1 = len(trk1.points)
#     len_2 = len(trk2.points)

#     if len_1 != len_2:
#         if len_2 > len_1:
#             diff = len_2 - len_1
#             trk1.points += [gpxpy.gpx.GPXTrackPoint(latitude=0.0,longitude=0.0,elevation=0.0)] *diff
#         else:
#             diff = len_1 - len_2
#             trk2.points += [gpxpy.gpx.GPXTrackPoint(latitude=0.0,longitude=0.0,elevation=0.0)] *diff


#     similarity = 0.0
#     for i in range(0,len_1):
#         similarity += manhattan_point(trk1.points[i], trk2.points[i])

#     return similarity



# def set_proxy(proxy_url):
#     "proxy = 'http://<user>:<pass>@<proxy>:<port>'"
#     os.environ['http_proxy']  = proxy_url 
#     os.environ['HTTP_PROXY']  = proxy_url
#     os.environ['https_proxy'] = proxy_url
#     os.environ['HTTPS_PROXY'] = proxy_url    


# def max_min_avg_from_list(l):
#     max_value = 0
#     min_value = 0
#     avg_value = 0
#     if len(l) > 0:
#         max_value = max(l)
#         min_value = min(l)
#         avg_value = 0 if len(l) == 0 else float(sum(l))/len(l)
#     return (max_value, min_value, avg_value)

# def is_nan(x):
#     return (x != x) or x is None

# def get_fval(x, v=0.0):
#     return  x if not is_nan(x) else v

# def time_str(seconds):
#         m, s = divmod(seconds, 60)
#         h, m = divmod(m, 60)
#         return "%02d:%02d:%02d" % (h, m, s)

# def next_odd_floor(x):
    
#     i = int(x)
#     while i>0:
#         if i % 2 != 0:
#             return i
#         i = i-1
    
#     return x

# def bearing(A, B):
#     return gpxpy.geo.get_course(A.latitude, A.longitude, 
#                                 B.latitude, B.longitude, 
#                                 loxodromic=True)

# def distancePoints(A, B):
#     return gpxpy.geo.distance( A.latitude, A.longitude, A.elevation,
#                                B.latitude, B.longitude, B.elevation,
#                                haversine=False )
    
# def distancePoints3D(A, B):
#     return gpxpy.geo.distance( A.latitude, A.longitude, A.elevation,
#                                B.latitude, B.longitude, B.elevation,
#                                haversine=True )

# def gradeslope(distance, elevation):
    
#     if distance == 0.0 or elevation == 0.0: 
#         return 0.0
    
#     r = math.pow(distance, 2) - math.pow(elevation, 2)

#     d = distance    
#     if r > 0.0: 
#         d = math.sqrt( r )
        
#     s = (elevation / d) * 100.0             # projected distance (horizontal)
#     s = (elevation / distance) * 100.0      # aproximation
    
#     #print("distance: %3.2f elevation: %3.2f d: %3.2f s: %3.2f " % (distance,elevation,d, s))
#     return s

# def guess_clockwise(gpx_points, p_center):
    
#     a = gpx_points[0]
#     b = gpx_points[int(len(gpx_points)/6)]
    
#     a_b = bearing(p_center,a) 
#     b_b = bearing(p_center,b) 
    
#     # convert from compass to algebra.
    
#     a_b = (a_b-90) % 360
#     b_b = (b_b-90) % 360 
     
#     a_d = distancePoints(p_center, a)
#     b_d = distancePoints(p_center, b)
    
#     A = ( a_d * math.cos(math.radians(a_b)), a_d * math.sin(math.radians(a_b)) )
#     B = ( b_d * math.cos(math.radians(b_b)), b_d * math.sin(math.radians(b_b)) )
    
#     MA =  math.sqrt( math.pow(A[0],2) + math.pow(A[1],2) )

#     AX = (A[0]*B[1]) - (A[1]*B[0])
#     M_AX = (AX / (2 * MA ))
    

#     if M_AX >= 0:
#         #if DEBUG: print "->"
#         return True
    
#     #if DEBUG: print "<-"
#     return False


# def savitzky_golay(y, window_size, order, deriv=0, rate=1):

#     import numpy as np
#     from math import factorial

#     try:
#         window_size = np.abs(int(window_size))
#         order = np.abs(int(order))
#     except ValueError as e:
#         raise ValueError("window_size and order have to be of type int")
#     if window_size % 2 != 1 or window_size < 1:
#         raise TypeError("window_size size must be a positive odd number")
#     if window_size < order + 2:
#         raise TypeError("window_size is too small for the polynomials order")
#     order_range = range(order+1)
#     half_window = (window_size -1) // 2
#     # precompute coefficients
#     b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
#     m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
#     # pad the signal at the extremes with
#     # values taken from the signal itself
#     firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
#     lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
#     y = np.concatenate((firstvals, y, lastvals))
#     return np.convolve( m[::-1], y, mode='valid')

# if __name__ == "__main__":
#     #test_cache()
#     # a = C()
#     # a.name = "name_value"
#     # a.data = C()
#     # a.data.subname = "subname_value"
#     # print(a.json())
#     pass