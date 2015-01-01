#!/usr/bin/env python3
import re
import os
import CommonMark

main_template = """<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="chrome=1">
    <title>Mobiilne Tunniplaani Rakendus</title>

    <link rel="stylesheet" href="stylesheets/styles.css">
    <link rel="stylesheet" href="stylesheets/pygment_trac.css">
    <link rel="stylesheet" href="octicons/octicons.css">
    <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
    <!--[if lt IE 9]>
    <script src="//html5shiv.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->
  </head>
  <body>
    <div class="wrapper">
      <header>
        <h1>Mobiilne Tunniplaani Rakendus</h1>
        <p>Tunniplaani rakendus, mis võimaldab Väike-Maarja Õppekeskuse ja Gümnaasiumi tunniplaane vaadata ilma Flash Player&#39;ita mobiiltelefonist</p>

        <p class="view"><a href="http://tunniplaan.arti.ee/">Ava töötav tunniplaani rakendus <small>tunniplaan.arti.ee</small></a></p>

        <p class="view"><a href="https://github.com/arti95/tunniplaan.arti.ee">Vaata projekti lähtekoodi GitHub'is <small>arti95/tunniplaan.arti.ee</small></a></p>


        <ul>
          <li><a href="http://tunniplaan.arti.ee/">Ava töötav <strong>Tunniplaan</strong></a></li>
          <li><a href="https://github.com/arti95/tunniplaan.arti.ee">Vaata lähtekoodi <strong>GitHub'is</strong></a></li>
        </ul>
      </header>
<section>
{posts}
      </section>
      <footer>
        <p>Selle projekti eest hoolitsevad <br>
        <a style="padding-left:20px" href="https://www.google.ee/+ArtiZirk">Arti Zirk</a><br>
        <a style="padding-left:20px" href="https://www.facebook.com/kaili.zirk">Kaili Zirk</a></p>
        <p><small>Teema autor <a href="https://github.com/orderedlist">orderedlist</a></small></p>
      </footer>
    </div>
    <script src="javascripts/scale.fix.js"></script>
              <script type="text/javascript">
            var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
            document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
          </script>
          <script type="text/javascript">
            try {
              var pageTracker = _gat._getTracker("UA-41510505-4");
            pageTracker._trackPageview();
            } catch(err) {}
          </script>

  </body>
</html>
"""

post_template = """
<h3>
<a id="{slug}" class="anchor" href="#{slug}" aria-hidden="true"><span class="octicon octicon-link"></span> </a>{title} <small>({date})</small></h3>
{content}
"""

def yaml_loads(string):
    """stupid minimal yaml like loader"""
    out = {}
    for line in string.strip().split("\n"):
        key, val = line.split(":")
        key = key.strip()
        val = val.strip()
        out[key] = val
    return out


POST_RE = re.compile(u'---(?P<meta>.*?)---(?P<body>.*)', re.DOTALL)

posts = []

parser = CommonMark.DocParser()
renderer = CommonMark.HTMLRenderer()

post_files = os.listdir("posts")
for post_file in post_files:
    with open("posts/"+post_file) as f:
        content = f.read()
        post_match = POST_RE.match(content)
        if not post_match:
            continue
        meta = yaml_loads(post_match.group("meta"))
        body = post_match.group('body')
        post = post_template.format(content=body, **meta)
        if post_file.endswith(".md"):
            ast = parser.parse(post)
            post = renderer.render(ast)
        posts.append(post)


with open("index.html", "w") as f:
    f.write(main_template.replace("{posts}", "\n".join(posts)))
print("done")