## 79 ########################################################################

#print(__file__)
from utilz2 import *


def merge_content(
<<<<<<< HEAD
  w=opjh('snippets/working'),
  show=True,
  default_height=120,
):
  """
  exec(gcsp(opjh('utilz2'),include_output=1));merge_snippets();CA()
  u2.sn.src=opjh('utilz2')
  u2.sn.dst=opjh('snippets/working')
  exec(gcsp(u2.spath,include_output=1));merge_snippets();CA()
  """
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
=======
    w=opjh('project_tac'),
    most_recent=1,
    show=True,
    default_height=120,
):
    if most_recent:
        w=most_recent_file_in_folder(w)
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
>>>>>>> 58a838b0684cac62cfa00b8301bd5c33edbc075f
<div>
<object data="PDFFILE"
      type="application/pdf"
      width="WIDTH"
      height="HEIGHT">
      <!--alt : <a href="test.pdf">test.pdf</a>-->
</object>
</div>
          """.replace(
            'PDFFILE',
            f.replace(w+'/','')).replace('HEIGHT',
              str(height)).replace('WIDTH',
              str(width)
            )
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

<<<<<<< HEAD
#EOF
## 79 ########################################################################
=======


if __name__ == '__main__':
    args=dict(
        src='',
        most_recent=1,
    )
    p=getparser(**args)
    assert ope(p.src)
    merge_content(w=p.src,most_recent=p.most_recent,default_height=u2.sn.default_height)


#EOF
>>>>>>> 58a838b0684cac62cfa00b8301bd5c33edbc075f
