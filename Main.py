
# return img, nested list
def read_ppm_file(f):
    fp = open(f)
    fp.readline()  # reads P3 (assume it is P3 file)
    lst = fp.read().split()
    n = 0
    n_cols = int(lst[n])
    n += 1
    n_rows = int(lst[n])
    n += 1
    max_color_value = int(lst[n])
    n += 1
    img = []
    for r in range(n_rows):
        img_row = []
        for c in range(n_cols):
            pixel_col = []
            for i in range(3):
                pixel_col.append(int(lst[n]))
                n += 1
            img_row.append(pixel_col)
        img.append(img_row)
    fp.close()
    return img, max_color_value


# Works
def img_printer(img):
    row = len(img)
    col = len(img[0])
    cha = len(img[0][0])
    for i in range(row):
        for j in range(col):
            for k in range(cha):
                print(img[i][j][k], end=" ")
            print("\t|", end=" ")
        print()


filename = input()
operation = int(input())


# DO_NOT_EDIT_ANYTHING_ABOVE_THIS_LINE
def operation1(file):
    # This  block takes the required input for operation 1.
    newmin=int(input())
    newmax=int(input())

    for r in file[0]:  # This block iterates through the image and changes each channel with the new calculated value.
        for c in r:
            for i in range(3):
               c[i]=round((((c[i]) / (file[1])) * (newmax - newmin)) + newmin,4)
    img_printer(file[0])


def operation2(file):
    pixels=len(file[0])*len(file[0][0]) # This variable keeps the value of the total pixels, since it is required in the following Deviation and Mean  calculations.
    ChannelValMean=[0,0,0]
    ChannelValDeviation=[0,0,0]

    for i in range(3): # This block iterates through the image and calculates the Mean for each channel.
        for r in file[0]:
            for c in r:
                ChannelValMean[i]+=c[i]/pixels


    for i in range(3): # This block iterates through the image once again and calculates the Deviation for each channel.
        for r in file[0]:
            for c in r:
                ChannelValDeviation[i]+=((c[i]-ChannelValMean[i])**2)/pixels
        ChannelValDeviation[i]=ChannelValDeviation[i]**0.5+10**-6

    for i in range(3): # This block calculates the normalized value and changes the image.
        for r in file[0]:
            for c in r:
                c[i]= round((c[i]-ChannelValMean[i])/(ChannelValDeviation[i]),4)
    img_printer(file[0])






def operation3(file):
    for r in file[0]: # This block iterates through the image and calculates the average value, then modifies the image.
        for c in r:
            rangesum=0
            for i in c:
                rangesum+=i
            average=rangesum/3
            for i in range(3):
                c[i]=int(average)
    img_printer(file[0])




def operation4(file):

    # This block takes the necessary input for operation 4.
    filter=input()
    stride=int(input())

    # This block opens the filter and turns it into a proper list so that it can be used in the further calculations.
    fp=open(filter,"r")
    filterlst=[]
    newimg=[]
    for i in fp:
        filterlst.append(i.split())
    fp.close()

    length=len(filterlst) # This variable keeps the dimensions of the filter.



    for row in range(0,len(file[0]),stride):
        newrow = []

        if row+length> len(file[0]):
            break
        else:
            for col in range(0,len(file[0][row]),stride):
                temp0 = []
                newpixel = []

                if col + length > len(file[0]):
                    break
                else:
                    for r in range(len(filterlst)): # This block applies the filter to the image and appends the results into a temporary list.
                        for c in range(len(filterlst[r])):
                            temp = []
                            for i in range(3):
                                newval = file[0][row+r][col+c][i] * float(filterlst[r][c])
                                temp.append(newval)
                            temp0.append(temp)



                for i in range(3): # This block adds the results in the temporary lists and calculates the values of the new pixel, then creates a new image.
                    val = 0
                    for j in temp0:
                        val += j[i]
                    if val>file[1]:
                        newpixel.append(file[1])
                    elif val<0:
                        newpixel.append(0)
                    else:
                        newpixel.append(int(val))
                newrow.append(newpixel)
            newimg.append(newrow)
    img_printer(newimg)

def operation5(file):

    # This block takes the necessary input for operation 5.
    filter = input()
    stride = int(input())


    pad=[0,0,0]
    row=[]
    newimg=[]

    # This block opens the filter and turns it into a proper list so that it can be used in the further calculations.
    fp = open(filter, "r")
    filterlst = []
    for i in fp:
        filterlst.append(i.split())
    fp.close()
    length = len(filterlst)


    for i in range(len(file[0])):
        row.append(pad)
    for i in range(int((length-1)/2)): # This block does the padding to the top and the bottom row.
        file[0].insert(0,row)
        file[0].append(row)
    for i in file[0]:
        for j in range(int((length-1)/2)): # This block does the padding to the sides.
            i.insert(0,pad)
            i.append(pad)

    for row in range(0,len(file[0]),stride):
        newrow = []

        if row+length> len(file[0]):
            break
        else:
            for col in range(0,len(file[0][row]),stride):
                temp0 = []
                newpixel = []

                if col + length > len(file[0]):
                    break
                else:
                    for r in range(len(filterlst)):
                        for c in range(len(filterlst[r])):
                            temp = []
                            for i in range(3):
                                newval = file[0][row+r][col+c][i] * float(filterlst[r][c])
                                temp.append(newval)
                            temp0.append(temp)



                for i in range(3):
                    val = 0
                    for j in temp0:
                        val += j[i]
                    if val>file[1]:
                        newpixel.append(file[1])
                    elif val<0:
                        newpixel.append(0)
                    else:
                        newpixel.append(int(val))
                newrow.append(newpixel)
            newimg.append(newrow)
    img_printer(newimg)


def quantizer(img, colorrange, prevpixel, coordinates=(0, 0), counter=[]): # This function is the recursive part of the operation 6.
    if coordinates[0]<0 or coordinates[1]<0 or coordinates[1]>=len(img) or coordinates[0]>=len(img): # This base condition makes sure that the function stays within the borders of the image
        return
    if coordinates in counter: # This base condition helps to change each pixel only once.
        return
    counter.append(coordinates) # This line keeps the track of the previously modified pixels.

    # This block changes the each value of the pixel if the pixel is in the required format.
    if -colorrange<img[coordinates[0]][coordinates[1]][0]-prevpixel[0]<colorrange and -colorrange<img[coordinates[0]][coordinates[1]][1]-prevpixel[1]<colorrange and -colorrange<img[coordinates[0]][coordinates[1]][2]-prevpixel[2]<colorrange:
        img[coordinates[0]][coordinates[1]][0]=prevpixel[0]
        img[coordinates[0]][coordinates[1]][1] = prevpixel[1]
        img[coordinates[0]][coordinates[1]][2] = prevpixel[2]

    # This block calls the function recursively to modify each pixel in the image.
    if coordinates[0]<=len(img)-1 and coordinates[1]<=len(img)-1:
        quantizer(img,colorrange,img[coordinates[0]][coordinates[1]],(coordinates[0]+1,coordinates[1]),counter)
        quantizer(img, colorrange, img[coordinates[0]][coordinates[1]], (coordinates[0] - 1, coordinates[1]),counter)
        quantizer(img, colorrange, img[coordinates[0]][coordinates[1]], (coordinates[0], coordinates[1]+1),counter)
        quantizer(img, colorrange, img[coordinates[0]][coordinates[1]], (coordinates[0], coordinates[1]-1),counter)
            

def operation6(file): # Operation 6 takes an input and calls the quantizer function, then prints the modified image.
    colorrange = float(input())
    quantizer(file[0], colorrange,file[0][0][0],(0,0))
    img_printer(file[0])

def quantizer2(img, colorrange, prevch, coordinates=(0, 0, 0), counter=[]): # This function is the recursive part of the operation 7.

    # This base condition makes sure that the function stays within the borders of the image
    if coordinates[0]<0 or coordinates[1]<0 or coordinates[1]>=len(img) or coordinates[0]>=len(img) or coordinates[2]>=3 or coordinates[2]<0:
        return

    # This base condition helps to change each channel only once.
    if coordinates in counter:
        return
    counter.append(coordinates) # This line keeps the track of the previously modified pixels.
    if -colorrange<img[coordinates[0]][coordinates[1]][coordinates[2]]-prevch<colorrange: # This block changes the each channel if the pixel is in the required format
        img[coordinates[0]][coordinates[1]][coordinates[2]]=prevch

    # This block calls the function recursively to modify each pixel in the image.
    if coordinates[0]<=len(img)-1 and coordinates[1]<=len(img)-1 and coordinates[2]<=2:
        quantizer2(img,colorrange,img[coordinates[0]][coordinates[1]][coordinates[2]],(coordinates[0]+1,coordinates[1],coordinates[2]),counter)
        quantizer2(img, colorrange, img[coordinates[0]][coordinates[1]][coordinates[2]], (coordinates[0] - 1, coordinates[1],coordinates[2]),counter)
        quantizer2(img, colorrange, img[coordinates[0]][coordinates[1]][coordinates[2]], (coordinates[0], coordinates[1]+1,coordinates[2]),counter)
        quantizer2(img, colorrange, img[coordinates[0]][coordinates[1]][coordinates[2]], (coordinates[0], coordinates[1]-1,coordinates[2]),counter)
        quantizer2(img, colorrange, img[coordinates[0]][coordinates[1]][coordinates[2]],(coordinates[0], coordinates[1] , coordinates[2]+1), counter)
        quantizer2(img, colorrange, img[coordinates[0]][coordinates[1]][coordinates[2]],(coordinates[0], coordinates[1] - 1, coordinates[2]-1), counter)

def operation7(file):   # Operation 7 takes an input and calls the quantizer2 function, then prints the modified image.
    colorrange=float(input())
    quantizer2(file[0],colorrange,file[0][0][0][0],(0,0,0))
    img_printer(file[0])


# This block stores the functions in the dictionary so that they can be called via input.
operations = {1:operation1,2:operation2,3:operation3,4:operation4,5:operation5,6:operation6,7:operation7}
operations.get(operation)(read_ppm_file(filename))


# DO_NOT_EDIT_ANYTHING_BELOW_THIS_LINE

