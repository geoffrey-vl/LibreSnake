import zipfile
import shutil
import os
import sys

tempDirName = "with_macro"
pythonScriptName = "Snake.py"

print("Delete and create directory with_macro")
shutil.rmtree(tempDirName,True)
os.mkdir(tempDirName)

filename = tempDirName+"/"+sys.argv[1]
print("Open file " + sys.argv[1])
shutil.copyfile(sys.argv[1],filename)

doc = zipfile.ZipFile(filename,'a')
doc.write(pythonScriptName, "Scripts/python/"+pythonScriptName)
manifest = []
for line in doc.open('META-INF/manifest.xml'):
  if '</manifest:manifest>' in line.decode('utf-8'):
    for path in ['Scripts/','Scripts/python/','Scripts/python/'+pythonScriptName]:
      manifest.append(' <manifest:file-entry manifest:media-type="application/binary" manifest:full-path="%s"/>' % path)
  manifest.append(line.decode('utf-8'))

doc.writestr('META-INF/manifest.xml', ''.join(manifest))
doc.close()
print("File created: "+filename)