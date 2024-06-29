#!/usr/bin/env python3
## 79 ########################################################################

#print(__file__)
from utilz2 import *


def merge_content(
  w=opjh('snippets/working'),
  show=True,
  default_height=120,
  newtab=True,
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
  fs=find_files(w,['*.py','*.pdf','*.txt','*.png'],noisy=False)
  fs = sorted(fs, key=get_file_mtime)
  fs.reverse()
  
  tabdic=dict(
      py=[],
      confusion=[],
      scores=[],
      accuracy=[],
      txt=[],
      loss=[],
      examples=[],
      outputs=[],
    )
  for f in fs:
    #cg(f)
    if '/env/' in f:
      continue
    if 'star-' in f:
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
      k='pdf'
      if not height:
        height=256
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
              'PDFFILE',f.replace(w,'')[1:])

    elif '.png' in f:
      k='png'
      if not height:
        height=256
        width=height
      div="""
<div>
<img src="FILE">
</div>
          """.replace(
              'FILE',f.replace(w,'')[1:])
    else:
      txt=file_to_text(f)
      txt=d2n('file: ',qtds(f.replace(w,'')[1:]),'\n',txt)
      if txt:

        if '.txt' in f:
          k='txt'
          div=d2n(
            '<div style="white-space: pre-line;">',
            '<font face="Courier">',
            txt,
            '</font>',
            '</div>',
          )

        else:
          k='py'
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
      for k in kys(tabdic):
        if k in f:
          tabdic[k].append(div+'\n')
          break
  tabs="""
  <div class="tab">\n"""
  for k in tabdic:
    tabs=tabs+"""<button class="tablinks" onclick="openTab(event, 'TAB')">TAB</button>\n""".replace('TAB',k)
  tabs=tabs+"</div>\n"



  tabscript="""
<style>
        .tab {
            overflow: hidden;
            border-bottom: 1px solid #ccc;
        }
        .tab button {
            background-color: inherit;
            border: none;
            outline: none;
            cursor: pointer;
            padding: 14px 16px;
            transition: 0.3s;
            font-size: 17px;
        }
        .tab button:hover {
            background-color: #ddd;
        }
        .tab button.active {
            background-color: #ccc;
        }
        .tabcontent {
            display: none;
            padding: 6px 12px;
            border-top: none;
        }
</style>

<script>
    function openTab(evt, tabName) {
        var i, tabcontent, tablinks;

        // Hide all tab content
        tabcontent = document.getElementsByClassName("tabcontent");
        for (i = 0; i < tabcontent.length; i++) {
            tabcontent[i].style.display = "none";
        }

        // Remove the background color of all tab links
        tablinks = document.getElementsByClassName("tablinks");
        for (i = 0; i < tablinks.length; i++) {
            tablinks[i].className = tablinks[i].className.replace(" active", "");
        }

        // Show the current tab content and add an "active" class to the button that opened the tab
        document.getElementById(tabName).style.display = "block";
        evt.currentTarget.className += " active";
    }

    // Set default tab to open
    document.getElementsByClassName("tablinks")[0].click();
</script>
"""


  hs=[css]+[tabscript]+[tabs]+["""
<font face="Courier">
<h3 id="copyText">"""+w.replace(opjh(),'')+"""</h3>
</font>
<script>
  document.getElementById('copyText').addEventListener('click', function() {
      // Create a temporary textarea element
      const textarea = document.createElement('textarea');
      textarea.value = this.innerText;
      document.body.appendChild(textarea);

      // Select the text and copy it
      textarea.select();
      document.execCommand('copy');

      // Remove the temporary textarea element
      document.body.removeChild(textarea);

      // Optionally, provide feedback to the user
      alert('Text copied to clipboard!');
  });
</script>
  """]
  
  for k in tabdic:
    tabcontent='\n'.join(tabdic[k])
    hs+=["""
<div id="THETAB" class="tabcontent">
  THE_TAB_CONTENT
</div>
""".replace('THETAB',k).replace('THE_TAB_CONTENT',tabcontent)]


  """
  <div class="tab">
    <button class="tablinks" onclick="openTab(event, 'Tab1')">Tab 1</button>
    <button class="tablinks" onclick="openTab(event, 'Tab2')">Tab 2</button>
    <button class="tablinks" onclick="openTab(event, 'Tab3')">Tab 3</button>
  </div>

  <div id="Tab2" class="tabcontent">
    <h3>Tab 2</h3>
    <p>This is the content for Tab 2.</p>
  </div>

  <div id="Tab3" class="tabcontent">
    <h3>Tab 3</h3>
    <p>This is the content for Tab 3.</p>
  </div>
  """


  #hs=[css]+[d2n('<font face="Courier"><h3>',w.replace(opjh(),''),
  #  '</h3></font>')]+hs
  htmlfile=opj(w,'_'+'merge.html')
  text_to_file(
    htmlfile,
    '\n'.join(hs)
  )
  if newtab:
    open_url(htmlfile)



if __name__ == '__main__':
    args=dict(
        src='',
        most_recent=1,
        repeat=30,
    )
    p=getparser(**args)
    assert ope(p.src)

    newtab=True
    src_previous=p.src

    while True:
      if p.most_recent:
        src=most_recent_file_in_folder(p.src)
        if src!=src_previous:
          newtab=True
        src_previous=src
      merge_content(w=src,default_height=u2.sn.default_height,newtab=newtab)
      newtab=False
      if not p.repeat:
        break
      else:
        time.sleep(p.repeat)

#EOF
