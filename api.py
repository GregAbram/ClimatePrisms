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

    if args['sequence_level'] == '1':
      reply_nodes = self.find_one({'include': 'x', 'theme': theme, 'story': story, 'detail': 'definition'})
      reply_nodes = reply_nodes + self.find_n({'include': 'x', 'theme': theme, 'story': story, '$and': [{'detail': {'$ne': 'intro'}}, {'detail': {'$ne': 'definition'}}, {'detail': {'$ne': 'problem'}}, {'detail': {'$ne': 'impact'}}, {'detail': {'$ne': 'pointer'}}]}, 4)
    elif args['sequence_level'] == '2':
      reply_nodes = self.find_one({'include': 'x', 'theme': theme, 'story': story, 'detail': 'problem'}) + [args]
      reply_nodes = reply_nodes + self.find_n({'include': 'x', 'theme': theme, 'story': story, '$and': [{'detail': {'$ne': 'intro'}}, {'detail': {'$ne': 'definition'}}, {'detail': {'$ne': 'problem'}}, {'detail': {'$ne': 'impact'}}, {'detail': {'$ne': 'pointer'}}]}, 4)
    elif args['sequence_level'] == '3':
      reply_nodes = self.find_one({'include': 'x', 'theme': theme, 'story': story, 'detail': 'impact'}) + [args]
      reply_nodes = reply_nodes + self.find_n({'include': 'x', 'theme': theme, 'story': story, '$and': [{'detail': {'$ne': 'intro'}}, {'detail': {'$ne': 'definition'}}, {'detail': {'$ne': 'problem'}}, {'detail': {'$ne': 'impact'}}, {'detail': {'$ne': 'pointer'}}]}, 4)
    else:
      # add last image and a pointer
      reply_nodes = [args] +  self.find_one({'include': 'x', '$or': [{'theme': {'$ne': theme}}, {'story': {'$ne': story}}], 'detail': 'pointer'})

      # half the time, pick a video or audio from this theme/story
      if random() > 0.5:
        query = {'include': 'x', 'theme': theme, 'story': story, 'type': {'$ne': 'image'}}
        reply_nodes = reply_nodes + self.find_one(query)

      # select 4 without text and 1 with
      reply_nodes = reply_nodes + self.find_n({'include': 'x', 'theme': theme, 'story': story, 'text': 0, '$and': [{'detail': {'$ne': 'intro'}}, {'detail': {'$ne': 'definition'}}, {'detail': {'$ne': 'problem'}}, {'detail': {'$ne': 'impact'}}, {'detail': {'$ne': 'pointer'}}]}, 4)
      reply_nodes = reply_nodes + self.find_n({'include': 'x', 'theme': theme, 'story': story, 'text': 1, '$and': [{'detail': {'$ne': 'intro'}}, {'detail': {'$ne': 'definition'}}, {'detail': {'$ne': 'problem'}}, {'detail': {'$ne': 'impact'}}, {'detail': {'$ne': 'pointer'}}]}, 1)


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

  def get_content(self, args):
    now = time()
    if now - self.last_user_action_time > 180:  # 3 minutes
      self.user_id = self.user_id + 1
    self.userinfo.insert_one({'userid': self.user_id, 'query': args})

    pdb.set_trace()

    reply_nodes = []
    # query = {'filename': 'aud_ecology_1.png'}
    # reply_nodes = self.find_and_add(query, 2, reply_nodes)

    if args['field'] == 'story' or args['field'] == 'tag':

      if args['field'] == 'tag':
        node = self.nodes.find_one({'category': args['value']})
      else:
        node = self.nodes.find_one({'story': args['value']})

      # self.choose a category

      choices = [i.replace(" ", "") for i in node['category'].split(",")]
      category = choices[int(random() * len(choices))]
      regex = {'$regex': ", " + category + ",|^" + category + ",|^" + category + "$|, " + category + "$"}

      # select from that category WITHOUT TEXT

      query = {'$and': [{'include': 'x'}, {'category': regex}, {'text': 0}]}
      reply_nodes = self.find_and_add(query, 2, reply_nodes)

      # select from that category WITH TEXT

      query = {'$and': [{'include': 'x'}, {'category': regex}, {'text': 1}]}
      reply_nodes = self.find_and_add(query, 1, reply_nodes)

      # self.choose a theme by story

      choices = [i.replace(" ", "") for i in node['story'].split(",")]
      theme = choices[int(random() * len(choices))]
      regex = {'$regex': ", " + theme + ",|^" + theme + ",|^" + theme + "$|, " + theme + "$"}
      query = {'$and': [{'include': 'x'}, {'theme': regex}, {'text': 0}]}
      reply_nodes = self.find_and_add(query, 1, reply_nodes)

      # select content from same row on the story by using the last digit of #8

      levels = [i.replace(" ", "") for i in node['level'].split(",")]
      level = list(levels[int(random() * len(levels))])
      level[2] = '8'
      level = "".join([str(i) for i in level])
      regex = {'$regex': ", " + level + ",|^" + level + ",|^" + level + "$|, " + level + "$"}
      query = {'$and': [{'include': 'x'}, {'level': regex}, {'text': 0}]}
      reply_nodes = self.find_and_add(query, 1, reply_nodes)

    elif args['field'] == 'rules':

      rule,story_iteration,iteration = args['value'].split(',')
      iteration = int(iteration)

      if iteration < 3:

        if iteration == 0:
          reply_nodes.append(self.nodes.find_one({'filename': rule}))

        query = {'$and': [{'include': 'x', 'theme': story_iteration, 'text': 0, 'layout': 0}]}
        reply_nodes = self.find_and_add(query, 3, reply_nodes)

        # this has got to be wrong, but check express_server.js

        query = {'$and': [{'include': 'x', 'theme': story_iteration, 'text': 0, 'layout': 0}]}
        reply_nodes = self.find_and_add(query, 1, reply_nodes)

        query = {'$and': [{'include': 'x', 'theme': story_iteration, 'text': 1, 'layout': 0}]}
        reply_nodes = self.find_and_add(query, 1, reply_nodes)

      else:

        query = {'filename': {'$regex': rule}}
        query_result = list(self.nodes.find(query))
        if len(query_result) > 0:

          for rule_node in query_result:
            reply_nodes.append(self.nodes.find_one({'filename': rule_node['filename']}))

            # Obtain an image from levels

            levels = [i.replace(" ", "") for i in rule_node['level'].split(",")]
            level = int(levels[int(random() * len(levels))])

            values = ['{a:03d}'.format(a = (level+i)) for i in range(2)]
            self.levelForContext = ','.join(values)

            regex = {'$regex': "(," + values[0] + "|^" + values[0] + ",|^" + values[0] + "$|^" + values[0] + "$)|(," + values[1] + "|^" + values[1] + ",|^" + values[1] + "$|^" + values[1] + "$)"}

            # 2 WITHOUT TEXT

            query = {'$and': [{'include': 'x'}, {'level': regex}, {'text': 0}]}
            reply_nodes = self.find_and_add(query, 1, reply_nodes)

            # 1 WITH TEXT

            query = {'$and': [{'include': 'x'}, {'level': regex}, {'text': 1}]}
            reply_nodes = self.find_and_add(query, 1, reply_nodes)

            # select content from same row on the story by using the last digit of #8

            levels = [i.replace(" ", "") for i in rule_node['level'].split(",")]
            level = list(levels[int(random() * len(levels))])
            level[2] = '8'
            level = "".join([str(i) for i in level])

            regex = {'$regex': ", " + level + ",|^" + level + ",|^" + level + "$|, " + level + "$"}
            query = {'$and': [{'include': 'x'}, {'level': regex}, {'text': 0}]}
            reply_nodes = self.find_and_add(query, 1, reply_nodes)

    else:
      print("XXXXXXXXX Unrecognized get_content tag: " + args['field'])

    for i in reply_nodes:
      i.pop('_id')
    return json.dumps({ 'data': reply_nodes })

  def post_userinfo(self, args):
    print("USERINFO", ",".join(args))
