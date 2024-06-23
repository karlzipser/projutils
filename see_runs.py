
## 79 ########################################################################

#,a
ignore_list = ['env']
extensions = ['.txt','.pdf','.py','.pkl','.pth','.html']+IMAGE_EXTENSIONS
fdic={}
def bytes_to_mb(bytes):
  return bytes / (1024 ** 2)


def time_sleep(seconds):
    start_time = time.time()
    while time.time() - start_time < seconds:
        pass

def see(ctr_or_ctr_list,fdic=fdic):
    if type(ctr_or_ctr_list)==tuple:
        ctr_or_ctr_list=list(ctr_or_ctr_list)
    if type(ctr_or_ctr_list) == list:
        ctr=ctr_or_ctr_list.pop()
    else:
        ctr=ctr_or_ctr_list
    f=fdic[ctr]['f']
    html=most_recent_file_in_folder(f,'.html')
    print(html)
    time_sleep(0.3)
    open_url(html)
    if type(ctr_or_ctr_list) == list:
        if len(ctr_or_ctr_list):
            see(ctr_or_ctr_list,fdic=fdic)

def trash(ctr):
  f=fdic[ctr]['f']
  trash=opj(pname(f),'_Trash')
  mkdirp(trash)
  os_system('mv',f,trash)

def summarize_run(src,min_duration):
    files = []
    for extension in extensions:
      files.extend(glob.glob(os.path.join(src, '**', '*' + extension), recursive=True))

    filtered_files = [f for f in files if not any(ignore in f for ignore in ignore_list)]

    file_info = {}
    for file in filtered_files:
      file_info[file] = (os.path.getsize(file), os.path.getctime(file))

    extension_counts = {}
    earliest_time=2*time.time()
    latest_time=-1
    for file, (size, t) in file_info.items():
      if t<earliest_time:
        earliest_time=t
      if t>latest_time:
        latest_time=t
      extension = file.split('.')[-1]
      extension_counts.setdefault(extension, {'total_size': 0, 'count': 0})
      extension_counts[extension]['total_size'] += size
      extension_counts[extension]['count'] += 1
    #if 'html' not in extension_counts:
    #    return None
    duration=latest_time-earliest_time
    if duration<min_duration:
        return None
    s=[src]
    for extension, counts in extension_counts.items():
        s.append(d2n(
            extension,':',counts['count'],'/',dp(bytes_to_mb(counts['total_size']),2)
        ))
    s.append(d2n(int(duration),'s'))
    s=' '.join(s)
    return s

def trash_no_html():
  for ctr in fdic:
    d=fdic[ctr]
    if 'html' not in d['s']:
      print('trashing',d['f'],'because it has no .html file')
      trash(ctr)



def dir(src='project_tac_ideal',min_t=1):
  min_duration=min_t
  fs=sggo(src+'/*')
  ctr=0
  for f in fs:
      if '_' == fname(f)[0]:
        continue
      s=summarize_run(f,min_duration)
      if isNone(s):
          continue
      print(ctr,s)
      fdic[ctr]=dict(s=s,f=f)
      ctr+=1

#,b
#EOF