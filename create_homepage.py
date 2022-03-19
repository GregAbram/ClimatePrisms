import sys, os
from json import load
from bs4 import BeautifulSoup

f = open('/tmp/log', 'a')
f.write('create_homepage\n')
f.close()

if len(sys.argv) != 2:
  print("project arg required")
  sys.exit(0)

if not os.path.isfile('%s/setup.json' % sys.argv[1]):
  print("project setup.json required")
  sys.exit(0)

with open('%s/setup.json' % sys.argv[1]) as cfp:
  config = load(cfp)

with open("homepage.html") as ifp:
    soup = BeautifulSoup(ifp, "html.parser")

title = soup.new_tag('title')
title.string = config['title']
soup.head.append(title)

homepage = soup.find(id='home-container')

f = open('/tmp/log', 'a')
f.write('a\n')
f.close()

img = soup.new_tag('img')
img['src'] = config['homepage-image']
img['class'] = 'home-container-img'
img['style'] = 'width: 100%; height: 100%;'
homepage.append(img)

bdiv = soup.new_tag("div")
bdiv['class'] = 'home-container-title-background'
homepage.append(bdiv)

f = open('/tmp/log', 'a')
f.write('b\n')
f.close()

for i,line in enumerate(config['homepage-title']):
  p = soup.new_tag("p")
  if i == 0:
    p['style'] = "font-weight: bold"
  p.string = line
  bdiv.append(p)

f = open('/tmp/log', 'a')
f.write('c\n')
f.close()


num_themes = len(config['themes'])
max_stories = -1
for i in range(num_themes):
  if len(config['themes'][i]['stories']) > max_stories:
    max_stories = len(config['themes'][i]['stories'])

button_box = soup.new_tag('div')
button_box['class'] = 'home-container-button-box '
button_box['style'] = "display: grid; grid-template-columns: " + ('1fr '*num_themes) + ';'

f = open('/tmp/log', 'a')
f.write('d\n')
f.close()

for t, theme in enumerate(config['themes']):

  f = open('/tmp/log', 'a')
  f.write('%s\n' % theme)
  f.close()

  p = soup.new_tag('p')

  f = open('/tmp/log', 'a')
  f.write('%s 1\n' % theme)
  f.close()

  p.string = theme['theme']['title']
  f = open('/tmp/log', 'a')
  f.write('%s 2\n' % theme)
  f.close()

  p['class'] = 'home-container-button-box-column-%d' % t
  f = open('/tmp/log', 'a')
  f.write('%s 3\n' % theme)
  f.close()

  tdiv = soup.new_tag('div')
  f = open('/tmp/log', 'a')
  f.write('%s 4\n' % theme)
  f.close()

  tdiv['class'] = 'home-container-button-box-theme home-container-button-box-column-%d' % t
  f = open('/tmp/log', 'a')
  f.write('%s 5\n' % theme)
  f.close()

  tdiv['onclick'] = "initialSelection('%s', {'theme': '%s', 'story': 'any'})" % (theme['theme']['video'], theme['theme']['tag'])
  f = open('/tmp/log', 'a')
  f.write('%s 6\n' % theme)
  f.close()

  tdiv.append(p)
  f = open('/tmp/log', 'a')
  f.write('%s 7\n' % theme)
  f.close()

  button_box.append(tdiv)

  f = open('/tmp/log', 'a')
  f.write('%s done\n' % theme)
  f.close()


f = open('/tmp/log', 'a')
f.write('e\n')
f.close()

for t, theme in enumerate(config['themes']):
  for s, story in enumerate(theme['stories']):
    tdiv = soup.new_tag('div')
    tdiv['class'] = 'home-container-button-box-story home-container-button-box-column-%d' % t
    tdiv['style'] = "grid-row: %d; grid-column: %d;" % (s+2, t+1)
    tdiv['onclick'] = "initialSelection('%s', {'theme': '%s', 'story': '%s'})" % (story['video'], theme['theme']['tag'], story['tag'])
    p = soup.new_tag('p')
    p.string = story['title']
    tdiv.append(p)
    button_box.append(tdiv)

f = open('/tmp/log', 'a')
f.write('f\n')
f.close()

homepage.append(button_box)

f = open('/tmp/log', 'a')
f.write('create_homepage bottom')
f.close()

with open("static/index.html", "w") as ofp:
    ofp.write(str(soup))

f = open('/tmp/log', 'a')
f.write('create_homepage done\n')
f.close()
