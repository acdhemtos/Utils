import asyncio
import os
import shutil
import filecmp

p = dict()
raw = "./RAW"
renamed = "./TIMELAPSE"

if not os.path.isdir(raw):
  print("Source Error")
  exit()

if os.path.isdir(renamed) and os.listdir(renamed):
  print("Destination Error")
  exit()

async def get_file_date(file):
 base_command = [
  r"C:\ExifTool\exiftool.exe",
  "-d", "%Y%m%d%H%M%S",
  "-s", "-s", "-s"
 ]

 for tag in ["-CreateDate", "-MediaCreateDate"]:
  command = base_command + [tag, file]
  process = await asyncio.create_subprocess_exec(
   *command,
   stdout=asyncio.subprocess.PIPE,
   stderr=asyncio.subprocess.PIPE
  )
  stdout, stderr = await process.communicate()
  date_str = stdout.decode().strip()
  if date_str:
   return date_str

 return False

async def process(path):
 if os.path.isdir(path):
  tasks = [process(path+'/'+file) for file in os.listdir(path)]
  await asyncio.gather(*tasks)
  return
 time = await get_file_date(path)
 if time is not False:
  path = path[len(raw)+1:]
  ext = path.split(".")[-1]
  newName = " - ".join([time] + path.split("/")[:-1][::-1])+ "." + ext
  if newName not in p:
   p[newName] = []
  p[newName].append(path)

asyncio.run(process(raw))

def rename(path,new):
 src = raw+"/"+path
 dst = renamed+"/"+new

 os.makedirs(os.path.dirname(dst), exist_ok=True)

 shutil.move(src, dst)

k = list(p.keys())
k.sort()

while k:
 name = k.pop(0)
 file_paths = p.pop(name)
 file_paths.sort()
 unique_files = []
 
 while file_paths:
  current = file_paths[0]
  unique_files.append(current)
  rest = []
  for other in file_paths[1:]:
   if filecmp.cmp(raw+"/"+current,raw+"/"+other,shallow=False):
    os.remove(raw+"/"+other)
   else:
    rest.append(other)
  file_paths = rest
  del rest
 file_paths = unique_files
 del unique_files
 
 l = len(file_paths)
 
 if l==1:
  rename(file_paths[0],name)
  continue
 
 d = 0
 while l>1:
  d += 1
  l /= 10
 
 print(name,file_paths)
 
 for i in range(len(file_paths)):
  ns = name.partition(".")
  rename(file_paths[i],ns[0] + " - " + str(i).zfill(d) + '.' + ns[2])

del p,k,raw,renamed
