import sys, os
from json import load
from bs4 import BeautifulSoup

with open('/tmp/py.log', 'w') as f:

  if len(sys.argv) != 2:
    f.write("project arg required\n")
    sys.exit(0)
  
  f.write('create_homepage\n')
  f.write('looking to setup home page from %s/setup.json\n' % sys.argv[1])
  
  if not os.path.isfile('%s/setup.json' % sys.argv[1]):
    f.write("project setup.json required\n")
    sys.exit(0)
  
  with open('%s/setup.json' % sys.argv[1]) as cfp:
    config = load(cfp)
  
  with open("homepage.html") as ifp:
      soup = BeautifulSoup(ifp, "html.parser")
  
  title = soup.new_tag('title')
  title.string = config['title']
  soup.head.append(title)
  
  homepage = soup.find(id='home-container')
  
  img = soup.new_tag('img')
  img['src'] = config['homepage-image']
  img['class'] = 'home-container-img'
  img['style'] = 'width: 100%; height: 100%;'
  homepage.append(img)
  
  bdiv = soup.new_tag("div")
  bdiv['class'] = 'home-container-title-background'
  homepage.append(bdiv)
  
  for i,line in enumerate(config['homepage-title']):
    p = soup.new_tag("p")
    if i == 0:
      p['style'] = "font-weight: bold"
    p.string = line
    bdiv.append(p)
  
  
  num_themes = len(config['themes'])
  max_stories = -1
  for i in range(num_themes):
    if len(config['themes'][i]['stories']) > max_stories:
      max_stories = len(config['themes'][i]['stories'])
  
  button_box = soup.new_tag('div')
  button_box['class'] = 'home-container-button-box '
  button_box['style'] = "grid-template-columns: " + ('1fr '*num_themes) + ';'
  
  for t, theme in enumerate(config['themes']):
  
    p = soup.new_tag('p')
  
    p.string = theme['theme']['title']
    p['class'] = 'home-container-button-box-column-%d' % t
  
    tdiv = soup.new_tag('div')
  
    tdiv['class'] = 'home-container-button-box-theme home-container-button-box-column-title home-container-button-box-column-%d' % t
  
    tdiv['onclick'] = "initialSelection('%s', {'theme': '%s', 'story': 'any'})" % (theme['theme']['video'], theme['theme']['tag'])
  
    tdiv.append(p)
  
    button_box.append(tdiv)
  
  for t, theme in enumerate(config['themes']):
    for s, story in enumerate(theme['stories']):
      tdiv = soup.new_tag('div')
      tdiv['class'] = 'home-container-button-box-story home-container-button-box-button home-container-button-box-column-%d' % t
      tdiv['style'] = "grid-row: %d; grid-column: %d;" % (s+2, t+1)
      tdiv['onclick'] = "initialSelection('%s', {'theme': '%s', 'story': '%s'})" % (story['video'], theme['theme']['tag'], story['tag'])
      p = soup.new_tag('p')
      p.string = story['title']
      tdiv.append(p)
      button_box.append(tdiv)
  
  homepage.append(button_box)
  
  with open("static/index.html", "w") as ofp:
      ofp.write(str(soup))
  
  f.write('create_homepage done\n')
