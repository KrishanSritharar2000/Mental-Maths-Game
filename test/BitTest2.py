from PIL import Image
import datetime
start = datetime.datetime.now()

bmpImage = Image.open('BitMapMono.bmp', 'r')
pixelValue = list(bmpImage.getdata())
print(pixelValue)

sizeWidth = bmpImage.size[0]
sizeHeight = bmpImage.size[1]

mapData = []
mapRow = []
blackPixel  = []

for col in range(sizeHeight):
    for row in range(sizeWidth):
        pixel = bmpImage.getpixel((row, col))
        mapRow.append(pixel)
        if pixel == 1:
            blackPixel.append((row, col))
    mapData.append(mapRow)
    mapRow = []

end1 = datetime.datetime.now()
print("Time taken {}".format(end1 - start))

for i in range(len(mapData)):
    print(mapData[i])
print(blackPixel)


end2 = datetime.datetime.now()
print("Time taken {}".format(end2 - start))
