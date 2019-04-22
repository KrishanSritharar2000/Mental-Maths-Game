from PIL import Image
import datetime


##start = datetime.datetime.now()
##image = Image.open('LevelTest2.bmp')
##size = width, height = image.size
##
##print(image.getpixel((570,235)))
##
##sizeW, sizeH = image.size[0], image.size[1]
##print("W",sizeW)#768
##print("H",sizeH)#576
##
##mapData = []
##mapRow = []
##drawn = []
##
##for col in range(sizeH):
##    for row in range(sizeW):
##        pixel = image.getpixel((row, col))
##        mapRow.append(pixel)
##        if pixel == 1:
##            drawn.append((row, col))
##    mapData.append(mapRow)
##    mapRow = []
##    
##end1 = datetime.datetime.now()
##print("Time taken {}".format(end1 - start))
##
##for i in range(len(mapData)):
##    print(mapData[i])
##print(drawn)
##
##end2 = datetime.datetime.now()
##print("Time taken {}".format(end2 - start))

##start = datetime.datetime.now()
##image = Image.open('Track4.bmp')
##size = width, height = image.size
##
##print(image.getpixel((570,235)))
##
##sizeW, sizeH = image.size[0], image.size[1]
##print("W",sizeW)#768
##print("H",sizeH)#576
##
##mapData = []
##mapRow = []
##drawn = []
##
##for col in range(sizeH):
##    for row in range(sizeW):
##        pixel = image.getpixel((row, col))
##        mapRow.append(pixel)
##        if pixel == 1:
##            drawn.append((row, col))
##    mapData.append(mapRow)
##    mapRow = []
##    
##end1 = datetime.datetime.now()
##print("Time taken {}".format(end1 - start))
##
##for i in range(len(mapData)):
##    print(mapData[i])
##print(drawn)
##
##end2 = datetime.datetime.now()
##print("Time taken {}".format(end2 - start))

##start = datetime.datetime.now()
##image = Image.open('BitTest.bmp')
##size = width, height = image.size
##
####print(image.getpixel((570,35)))
##
##sizeW, sizeH = image.size[0], image.size[1]
##print("W",sizeW)#768
##print("H",sizeH)#576
##
##mapData = []
##mapRow = []
##drawn = []
##
##for col in range(sizeH):
##    for row in range(sizeW):
##        pixel = image.getpixel((row, col))
##        mapRow.append(pixel)
##        if pixel == 1:
##            drawn.append((row, col))
##    mapData.append(mapRow)
##    mapRow = []
##    
##end1 = datetime.datetime.now()
##print("Time taken {}".format(end1 - start))
##
##for i in range(len(mapData)):
##    print(mapData[i])
####print(drawn)
##
##end2 = datetime.datetime.now()


start = datetime.datetime.now()
image = Image.open('BitTest2.bmp')
size = width, height = image.size

##print(image.getpixel((570,35)))

sizeW, sizeH = image.size[0], image.size[1]
print("W",sizeW)#768
print("H",sizeH)#576

mapData = []
mapRow = []
drawn = []

for col in range(sizeH):
    for row in range(sizeW):
        pixel = image.getpixel((row, col))
        mapRow.append(pixel)
        if pixel == 12:
            drawn.append((row, col))
    mapData.append(mapRow)
    mapRow = []
    
end1 = datetime.datetime.now()
print("Time taken {}".format(end1 - start))

for i in range(len(mapData)):
    print(mapData[i])
##print(drawn)

end2 = datetime.datetime.now()
