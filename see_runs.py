
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


def star(ctr):
    f=fdic[ctr]['f']
    os_system('touch',opj(f,'star-'+time_str()+'.txt'))


def comment(ctr):
    f=fdic[ctr]['f']
    s=input(d2n('Enter comment on',f,'> '))
    t2f(opj(f,'comment-'+time_str()+'.txt'),s)


def see(ctr):
    f=fdic[ctr]['f']
    html=most_recent_file_in_folder(f,'.html')
    print(html)
    time_sleep(0.3)
    open_url(html)


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
    for f in filtered_files:
      file_info[f] = dict(
          size=os.path.getsize(f),
          t=os.path.getctime(f),
        )
    stars=0
    comments=[]
    for f in filtered_files:
      #cm(f)
      if 'star' in f:
        stars+=1
      if 'comment' in f:
        comments.append(f2t(f))
    extension_counts = {}
    earliest_time=2*time.time()
    latest_time=-1
    for f in file_info:
      size, t = file_info[f]['size'],file_info[f]['t']
      if t<earliest_time:
        earliest_time=t
      if t>latest_time:
        latest_time=t
      extension = f.split('.')[-1]
      extension_counts.setdefault(extension, {'total_size': 0, 'count': 0})
      extension_counts[extension]['total_size'] += size
      extension_counts[extension]['count'] += 1
    duration=latest_time-earliest_time
    if duration<min_duration:
        return None
    s=[stars*'*',src.replace(pname(src),'')[1:]]
    for extension, counts in extension_counts.items():
        s.append(d2n(
            extension,':',counts['count'],'/',dp(bytes_to_mb(counts['total_size']),2)
        ))
    s.append(d2n(int(duration),'s'))
    if comments:
      s.append(d2n('\n\t-'+'\n\t-'.join(comments)))
    s=' '.join(s)
    return s


def trash_no_html():
  for ctr in fdic:
    d=fdic[ctr]
    if 'html' not in d['s']:
      print('trashing',d['f'],'because it has no .html file')
      trash(ctr)


def dir(min_t=1):
  ps=sggo(opjh('project_*'))
  src=select_from_list(ps)
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