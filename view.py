## 79 ########################################################################

#print(__file__)
from utilz2 import *


def merge_content(
  w=opjh('snippets/working'),
  show=True,
  default_height=120,
):

  from pygments import highlight
  from pygments.lexers import PythonLexer
  from pygments.formatters import HtmlFormatter
  css='\n'.join([
      '<head><style>',
      HtmlFormatter().get_style_defs('.highlight'),
      '</style></head>',
      ' '
  ])
  mkdirp_(w)
  fs=find_files(w,['*.py','*.pdf','*.txt'],noisy=False)
  fs = sorted(fs, key=get_file_mtime)
  fs.reverse()
  hs=[]
  for f in fs:
    #cg(f)
    if '/env/' in f:
      continue
    div=''
    con=False
    for f_ in f.split('/'):
      if len(f_) and f_[0]=='_':
        con=True
    if con:
      continue
    dims=parse_dimensions(f)
    if not isNone(dims):
      height=dims[0]
      width=dims[1]
    else:
      height=0
      width=height
    if '.pdf' in f:
      if not height:
        height=512
        width=height
      div="""
<div>
<object data="PDFFILE"
      type="application/pdf"
      width="512"
      height="512">
</object>
</div>
          """.replace(
              'PDFFILE',opjh(f))
              #f.replace(w+'/','')).replace(
              #  'HEIGHT',str(height)).replace(
              #    'WIDTH',str(width))
      #cb(div)
    else:
      txt=file_to_text(f)
      txt=d2n('file: ',qtds(f.replace(w,'')[1:]),'\n',txt)
      if txt:
        if '.txt' in f:
          div=d2n(
            '<div style="white-space: pre-line;">',
            '<font face="Courier">',
            txt,
            '</font>',
            '</div>',
          )
        else:
          div=highlight(txt,PythonLexer(),HtmlFormatter())
        div='\n'.join([
              """<div style="height:HEIGHTpx;border:1px solid ;overflow:auto;">""",
              div,
              '</div>\n',
          ])
    if not height:
      height=default_height
    div=div.replace('HEIGHT',str(height))
    if 'application/pdf' in div:
        pass#cy(div)
    if div:
      hs.append(div)
  hs=[css]+[d2n('<font face="Courier"><h1>',w.replace(opjh(),''),
    '</h1></font>')]+hs
  htmlfile=opj(w,'_'+'merge.html')
  text_to_file(
    htmlfile,
    '\n'.join(hs)
  )
  open_url(htmlfile)



if __name__ == '__main__':
    args=dict(
        src='',
        most_recent=1,
        repeat=30,
    )
    p=getparser(**args)
    assert ope(p.src)
    if p.most_recent:
      p.src=most_recent_file_in_folder(p.src)
    while True:
      merge_content(w=p.src,default_height=u2.sn.default_height)
      if not p.repeat:
        break
      else:
        time.sleep(p.repeat)

#EOF
