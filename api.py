import pymongo, json, pdb
from time import time
from random import random

class API:

  def __init__(self):
    self.db = pymongo.MongoClient('localhost', 1336)['climateprisms']
    self.nodes = self.db['nodes']
    self.fillers = self.db['fillers']
    self.userinfo = self.db['userinfo']
    self.keywords = self.db['keywords']
    self.user_id = -1
    self.last_user_action_time = -1
    self.levelForContext = ''

  def choose(self, options, k):
    r = []
    for i in range(k):
      if len(options) > 0:
        r.append(options.pop(int(random() * len(options))))
    return r

  def run(self, op, args):
    try:
        fcn = getattr(self, op)
        return fcn(args)
    except:
        print("bad API call:", op, args)

  def get_fillers(self, args):
    f = list(self.fillers.find())
    for i in f:
      i.pop('_id')
    s = json.dumps({ 'data': f })
    print("rply:", s)
    return json.dumps({ 'data': f })

  def get_keywords(self, args):
    f = list(self.keywords.find())
    for i in f:
      i.pop('_id')
    return json.dumps({ 'data': f })

  def find_one(self, q):
    agg = self.nodes.aggregate([{'$match': q}, { '$sample': {'size': 1}}])
    return [i for i in agg]

  def find_n(self, q, n):
    agg = self.nodes.aggregate([{'$match': q}, { '$sample': {'size': n}}])
    return [i for i in agg]

  def find_and_add(self, q, n, r):
    agg = self.nodes.aggregate([{'$match': q}, { '$sample': {'size': n}}])
    return r + [i for i in agg]

  def detail_general(self):
    return

  def get_tag(self, args):

    now = time()
    if now - self.last_user_action_time > 180:  # 3 minutes
      self.user_id = self.user_id + 1
    self.userinfo.insert_one({'userid': self.user_id, 'query': args})

    theme = args['theme']
    story = args['story']

    print("GET_TAG ENTRY")

    headers = ['definition', 'problem', 'impact', 'pointer']

    if args['sequence_level'] == '1':
      reply_nodes = self.find_one({'include': 'x', 'theme': theme, 'story': story, 'detail': 'definition'})
      if len(reply_nodes) == 0:
          reply_nodes = self.find_one({'include': 'x', 'theme': theme, 'story': 'any', 'detail': 'definition'})
      filename_list = [i['filename'] for i in reply_nodes]
      reply_nodes = reply_nodes + self.find_n({'filename': {'$nin': filename_list}, 'detail': {'$nin': headers}, 'include': 'x', 'theme': theme, 'story': story}, 4)
    elif args['sequence_level'] == '2':
      reply_nodes = self.find_one({'include': 'x', 'theme': theme, 'story': story, 'detail': 'problem'}) + [args]
      if len(reply_nodes) == 0:
          reply_nodes = self.find_one({'include': 'x', 'theme': theme, 'story': 'any', 'detail': 'problem'})
      filename_list = [i['filename'] for i in reply_nodes]
      reply_nodes = reply_nodes + self.find_n({'filename': {'$nin': filename_list}, 'detail': {'$nin': headers}, 'include': 'x', 'theme': theme, 'story': story}, 4)
    elif args['sequence_level'] == '3':
      reply_nodes = self.find_one({'include': 'x', 'theme': theme, 'story': story, 'detail': 'impact'}) + [args]
      if len(reply_nodes) == 0:
          reply_nodes = self.find_one({'include': 'x', 'theme': theme, 'story': 'any', 'detail': 'impact'})
      filename_list = [i['filename'] for i in reply_nodes]
      reply_nodes = reply_nodes + self.find_n({'filename': {'$nin': filename_list}, 'detail': {'$nin': headers}, 'include': 'x', 'theme': theme, 'story': story}, 4)
    else:
      # add last image and a pointer
      reply_nodes = [args] +  self.find_one({'include': 'x', '$or': [{'theme': {'$ne': theme}}, {'story': {'$ne': story}}], 'detail': 'pointer'})
      filename_list = [i['filename'] for i in reply_nodes]

      if args['type'] == 'image':
        # half the time, pick a video or audio from this theme/story UNLESS selected was nor a video or audio
        if random() > 0.5:
          query = {'filename': {'$nin': filename_list}, 'detail': {'$nin': headers}, 'include': 'x', 'theme': theme, 'story': story, 'type': {'$ne': 'image'}}
          reply_nodes = reply_nodes + self.find_one(query)
          filename_list = [i['filename'] for i in reply_nodes]

      # select 4 without text and 1 with

      reply_nodes = reply_nodes + self.find_n({'filename': {'$nin': filename_list}, 'detail': {'$nin': headers}, 'include': 'x', 'theme': theme, 'story': story, 'type': 'image'}, 4)
      filename_list = [i['filename'] for i in reply_nodes]

      reply_nodes = reply_nodes + self.find_n({'filename': {'$nin': filename_list}, 'detail': {'$nin': headers}, 'include': 'x', 'theme': theme, 'story': story, 'type': 'image'}, 4)
      filename_list = [i['filename'] for i in reply_nodes]

    print('SEQUENCE', args['sequence_level'])
    for i in reply_nodes:
      print(i['theme'], i['story'], i['filename'], i['type'], i['detail'])
      if 'caption' in i:
        i['caption'] = i['caption'].replace("'", "")
      if ('_id') in i:
        i.pop('_id')

    query = {'include': 'x', 'type': 'video', 'theme': theme}
    filler_nodes = self.find_n(query, 6)

    for i in filler_nodes:
      if ('_id') in i:
        i.pop('_id')

    s = json.dumps({ 'data': reply_nodes, 'filler nodes': filler_nodes })

    print('GET_TAG DONE')
    return s;

  def post_userinfo(self, args):
    print("USERINFO", ",".join(args))
