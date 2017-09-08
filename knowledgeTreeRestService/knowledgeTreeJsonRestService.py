__author__ = 'naras_mg'
# libraries
from flask import Flask, jsonify, abort, make_response, request
import json, ast, logging, peewee, flask_httpauth
import networkx as nx
from networkx.readwrite import json_graph
import random, string

auth = flask_httpauth.HTTPBasicAuth()
def ceasar(plain,shift):  # shift each letter by shift
        return "".join([chr((ord(x)- start(x) + shift) % 26 + start(x)) for (x) in list(plain)])
def start(alphabet): # find distance between alphabet and 'a' or 'A'
            strt = ord('a') if alphabet.islower() else ord('A')
            return strt
@auth.get_password
def get_password(username):
    auths = json.load(open("credentials_roles.txt"))
    if username in auths:
        return ceasar(auths[username]["pw"],10);
    return None
def get_role(username):
    auths = json.load(open("credentials_roles.txt"))
    if username in auths:
        return auths[username]["role"]
    return None
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

# own modules
import knowledgeTreeModelSmall as ktm

def create_relation(subject1,subject2,relation,sortorder=None):
    # for item in srsJson:
    #     dict = ast.literal_eval(item)
    #     if (dict['subject1'] == subject1) and (dict['subject2'] == subject2) and (dict['relations'] == relation): #duplicate relation
    #       return False
    if (find_item_json_dict_list(subjectsJson,'id',subject1) is None) or (find_item_json_dict_list(subjectsJson,'id',subject2) is None) or (find_item_json_dict_list(ssrJson,'id',relation) is None):
        return False  # either of the subjects or relation not valid
    elif find_relation(subject1,subject2) is not None:  # subjects are already related
        return False
    else:
        try:
            dict = {'subject1':subject1,'subject2':subject2,'relation':relation,'sortorder':sortorder}
            srsJson.append(dict)
            srsNew = ktm.SubjectRelatestoSubject.create(subject1=subject1,subject2=subject2,relation=relation,sortorder=sortorder)
        except peewee.IntegrityError:
            logging.error(auth.username() + 'Failed to create relation:', dict)
            return False
    return True
def update_relation(subject2,relation=None,sortorder=None):
    subject1 = find_relations(subject2)   # a list of subject1s - usually only one expected
    subject1 = find_relations(subject2)[0]['related']   # a list of subject1s - usually only one expected
    if (find_item_json_dict_list(subjectsJson,'id',subject1) is None) or (find_item_json_dict_list(subjectsJson,'id',subject2) is None) \
            or (find_item_json_dict_list(ssrJson,'id',relation) is None):
        return False  # either of the subjects or relation not valid
    else:
        try:
            # update the subject relations and sort order on the db
            replace_relation(subject1,subject2,relation,sortorder)
            srsNew = ktm.SubjectRelatestoSubject.get(ktm.SubjectRelatestoSubject.subject1==subject1,ktm.SubjectRelatestoSubject.subject2==subject2)
            if relation is not None:srsNew.relation = relation
            if sortorder is not None:srsNew.sortorder = sortorder
            srsNew.save()
        except peewee.IntegrityError:
            logging.error(auth.username() + 'Failed to update relation:'+ str(dict))
            return False
    return True
def delete_relation(subject1,subject2,relation):
    found = False
    for indx in range(len(srsJson)):  # find and remove the entry in Json array
        dict = srsJson[indx] #ast.literal_eval(srsJson[indx])
        # print dict
        if (dict['subject1'] == subject1) and (dict['subject2'] == subject2) and (dict['relation'] == relation):
            del srsJson[indx]
            found = True
            break;
    if not found: return False
    # if (find_item_json_dict_list(subjectsJson,'id',subject1) is None) or (find_item_json_dict_list(subjectsJson,'id',subject2) is None) or (find_item_json_dict_list(ssrJson,'id',relation) is None):
    #     return False # either of the subjects or relation not valid
    else:
        try:
            srs = ktm.SubjectRelatestoSubject.get(subject1=subject1,subject2=subject2,relation=relation)
            srs.delete_instance()
            return True
        except:
            logging.error(auth.username() + 'Failed to delete relation:'+ str(dict))
            return False
def find_relation(subject1,subject2):
    for dict in srsJson:
        # dict = item #ast.literal_eval(item)
        if (dict['subject1'] == subject1) and (dict['subject2'] == subject2):
          return dict['relation']
    return None
def find_relations(subject):  # find all relations a subject has with another subject
    relations = []
    for item in srsJson:
        dict = item #ast.literal_eval(item)
        if dict['subject2'] == subject:
            dictitem = {'related': dict['subject1'], 'relation': dict['relation']}
            if 'sortorder' in dict: dictitem['sortorder']=dict['sortorder']
            relations.append(dictitem)
    return relations
def replace_relation(subject1,subject2,relation=None,sortorder=None):
    for dict in srsJson:
        if (dict['subject1'] == subject1) and (dict['subject2'] == subject2):
          if relation is not None: dict['relation'] = relation
          if sortorder is not None: dict['sortorder'] = sortorder
          return dict
    return None
def find_item_json_dict_list(lst,key,value):
    for dic in lst:
        # print dic, type(dic)
        if dic[key] == value: return dic
    return None
def entity_json_dict_list(rows):
    rowsJson = []
    for row in rows:
        db_flds = row.__dict__['_data']  # get all the db field names/values .. a dictionary
        jsonElement = '{'
        for fld_name,fld_value in db_flds.items():
            if not fld_value is None:
                # print ('name:'+fld_name + ' value:'+fld_value)
                withoutCRLF = unicode(fld_value).replace('\r\n','')
                withoutCRLF = unicode(withoutCRLF).replace('\n','')
                withoutCRLF=unicode(withoutCRLF).replace("'", r'\"')
                # if fld_name == 'description':
                #     logging.debug(auth.username() + withoutCRLF)
                jsonElement += "'" + fld_name + "':'" + withoutCRLF + "',"  # escape /r/n
        elem = jsonElement[:-1] + '}'
        # elem = ast.literal_eval(jsonElement2)
        # print elem
        rowsJson.append(ast.literal_eval(elem))
    return rowsJson
def move_relation(subject,newparent,newrelation=None,sortorder=None):  # moves a subject from one parent to another - the subtree moves
    relations=find_relations(subject)
    delete_relation(relations[0]['related'],subject,relations[0]['relation'])
    if newrelation == None: newrelation = relations[0]['relation']
    return create_relation(newparent,subject,newrelation,sortorder)
def add_name_description(td):
    dict = find_item_json_dict_list(subjectsJson,'id',td['id'])
    if not (dict == None):
        if 'name' in dict: td['name'] = dict['name']
        if 'description' in dict: td['description'] = dict['description']
        rel = find_relations(dict['id'])
        if not (rel==[]):
            td['relation']=rel[0]['relation']
            if 'sortorder' in rel[0]: td['sortorder']=rel[0]['sortorder']
        if 'children' in td:
            for child in td['children']:
                child = add_name_description(child)
    return td
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
def refreshGraph():
    g = nx.Graph()
    for row in subjectsJson:
        g.add_node(row['id'])
        g.node[row['id']]['name'] = row['name']
        if 'description' in row: g.node[row['id']]['description'] = row['description']
    for row in srsJson:
        g.add_edge(row['subject1'],row['subject2'])
        g[row['subject1']][row['subject2']]['relation'] = row['relation']
        if 'sortorder' in row: g[row['subject1']][row['subject2']]['sortorder'] = row['sortorder']
    return g
def refreshFromdb():
    # logging.debug('refresh subjects and relations from db')
    subjects = ktm.Subject.select()
    subjectsJson = entity_json_dict_list(subjects)
    srs = ktm.SubjectRelatestoSubject.select()
    srsJson = entity_json_dict_list(srs)

def work_find_relation(work1,work2):
    for dict in wrwJson:
        # dict = item #ast.literal_eval(item)
        if (dict['work1'] == work1) and (dict['work2'] == work2):
          return dict['relation']
    return None
def work_find_relations(work):  # find all relations a subject has with another subject
    relations = []
    for item in wrwJson:
        dict = item #ast.literal_eval(item)
        if dict['work2'] == work:
            # print dict
            dictitem = {'related': dict['work1'], 'relation': dict['relation']}
            if 'sortorder' in dict: dictitem['sortorder']=dict['sortorder']
            relations.append(dictitem)
    return relations
def work_create_relation(work1,work2,relation,sortorder=None):
    # for item in wrwJson:
    #     dict = ast.literal_eval(item)
    #     if (dict['work1'] == work1) and (dict['work2'] == work2) and (dict['relations'] == relation): #duplicate relation
    #       return False
    if (find_item_json_dict_list(worksJson,'id',work1) is None) or (find_item_json_dict_list(worksJson,'id',work2) is None) or (find_item_json_dict_list(wwrJson,'id',relation) is None):
        return False  # either of the works or relation not valid
    elif work_find_relation(work1,work2) is not None:  # works are already related
        return False
    else:
        try:
            dict = {'work1':work1,'work2':work2,'relation':relation,'sortorder':sortorder}
            wrwJson.append(dict)
            wrwNew = ktm.WorkRelatestoWork.create(work1=work1,work2=work2,relation=relation,sortorder=sortorder)
        except peewee.IntegrityError:
            logging.error(auth.username() + 'Failed to create work relation:'+ str(dict))
            return False
    return True
def work_update_relation(work2,relation=None,sortorder=None):
    work1 = work_find_relations(work2)[0]['related']   # a list of work1s - usually only one expected
    if (find_item_json_dict_list(worksJson,'id',work1) is None) or (find_item_json_dict_list(worksJson,'id',work2) is None) \
            or (find_item_json_dict_list(wwrJson,'id',relation) is None):
        return False  # either of the works or relation not valid
    else:
        try:
            # update the subject relations and sort order on the db
            work_replace_relation(work1,work2,relation,sortorder)
            wrwNew = ktm.WorkRelatestoWork.get(ktm.WorkRelatestoWork.work1==work1,ktm.WorkRelatestoWork.work2==work2)
            if relation is not None:wrwNew.relation = relation
            if sortorder is not None:wrwNew.sortorder = sortorder
            wrwNew.save()
        except peewee.IntegrityError:
            logging.error(auth.username() + 'Failed to update work relation:' + str(dict))
            return False
    return True
def work_replace_relation(work1,work2,relation=None,sortorder=None):
    for dict in wrwJson:
        if (dict['work1'] == work1) and (dict['work2'] == work2):
          if relation is not None: dict['relation'] = relation
          if sortorder is not None: dict['sortorder'] = sortorder
          return dict
    return None
def work_delete_relation(work1,work2,relation):
    found = False
    for indx in range(len(wrwJson)):  # find and remove the entry in Json array
        dict = wrwJson[indx] #ast.literal_eval(wrwJson[indx])
        # print dict
        if (dict['work1'] == work1) and (dict['work2'] == work2) and (dict['relation'] == relation):
            del wrwJson[indx]
            found = True
            break;
    if not found: return False
    # if (find_item_json_dict_list(worksJson,'id',work1) is None) or (find_item_json_dict_list(worksJson,'id',work2) is None) or (find_item_json_dict_list(wwrJson,'id',relation) is None):
    #     return False # either of the works or relation not valid
    else:
        try:
            wrw = ktm.WorkRelatestoWork.get(work1=work1,work2=work2,relation=relation)
            wrw.delete_instance()
            return True
        except:
            logging.error(auth.username() + 'Failed to delete work relation:' + str(dict))
            return False
def work_refreshGraph():
    g = nx.Graph()
    for row in worksJson:
        g.add_node(row['id'])
        g.node[row['id']]['name'] = row['name']
        if 'description' in row: g.node[row['id']]['description'] = row['description']
    for row in wrwJson:
        g.add_edge(row['work1'],row['work2'])
        g[row['work1']][row['work2']]['relation'] = row['relation']
        if 'sortorder' in row:
            g[row['work1']][row['work2']]['sortorder'] = row['sortorder']
            # print row['sortorder']
        else:g[row['work1']][row['work2']]['sortorder'] = '99'
        # print g[row['work1']][row['work2']]
    return g
def work_refreshFromdb():
    # logging.debug('refresh works and relations from db')
    works = ktm.Work.select()
    worksJson = entity_json_dict_list(works)
    wrw = ktm.WorkRelatestoWork.select()
    wrwJson = entity_json_dict_list(wrw)
def work_add_name_description(td):
    dict = find_item_json_dict_list(worksJson,'id',td['id'])
    if not (dict == None):
        if 'name' in dict: td['name'] = dict['name']
        if 'description' in dict: td['description'] = dict['description']
        rel = work_find_relations(dict['id'])
        if not (rel==[]):
            td['relation']=rel[0]['relation']
            if 'sortorder' in rel[0]: td['sortorder']=rel[0]['sortorder']
        if 'children' in td:
            for child in td['children']:
                child = work_add_name_description(child)
    return td
def work_move_relation(work,newparent,newrelation=None,sortorder=None):  # moves a work from one parent to another - the subtree moves
    relations=work_find_relations(work)
    work_delete_relation(relations[0]['related'],work,relations[0]['relation'])
    if newrelation == None: newrelation = relations[0]['relation']
    return work_create_relation(newparent,work,newrelation,sortorder)

def find_subject_work_relations(subject,work):
    relations = []
    for item in shwJson:
        dict = item #ast.literal_eval(item)
        if dict['subject'] == subject and dict['work'] == work:
            # print dict
            relations.append(item)
    return relations
def subject_work_create_relation(subject,work,relation):
    if find_subject_work_relations(subject,work) != []:  # subject/work are already related
        return False
    else:
        try:
            dict = {'subject':subject,'work':work,'relation':relation}
            shwJson.append(dict)
            # print 'creating subject_work relation:'+ dict['subject'] + '-'+ dict['work'] + '-'+relation
            ktm.SubjectHasWork.create(subject=subject,work=work,relation=relation)
            return True
        except peewee.IntegrityError:
                # print('Failed to create subject-work relation:', dict)
                return False
def subject_work_delete_relation(subject,work,relation):
    found = False
    for indx in range(len(shwJson)):  # find and remove the entry in Json array
        dict = shwJson[indx] #ast.literal_eval(srsJson[indx])
        # print dict
        if (dict['subject'] == subject) and (dict['work'] == work) and (dict['relation'] == relation):
            del shwJson[indx]
            found = True
            break;
    if not found: return False
    # if (find_item_json_dict_list(subjectsJson,'id',subject1) is None) or (find_item_json_dict_list(subjectsJson,'id',subject2) is None) or (find_item_json_dict_list(ssrJson,'id',relation) is None):
    #     return False # either of the subjects or relation not valid
    else:
        try:
            # shw = ktm.SubjectHasWork.get(subject=subject,work=work,relation=relation)
            # shw.delete_instance()
            qry = ktm.SubjectHasWork.delete().where(ktm.SubjectHasWork.subject==subject,ktm.SubjectHasWork.work==work,ktm.SubjectHasWork.relation==relation)
            qry.execute()
            return True
        except:
            # print 'Failed to delete subject-work relation:'+ subject + '-' + work + '-' + relation  #, dict
            return False
def subject_work_refreshFromdb():
    # logging.debug('refresh subject-to=worksfrom db')
    shw = ktm.SubjectHasWork.select()
    shwJson = entity_json_dict_list(shw)
def subject_work_refreshGraph(subject):
    g = nx.Graph()
    for row in shwJson:
        if row['subject']==subject:
            g.add_node(row['subject'])
            if row['subject'] == row['work']: wrk=row['work']+'_pramaaNa'
            else: wrk=row['work']
            g.add_node(wrk)
            g.add_edge(row['subject'],wrk)
            g[row['subject']][wrk]['relation'] = row['relation']
    if g.number_of_edges()==0:g.add_node(subject) # no work relatons for this subject
    return g
def work_subject_refreshGraph(work):
    g = nx.Graph()
    for row in shwJson:
        if row['work']==work:
            if row['subject'] == row['work']: sub=row['subject']+'_pramEya'
            else: sub=row['subject']
            g.add_node(sub)
            g.add_node(row['work'])
            g.add_edge(row['work'],sub)
            g[row['work']][sub]['relation'] = row['relation']
    if g.number_of_edges()==0:g.add_node(work) # no subject relatons for this work
    return g
def subject_work_add_relation(td):
    for elem in td['children']:
        dict = find_item_json_dict_list(shwJson,'work',elem['id'])
        if not (dict == None):
            if 'relation' in dict: elem['relation'] = dict['relation']
    return td
def work_subject_add_relation(td):
    for elem in td['children']:
        dict = find_item_json_dict_list(shwJson,'subject',elem['id'])
        if not (dict == None):
            if 'relation' in dict: elem['relation'] = dict['relation']
    return td

logging.basicConfig(filename='knowledgeTreeJournal.log',format='%(asctime)s %(message)s',level=logging.DEBUG)

app = Flask(__name__)

# db = ktm.database
# db.create_tables([ktm.Subject, ktm.SubjectRelatestoSubject], safe=True)
#
# # g.graph['subject'] = ktm.Subject.select()
# subjects = ktm.Subject.select()

db = ktm.database
db.create_tables([ktm.Subject, ktm.SubjectSubjectRelation, ktm.SubjectRelatestoSubject, \
                  ktm.Work, ktm.WorkWorkRelation, ktm.WorkRelatestoWork, \
                  ktm.SubjectHasWork, ktm.WorkSubjectRelation], safe=True)
logging.debug('Opened knowledgeTree Tables - Subject, SubjectSubjectRelation, Subject-Relates-to-Subject, Work, WorkWorkRelation Work_Relatesto_Work, SubjectHasWork % WorkSubjectRelation')

# subject related entities
ssr = ktm.SubjectSubjectRelation.select()
ssrJson = entity_json_dict_list(ssr)
srs = ktm.SubjectRelatestoSubject.select()
srsJson = entity_json_dict_list(srs)
subjects = ktm.Subject.select()
subjectsJson = entity_json_dict_list(subjects)

# work related entities
wwr = ktm.WorkWorkRelation.select()
wwrJson = entity_json_dict_list(wwr)
wrw = ktm.WorkRelatestoWork.select()
wrwJson = entity_json_dict_list(wrw)
works = ktm.Work.select()
worksJson = entity_json_dict_list(works)

#subject-work cross related entities
wsr = ktm.WorkSubjectRelation.select()
wsrJson = entity_json_dict_list(wsr)
shw = ktm.SubjectHasWork.select()
shwJson= entity_json_dict_list(shw)

logging.debug('populated Subject, SubjectSubjectRelation, Subject-Relates-to-Subject, Work, WorkWorkRelation & Work_Relatesto_Work arrays')
gs = refreshGraph()
gw = work_refreshGraph()

endpoint_prefix = '/knowledgeTree/api/v1.0/'

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/knowledgeTree')
def hello_world():
  return 'Hello from knowledgeTreeJsonRestService!'

#  --------------------  all features allowed for normal users(view subjects and relations) below -----------------------------
@app.route(endpoint_prefix + 'subjects', methods=['GET'])
@auth.login_required
def get_subjects():
    logging.debug(auth.username() + ':servicing JSON GET All subjects')
    return jsonify({'subjects': subjectsJson})
@app.route(endpoint_prefix + 'subject/<string:sub_id>', methods=['GET'])
@auth.login_required
def get_subject(sub_id):
    # sub = [sub for sub in subjectsJson if sub['id'] == str(sub_id)]
    logging.debug(auth.username() + ':servicing JSON GET: ' + sub_id)
    sub = find_item_json_dict_list(subjectsJson,'id',sub_id)
    if sub is None or len(sub) == 0:
        logging.error('JSON GET id missing: ' + sub_id)
        abort(404)
    return jsonify({'subject': sub})
@app.route(endpoint_prefix + 'subject-subject-relations', methods=['GET'])
@auth.login_required
def get_subject_subject_relations():
    logging.debug(auth.username() + ':servicing JSON GET All subject-subject-relations')
    return jsonify({'relations': ssrJson})
@app.route(endpoint_prefix + 'subject-to-subject', methods=['GET'])
@auth.login_required
def get_subject_relates_subject():
    logging.debug(auth.username() + ':servicing JSON GET All subject-relates-to-subject')
    return jsonify({'subject-to-subject': srsJson})
@app.route(endpoint_prefix + 'nodes-edges', methods=['GET'])
@auth.login_required
def get_nodes_edges():
    logging.debug(auth.username() + ':servicing JSON GET nodes & edges')
    refreshFromdb()
    # g = refreshGraph()
    # write json formatted data
    # d = json_graph.node_link_data(g) # node-link format to serialize
    # write json
    return jsonify(json_graph.node_link_data(refreshGraph()))
@app.route(endpoint_prefix + 'tree', methods=['GET'])
@auth.login_required
def get_tree():
    logging.debug(auth.username() + ':servicing JSON GET tree')
    refreshFromdb()
    # g = refreshGraph()
    # write json formatted data
    # t = nx.bfs_tree(g,"aum")
    # treedata = json_graph.tree_data(t,"aum")
    # write json
    return jsonify(add_name_description(json_graph.tree_data(nx.bfs_tree(refreshGraph(),"aum"),"aum")))
@app.route(endpoint_prefix + 'subtree/<string:sub_id>', methods=['GET'])
@auth.login_required
def get_subtree(sub_id):
    logging.debug(auth.username() + ':servicing JSON GET sub-tree')
    refreshFromdb()
    return jsonify(add_name_description(json_graph.tree_data(nx.bfs_tree(refreshGraph(),"aum"),sub_id)))
#  --------------------  all features allowed for editors (edit, create, remove subjects and relatins) below -----------------------------
@app.route(endpoint_prefix + 'subject-with-relation', methods=['POST'])
@auth.login_required
def create_subject_with_relation():
    if get_role(auth.username())in ['editor','admin']:
        logging.debug(auth.username() + ':servicing create subject with relation:'+str(request.json))
        if not request.json or not 'subject' in request.json or not 'related' in request.json or not 'relation' in request.json:
            logging.error('incorrect request:' + str(request.json))
            abort(400)
        if 'sortorder' in request.json: dict = {"subject": request.json['subject'], "related": request.json['related'], "relation": request.json['relation'],'sortorder':request.json['sortorder']}
        else: dict = {"subject": request.json['subject'], "related": request.json['related'], "relation": request.json['relation']}
        subject2 = dict['subject']
        if not 'id' in subject2 or not 'name' in subject2:
            logging.error('incorrect request:' + str(subject2))
            abort(401)
        subject1id = dict['related']
        if dict.has_key('relation'): relation = dict['relation']
        else: relation = None
        if dict.has_key('sortorder'): sortorder = int(dict['sortorder'])
        else: sortorder = None
        if find_item_json_dict_list(subjectsJson,'id',subject1id) is None:  # no subject1
            return None
        if find_item_json_dict_list(subjectsJson,'id',subject2['id']) is not None:
            # duplicate subject2 id .. generate a random id suffix and concatenate
            subject2['id'] = (subject2['id'] + ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(16)))[0:19]
        # subj = subject2 #ast.literal_eval(subject2)
        ktm.Subject.create(id=subject2['id'],name=subject2['name'],description=subject2['description'])  # db create row
        subjectsJson.append(subject2)
        return jsonify({'subject': create_relation(subject1id,subject2['id'],relation=relation,sortorder=sortorder)})
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'subject', methods=['POST'])
@auth.login_required
def create_subject():
    if get_role(auth.username())in ['editor','admin']:
        logging.debug(auth.username() + ':servicing create subject')
        if not request.json or not 'id' in request.json or not 'name' in request.json:
            logging.error('incorrect request:' + str(request.json))
            abort(400)
        subject = {"id": request.json['id'], "name": request.json['name'], "description": request.json.get('description', "")}
        if find_item_json_dict_list(subjectsJson,'id',str(request.json['id'])) is not None:
            # subj = ast.literal_eval(str(sub))
            # generate a random string and concatenate - changes id to unique 20-char string
            subject['id'] = (subject['id'] + ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(16)))[0:19]
        ktm.Subject.create(id=subject['id'],name=subject['name'],description=subject['description'])  # db create row
        subjectsJson.append(subject)
        return jsonify({'subject': subject}), 201
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'subject/<string:sub_id>', methods=['PUT'])
@auth.login_required
def update_subject(sub_id):
    if get_role(auth.username())in ['editor','admin']:
        logging.debug(auth.username() + ':servicing update subject: ' + sub_id)
        if (not request.json) or ('name' in request.json and type(request.json['name']) != unicode) \
                or ('description' in request.json and type(request.json['description']) is not unicode) \
                or ('relation' in request.json and type(request.json['relation']) is not unicode) \
                or ('sortorder' in request.json and type(request.json['sortorder']) is not unicode):
            logging.error('JSON PUT error incorrect request:' + str(request.json))
            abort(400)
        for index in range(len(subjectsJson)):
            # json_acceptable_string = subjectsJson[index].replace("'", "\"")
            dict = subjectsJson[index] #ast.literal_eval(subjectsJson[index])
            if dict['id'] == sub_id:
                dict['name'] = request.json.get('name', '')
                dict['description'] = request.json.get('description', '')
                subjectsJson[index] = dict #json.dumps(dict)
                subj = ktm.Subject.get(ktm.Subject.id == sub_id)   # db get/update row
                subj.name = dict['name']
                subj.description = dict['description']
                subj.save()
                if 'relation' in request.json or 'sortorder' in request.json:  # modify subject_to_subject if any change to relation or sort order
                    update_relation(sub_id,request.json.get('relation', None),int(request.json.get('sortorder', None)))
                return jsonify({'subject': dict}), 201
        logging.error('JSON PUT: id missing - '+ sub_id)
        abort(404)  # not found
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'subject-with-relation/<string:sub_id>', methods=['DELETE'])
@auth.login_required
def delete_subject_with_relation(sub_id):
    if get_role(auth.username())in ['editor','admin']:
        logging.debug(auth.username() + ':servicing delete subject with relation: ' + sub_id)
        relations = find_relations(sub_id)
        for subject_with_relation in relations:
            subject1 = subject_with_relation['related']
            relation = subject_with_relation['relation']
            delete_relation(subject1,sub_id,relation)# each relation with another subject1 removed
        for subj_index in range(len(subjectsJson)): # remove subject from db & Json list
                subj_as_dict = subjectsJson[subj_index] #ast.literal_eval(subjectsJson[subj_index])
                if subj_as_dict['id'] == sub_id or subj_as_dict[u'id'] == sub_id:
                    subjdbrow = ktm.Subject.get(ktm.Subject.id == subj_as_dict['id'])   # db get/delete row
                    subjdbrow.delete_instance()
                    del subjectsJson[subj_index]
                    break
        return jsonify({'result': True})
@app.route(endpoint_prefix + 'subject/<string:sub_id>', methods=['DELETE'])
@auth.login_required
def delete_subject(sub_id):
    if get_role(auth.username())in ['editor','admin']:
        logging.debug(auth.username() + ':servicing delete subject: ' + sub_id)
        sub = find_item_json_dict_list(subjectsJson,'id',sub_id)
        if sub is None or len(sub) == 0:
            logging.error('incorrect request:' + str(request.json))
            abort(404)
        # if len(sub) == 0:
        #     return False
        for subj_index in range(len(subjectsJson)):
            subj_as_dict = subjectsJson[subj_index] #ast.literal_eval(subjectsJson[subj_index])
            if (subj_as_dict['id'] == sub['id'] or subj_as_dict[u'id'] == sub['id'] or subj_as_dict['id'] == sub[u'id']) :
                subj = ktm.Subject.get(ktm.Subject.id == subj_as_dict['id'])   # db get/delete row
                subj.delete_instance()
                del subjectsJson[subj_index]
                break
        return jsonify({'result': True})
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'subject-to-subject', methods=['POST'])
@auth.login_required
def create_subject_to_subject():
    if get_role(auth.username())in ['editor','admin']:
        logging.debug(auth.username() + ':servicing subject-to-subject create relation')
        if not request.json or not 'subject1' in request.json or not 'subject2' in request.json or not 'relation' in request.json:
            logging.error('JSON POST incorrect request:' + str(request.json))
            abort(400)
        return jsonify({'result': create_relation(request.json['subject1'],request.json['subject2'],request.json['relation'])})
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'subject-to-subject', methods=['DELETE'])
@auth.login_required
def delete_subject_to_subject():
    if get_role(auth.username())in ['editor','admin']:
        logging.debug(auth.username() + ':servicing subject-to-subject delete relation')
        if not request.json or not 'subject1' in request.json or not 'subject2' in request.json or not 'relation' in request.json:
            logging.error('JSON POST incorrect request:' + str(request.json))
            abort(400)
        return jsonify({'result': delete_relation(request.json['subject1'],request.json['subject2'],request.json['relation'])})
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'subject-move/<string:sub_id>', methods=['POST'])
@auth.login_required
def move_subject(sub_id):
    if get_role(auth.username())in ['editor','admin']:
        logging.debug(auth.username() + ':servicing subject-to-subject move relation')
        if not request.json or not 'id' in request.json:
            logging.error('JSON POST incorrect request:' + str(request.json))
            abort(400)
        if 'relation' in request.json:
            if 'sortorder' in request.json:return jsonify({'result': move_relation(sub_id,request.json['id'],request.json['relation'],request.json['sortorder'])})
            else:return jsonify({'result': move_relation(sub_id,request.json['id'],request.json['relation'])})
        else:
            return jsonify({'result': move_relation(sub_id,request.json['id'])})
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'shutdown', methods=['POST'])
@auth.login_required
def shutdown():
    if get_role(auth.username())=='admin':
        shutdown_server()
        return jsonify({'result':'Server shutting down...'});
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)

#------------------------------------ work related selects -----------------------
#  --------------------  all features allowed for normal users(view works and relations) below -----------------------------
@app.route(endpoint_prefix + 'works', methods=['GET'])
@auth.login_required
def get_works():
    logging.debug(auth.username() + ':servicing JSON GET All works')
    return jsonify({'works': worksJson})
@app.route(endpoint_prefix + 'work/<string:wrk_id>', methods=['GET'])
@auth.login_required
def get_work(wrk_id):
    # sub = [sub for sub in subjectsJson if sub['id'] == str(wrk_id)]
    logging.debug(auth.username() + ':servicing JSON GET work: ' + wrk_id)
    wrk = find_item_json_dict_list(worksJson,'id',wrk_id)
    if wrk is None or len(wrk) == 0:
        logging.error('JSON GET id missing: ' + wrk_id)
        abort(404)
    return jsonify({'work': wrk})
@app.route(endpoint_prefix + 'work-work-relations', methods=['GET'])
@auth.login_required
def get_work_work_relations():
    logging.debug(auth.username() + ':servicing JSON GET All work-work-relations')
    return jsonify({'relations': wwrJson})
@app.route(endpoint_prefix + 'work-to-work', methods=['GET'])
@auth.login_required
def get_work_relates_work():
    logging.debug(auth.username() + ':servicing JSON GET All work-relates-to-work')
    return jsonify({'work-to-work': wrwJson})
@app.route(endpoint_prefix + 'nodes-edges-work', methods=['GET'])
@auth.login_required
def get_nodes_edges_work():
    logging.debug(auth.username() + ':servicing JSON GET work nodes & edges')
    work_refreshFromdb()
    # g = refreshGraph()
    # write json formatted data
    # d = json_graph.node_link_data(g) # node-link format to serialize
    # write json
    return jsonify(json_graph.node_link_data(work_refreshGraph()))
@app.route(endpoint_prefix + 'tree-work', methods=['GET'])
@auth.login_required
def get_tree_work():
    logging.debug(auth.username() + ':servicing JSON GET work tree')
    work_refreshFromdb()
    # g = refreshGraph()
    # write json formatted data
    # t = nx.bfs_tree(g,"aum")
    # treedata = json_graph.tree_data(t,"aum")
    # write json
    return jsonify(work_add_name_description(json_graph.tree_data(nx.bfs_tree(work_refreshGraph(),"all"),"all")))
@app.route(endpoint_prefix + 'subtree-work/<string:wrk_id>', methods=['GET'])
@auth.login_required
def get_subtree_work(wrk_id):
    logging.debug(auth.username() + ':servicing JSON GET work sub-tree')
    work_refreshFromdb()
    return jsonify(work_add_name_description(json_graph.tree_data(nx.bfs_tree(work_refreshGraph(),"all"),wrk_id)))
#  --------------------  all features allowed for editors (edit, create, remove subjects and relatins) below -----------------------------
@app.route(endpoint_prefix + 'work-with-relation', methods=['POST'])
@auth.login_required
def create_work_with_relation():
    if get_role(auth.username())in ['editor','admin']:
        logging.debug(auth.username() + ':servicing create work with relation:'+str(request.json))
        if not request.json or not 'work' in request.json or not 'related' in request.json or not 'relation' in request.json:
            logging.error('incorrect request:' + str(request.json))
            abort(400)
        if 'sortorder' in request.json: dict = {"work": request.json['work'], "related": request.json['related'], "relation": request.json['relation'],'sortorder':request.json['sortorder']}
        else: dict = {"work": request.json['work'], "related": request.json['work'], "relation": request.json['relation']}
        work2 = dict['work']
        if not 'id' in work2 or not 'name' in work2:
            logging.error('incorrect request:' + str(work2))
            abort(401)
        work1id = dict['related']
        if dict.has_key('relation'): relation = dict['relation']
        else: relation = None
        if dict.has_key('sortorder'): sortorder = int(dict['sortorder'])
        else: sortorder = None
        if find_item_json_dict_list(worksJson,'id',work1id) is None:  # no work1
            return None
        if find_item_json_dict_list(worksJson,'id',work2['id']) is not None:
            # duplicate work2 id .. generate a random id suffix and concatenate
            work2['id'] = (work2['id'] + ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(16)))[0:19]
        # workx = work2 #ast.literal_eval(work2)
        ktm.Work.create(id=work2['id'],name=work2['name'],description=work2['description'])  # db create row
        worksJson.append(work2)
        return jsonify({'work': work_create_relation(work1id,work2['id'],relation=relation,sortorder=sortorder)})
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'work', methods=['POST'])
@auth.login_required
def create_work():
    if get_role(auth.username())in ['editor','admin']:
        logging.debug(auth.username() + ':servicing create work')
        if not request.json or not 'id' in request.json or not 'name' in request.json:
            logging.error('incorrect request:' + str(request.json))
            abort(400)
        work = {"id": request.json['id'], "name": request.json['name'], "description": request.json.get('description', "")}
        if find_item_json_dict_list(worksJson,'id',str(request.json['id'])) is not None:
            # subj = ast.literal_eval(str(sub))
            # generate a random string and concatenate - changes id to unique 20-char string
            work['id'] = (work['id'] + ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(16)))[0:19]
        ktm.Work.create(id=work['id'],name=work['name'],description=work['description'])  # db create row
        worksJson.append(work)
        return jsonify({'work': work}), 201
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'work/<string:wrk_id>', methods=['PUT'])
@auth.login_required
def update_work(wrk_id):
    if get_role(auth.username())in ['editor','admin']:
        logging.debug(auth.username() + ':servicing update work: ' + wrk_id)
        if (not request.json) or ('name' in request.json and type(request.json['name']) != unicode) \
                or ('description' in request.json and type(request.json['description']) is not unicode) \
                or ('relation' in request.json and type(request.json['relation']) is not unicode) \
                or ('sortorder' in request.json and type(request.json['sortorder']) is not unicode):
            logging.error('JSON PUT error incorrect request:' + str(request.json))
            abort(400)
        for index in range(len(worksJson)):
            # json_acceptable_string = subjectsJson[index].replace("'", "\"")
            dict = worksJson[index] #ast.literal_eval(subjectsJson[index])
            if dict['id'] == wrk_id:
                dict['name'] = request.json.get('name', '')
                dict['description'] = request.json.get('description', '')
                worksJson[index] = dict #json.dumps(dict)
                workx = ktm.Work.get(ktm.Work.id == wrk_id)   # db get/update row
                workx.name = dict['name']
                workx.description = dict['description']
                workx.save()
                if 'relation' in request.json or 'sortorder' in request.json:  # modify work_to_work if any change to relation or sort order
                    work_update_relation(wrk_id,request.json.get('relation', None),int(request.json.get('sortorder', None)))
                return jsonify({'work': dict}), 201
        logging.error('JSON PUT: id missing - '+ wrk_id)
        abort(404)  # not found
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'work-with-relation/<string:wrk_id>', methods=['DELETE'])
@auth.login_required
def delete_work_with_relation(wrk_id):
    if get_role(auth.username())in ['editor','admin']:
        logging.debug(auth.username() + ':servicing delete subject with relation: ' + wrk_id)
        relations = work_find_relations(wrk_id)
        for work_with_relation in relations:
            work1 = work_with_relation['related']
            relation = work_with_relation['relation']
            work_delete_relation(work1,wrk_id,relation)# each relation with another work1 removed
        for work_index in range(len(worksJson)): # remove work from db & Json list
                work_as_dict = worksJson[work_index] #ast.literal_eval(subjectsJson[subj_index])
                if work_as_dict['id'] == wrk_id or work_as_dict[u'id'] == wrk_id:
                    workdbrow = ktm.Work.get(ktm.Work.id == work_as_dict['id'])   # db get/delete row
                    workdbrow.delete_instance()
                    del worksJson[work_index]
                    break
        return jsonify({'result': True})
@app.route(endpoint_prefix + 'work/<string:wrk_id>', methods=['DELETE'])
@auth.login_required
def delete_work(wrk_id):
    if get_role(auth.username())in ['editor','admin']:
        logging.debug(auth.username() + ':servicing delete subject: ' + wrk_id)
        wrk = find_item_json_dict_list(worksJson,'id',wrk_id)
        if wrk is None or len(wrk) == 0:
            logging.error('incorrect request:' + str(request.json))
            abort(404)
        # if len(wrk) == 0:
        #     return False
        for work_index in range(len(worksJson)):
            work_as_dict = worksJson[work_index] #ast.literal_eval(worksJson[work_index])
            if (work_as_dict['id'] == wrk['id'] or work_as_dict[u'id'] == wrk['id'] or work_as_dict['id'] == wrk[u'id']) :
                workx = ktm.Work.get(ktm.Work.id == work_as_dict['id'])   # db get/delete row
                workx.delete_instance()
                del worksJson[work_index]
                break
        return jsonify({'result': True})
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'work-to-work', methods=['POST'])
@auth.login_required
def create_work_to_work():
    if get_role(auth.username())in ['editor','admin']:
        logging.debug(auth.username() + ':servicing work-to-work create relation')
        if not request.json or not 'work1' in request.json or not 'work2' in request.json or not 'relation' in request.json:
            logging.error('JSON POST incorrect request:' + str(request.json))
            abort(400)
        return jsonify({'result': work_create_relation(request.json['work1'],request.json['work2'],request.json['relation'])})
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'work-to-work', methods=['DELETE'])
@auth.login_required
def delete_work_to_work():
    if get_role(auth.username())in ['editor','admin']:
        logging.debug(auth.username() + ':servicing work-to-work delete relation')
        if not request.json or not 'work1' in request.json or not 'work2' in request.json or not 'relation' in request.json:
            logging.error('JSON POST incorrect request:' + str(request.json))
            abort(400)
        return jsonify({'result': work_delete_relation(request.json['work1'],request.json['work2'],request.json['relation'])})
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'work-move/<string:wrk_id>', methods=['POST'])
@auth.login_required
def move_work(wrk_id):
    if get_role(auth.username())in ['editor','admin']:
        logging.debug(auth.username() + ':servicing work-to-work move relation')
        if not request.json or not 'id' in request.json:
            logging.error('JSON POST incorrect request:' + str(request.json))
            abort(400)
        if 'relation' in request.json:
            if 'sortorder' in request.json:return jsonify({'result': work_move_relation(wrk_id,request.json['id'],request.json['relation'],request.json['sortorder'])})
            else:return jsonify({'result': work_move_relation(wrk_id,request.json['id'],request.json['relation'])})
        else:
            return jsonify({'result': work_move_relation(wrk_id,request.json['id'])})
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)

#------------------------------------ subject-work related selects -----------------------
#  --------------------  all features allowed for normal users(view works and relations) below -----------------------------
@app.route(endpoint_prefix + 'subject-work-relations', methods=['GET'])
@auth.login_required
def get_subject_work_relations():
    logging.debug(auth.username() + ':servicing JSON GET All possible subject-work-relations')
    return jsonify({'relations': wsrJson})
@app.route(endpoint_prefix + 'subject-to-work', methods=['GET'])
@auth.login_required
def get_subject_relatesto_work():
    logging.debug(auth.username() + ':servicing JSON GET All subject-relates-to-work')
    return jsonify({'subject-to-work': shwJson})
@app.route(endpoint_prefix + 'subject-to-work', methods=['POST'])
@auth.login_required
def create_subject_to_work():
    if get_role(auth.username())in ['editor','admin']:
        logging.debug(auth.username() + ':servicing subject-to-work create relation')
        if not request.json or not 'subject' in request.json or not 'work' in request.json or not 'relation' in request.json:
            logging.error('JSON POST incorrect request:' + str(request.json))
            abort(400)
        return jsonify({'result': subject_work_create_relation(request.json['subject'],request.json['work'],request.json['relation'])})
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'subject-to-work', methods=['DELETE'])
@auth.login_required
def delete_subject_to_work():
    if get_role(auth.username())in ['editor','admin']:
        logging.debug(auth.username() + ':servicing subject-to-work delete relation')
        if not request.json or not 'subject' in request.json or not 'work' in request.json or not 'relation' in request.json:
            logging.error('JSON POST incorrect request:' + str(request.json))
            abort(400)
        return jsonify({'result': subject_work_delete_relation(request.json['subject'],request.json['work'],request.json['relation'])})
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'tree-subject-work/<string:subject>', methods=['GET'])
@auth.login_required
def get_tree_subject_to_work(subject):
    logging.debug(auth.username() + ':servicing JSON GET subject-work tree')
    subject_work_refreshFromdb();
    return jsonify(subject_work_add_relation(json_graph.tree_data(nx.bfs_tree(subject_work_refreshGraph(subject),subject),subject)))
@app.route(endpoint_prefix + 'tree-work-subject/<string:work>', methods=['GET'])
@auth.login_required
def get_tree_work_to_subject(work):
    logging.debug(auth.username() + ':servicing JSON GET work-subject tree')
    subject_work_refreshFromdb();
    return jsonify(work_subject_add_relation(json_graph.tree_data(nx.bfs_tree(work_subject_refreshGraph(work),work),work)))

if __name__ == '__main__':
    app.run(debug=True)