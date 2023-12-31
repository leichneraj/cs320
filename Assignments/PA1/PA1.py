import math
import numpy as np
import argparse

# begin PROVIDED section - do NOT modify ##################################

count = 0

def getArgs() :
    
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type = str, help = 'File containing terrain')
    
    parser.add_argument('h', type = float, help = 'h value')
    
    parser.add_argument('theta', type = float, help = 'Angle of elevation for Sun')
    parser.add_argument('algorithm', type = str, help = 'naive | early | fast')
    return parser.parse_args()

def compare(x,y):
    global count
    count += 1
    if abs(x-y) < .000000000001 :
        return False
    if x < y :
        return True
    else:
        return False

def print_shade(boolean_array):
    for row in boolean_array:
        for column in row:
            if column == True:
                print ('*    ', end = '')
            elif column == False:
                print ('0    ', end = '')
        print('\n')
        
def read2Dfloat(fileName) : # read CSV of floats into 2D array
    array2D = []
    # Read input file
    f = open(fileName, "r")
    data = f.read().split('\n')
    
    # Get 2-D array
    for row in data:
        if row=='':
            continue
        float_list = list(map(float, row.split(',')[0:-1]))
        array2D.append(float_list)

    return array2D

def runTest(args, terrain = None) :

    
    # Initialize counter
    global count
    count = 0

    theta = np.deg2rad(args.theta)
    
    if terrain == None :
      terrain = read2Dfloat(args.input_file)

    N     = len(terrain)
    shade = [[False] * N for i in range(N)]

    if args.algorithm == 'naive':
        result = naive(terrain, args.h, theta, N, shade)
    elif args.algorithm == 'early':
        result = earlyexit(terrain, args.h, theta, N, shade)
    elif args.algorithm == 'fast':
        result = fast(terrain, args.h, theta, N, shade)

    return result

# end PROVIDED section ##################################

# Fritz Sieker 

def naive(image,h,angle,N,shade):
    tangentAngle = math.tan(angle)
    for i in range(N) :
        R = image[i]
        for j in range (N) :
            for k in range (j) :
                temp = compare(tangentAngle, (R[k] - R[j]) / (h * (j - k)))
                if shade[i][j] == False :
                    shade[i][j] = temp
    
###### Complete this function

    return shade

def earlyexit(image,h,angle, N, shade):
    tangentAngle = math.tan(angle)
    for i in range(N) :
        R = image[i]
        for j in range (N) :
            for k in range (j) :
                if(compare(tangentAngle, (R[k] - R[j]) / (h * (j - k)))) :
                    shade[i][j] = True
                    break
###### Complete this function

    return shade

def fast(image,h,angle, N, shade):
    tangentAngle = math.tan(angle)
    for i in range(N) :
        R = image[i]
        maxVal = R[0]
        maxValIndex = 0
        for j in range (N) :
            if compare((R[j] + h * j * tangentAngle), (maxVal + h * maxValIndex * tangentAngle)) :
                shade[i][j] = True
            else :
                maxVal = R[j]
                maxValIndex = j
        # j is sunny if for every k: 0 less than or equal to k less than j
        # (R[j] + h * j * tangentAngle) greater than or equal to (max[0 less than or rqual to k  less than j] + h * k * tangentAngle)
            
###### Complete this function
    
    return shade
    
if __name__ == '__main__':
    

    answer = runTest(getArgs())
    print_shade(answer)
    print('Number of comparisons: ' + str(count))