## 79 ########################################################################

print(__file__)
from utilz2 import *
#from .view import *

"""
e.g.,
    python3 projutils/project.py --src tac --tag Sat2 --termout 1
"""

<<<<<<< HEAD
def run_project(src,repos=[opjh('projutils')]):
  name=fname(src)
  s=time_str()
  if p.tag:
    s+='-'+get_safe_name(p.tag)
  dst=opjh('project_'+name,s)
  mkdirp(dst)
  os_system('rsync -ravL',src,dst,e=1,a=1)
  for d in ['env','figures','net/weights','stats']:
    mkdirp(opj(dst,name,d))
  for d in repos:
    os_system('rsync -ravL',d,opj(dst,name,'env'),e=1,a=1)

  m=most_recent_file_in_folder(opjh('project_'+name)).replace(opjh(),'')
  cg(m)
  o=opj(m,name,'stats/out.txt')
  cb(o)
  m=d2p(m.replace('/','.'),name,'code.main')
  cy(m)
  os_system('python3 -m',m,' > ',o,e=1)

if __name__ == '__main__':
  args=dict(
    src='',
    tag='',
    termout=1,
  )
  p=getparser(**args)
  assert ope(p.src)
  run_project(p.src)
=======
def run_project(src,repos=[opjh('projutils')],termout=1):
    name=fname(src)
    s=time_str()
    if p.tag:
        s+='-'+get_safe_name(p.tag)
    dst=opjh('project_'+name,s)
    mkdirp(dst)
    os_system('rsync -ravL',"--exclude '*.pyc'","--exclude '.git*'",src,dst,e=1,a=1)
    for d in ['env','figures','net/weights','stats']:
        mkdirp(opj(dst,name,d))
    for d in repos:
        os_system('rsync -ravL',"--exclude '*.pyc'","--exclude '.git*'",d,opj(dst,name,'env'),e=1,a=1)

    m=most_recent_file_in_folder(opjh('project_'+name)).replace(opjh(),'')
    cg(m)
    o=opj(m,name,'stats/out.txt')
    cb(o)
    m=d2p(m.replace('/','.'),name,'code.main')
    cy(m)
    s=d2s('python3 -m',m)
    if not p.termout:
        s=d2s(s,'>',o)
    os_system(s,e=1)

if __name__ == '__main__':
    args=dict(
        src='',
        tag='',
        termout=1,
    )
    p=getparser(**args)
    assert ope(p.src)
    run_project(p.src,termout=p.termout)

>>>>>>> 58a838b0684cac62cfa00b8301bd5c33edbc075f

#EOF
## 79 ########################################################################
