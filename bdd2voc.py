import os
import pascal_voc_io
import parseJson

dirName = "labels"
i = 1
for dirpath,dirnames,filenames in os.walk(dirName):
  
  for filepath in filenames:
    fileName = os.path.join(dirpath,filepath)
    print("processing: ",i)
    
    i = i + 1
    xmlFileName = filepath[:-5]
    #print("xml: ",xmlFileName)
    print(fileName)
    objs = parseJson.parseJson(str(fileName))
    if len(objs):
        tmp = pascal_voc_io.PascalVocWriter('Annotations',xmlFileName, (720,1280,3))
        for obj in objs:
            tmp.addBndBox(obj[0],obj[1],obj[2],obj[3],obj[4])
        tmp.save()
    else:
        print(fileName)
