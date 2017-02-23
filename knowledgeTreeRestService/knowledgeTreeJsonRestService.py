__author__ = 'naras_mg'
# libraries
from flask import Flask, jsonify, abort, make_response, request
import json, ast, logging, peewee
import flask_httpauth
import networkx as nx
from networkx.readwrite import json_graph

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
def create_relation(subject1,subject2,relation):
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
            dict = {'subject1':subject1,'subject2':subject2,'relations':relation}
            srsJson.append(dict)
            srsNew = ktm.SubjectRelatestoSubject.create(subject1=subject1,subject2=subject2,relations=relation)
        except peewee.IntegrityError:
            print 'Failed to create relation:', dict
            return False
    return True
def delete_relation(subject1,subject2,relation):
    found = False
    for indx in range(len(srsJson)):  # find and remove the entry in Json array
        dict = srsJson[indx] #ast.literal_eval(srsJson[indx])
        # print dict
        if (dict['subject1'] == subject1) and (dict['subject2'] == subject2) and (dict['relations'] == relation):
            del srsJson[indx]
            found = True
            break;
    if not found: return False
    # if (find_item_json_dict_list(subjectsJson,'id',subject1) is None) or (find_item_json_dict_list(subjectsJson,'id',subject2) is None) or (find_item_json_dict_list(ssrJson,'id',relation) is None):
    #     return False # either of the subjects or relation not valid
    else:
        try:
            srs = ktm.SubjectRelatestoSubject.get(subject1=subject1,subject2=subject2,relations=relation)
            srs.delete_instance()
            return True
        except:
            print 'Failed to delete relation:' #, dict
            return False
def find_relation(subject1,subject2):
    for dict in srsJson:
        if (dict['subject1'] == subject1) and (dict['subject2'] == subject2):
          return dict['relations']
    return None
def find_relations(subject):  # find all relations a subject has with another subject
    relations = []
    for item in srsJson:
        dict = item #ast.literal_eval(item)
        if dict['subject2'] == subject:
            relations.append({'related': dict['subject1'], 'relations': dict['relations']})
    return relations
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
                jsonElement += "'" + fld_name + "':'" + fld_value.encode('unicode_escape').replace("'", r'\"') + "',"
        elem = jsonElement[:-1] + '}'
        # elem = ast.literal_eval(jsonElement2)
        rowsJson.append(ast.literal_eval(elem))
    return rowsJson
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
        g[row['subject1']][row['subject2']]['relation'] = row['relations']
    # logging.debug('refreshed nodes and edges from database');
    return g
def refreshFromdb():
    # logging.debug('refresh subjects and relations from db')
    subjects = ktm.Subject.select()
    subjectsJson = entity_json_dict_list(subjects)
    srs = ktm.SubjectRelatestoSubject.select()
    srsJson = entity_json_dict_list(srs)
def add_name_description(td):
    dict = find_item_json_dict_list(subjectsJson,'id',td['id'])
    if not (dict == None):
        if 'name' in dict: td['name'] = dict['name']
        if 'description' in dict: td['description'] = dict['description']
        rel = find_relations(dict['id'])
        if not (rel==[]):td['relation']=rel[0]['relations']
        if 'children' in td:
            for child in td['children']:
                child = add_name_description(child)
                # print child
    return td
def move_relation(subject,newparent,newrelation=None):  # moves a subject from one parent to another - the subtree moves
    if subject==newparent: return False

    relations=find_relations(subject)
    delete_relation(relations[0]['related'],subject,relations[0]['relations'])
    if newrelation == None: newrelation = relations[0]['relations']
    return create_relation(newparent,subject,newrelation)
logging.basicConfig(filename='knowledgeTreeJournal.log',format='%(asctime)s %(message)s',level=logging.DEBUG)

app = Flask(__name__)

db = ktm.database
db.create_tables([ktm.Subject, ktm.SubjectRelatestoSubject], safe=True)

# g.graph['subject'] = ktm.Subject.select()
subjects = ktm.Subject.select()

db = ktm.database
db.create_tables([ktm.Subject, ktm.SubjectSubjectRelation, ktm.SubjectRelatestoSubject], safe=True)

logging.debug('Opened knowledgeTree Tables - Subject, SubjectSubjectRelation, Subject-Relates-to-Subject')

subjects = ktm.Subject.select()
subjectsJson = entity_json_dict_list(subjects)
#subjectsJsonCheckPoint = subjectsJson .. can be used to change the logic to collect json creates/updates in memory and batch them to db
ssr = ktm.SubjectSubjectRelation.select()
ssrJson = entity_json_dict_list(ssr)
srs = ktm.SubjectRelatestoSubject.select()
srsJson = entity_json_dict_list(srs)
logging.debug('populated Subjects, SubjectSubjectRelation & Subject-Relates-to-Subject arrays')
g = refreshGraph();

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
#  --------------------  all features allowed for normal users(view subjects and relations) below -----------------------------
@app.route('/knowledgeTree/api/v1.0/subjects', methods=['GET'])
@auth.login_required
def get_subjects():
    logging.debug(auth.username() + ':servicing JSON GET All subjects')
    return jsonify({'subjects': subjectsJson})
@app.route('/knowledgeTree/api/v1.0/subject/<string:sub_id>', methods=['GET'])
@auth.login_required
def get_subject(sub_id):
    # sub = [sub for sub in subjectsJson if sub['id'] == str(sub_id)]
    logging.debug(auth.username() + ':servicing JSON GET: ' + sub_id)
    sub = find_item_json_dict_list(subjectsJson,'id',sub_id)
    if sub is None or len(sub) == 0:
        logging.error('JSON GET id missing: ' + sub_id)
        abort(404)
    return jsonify({'subject': sub})
@app.route('/knowledgeTree/api/v1.0/subject-subject-relations', methods=['GET'])
@auth.login_required
def get_subject_subject_relations():
    logging.debug(auth.username() + ':servicing JSON GET All subject-subject-relations')
    return jsonify({'relations': ssrJson})
@app.route('/knowledgeTree/api/v1.0/subject-to-subject', methods=['GET'])
@auth.login_required
def get_subject_relates_subject():
    logging.debug(auth.username() + ':servicing JSON GET All subject-relates-to-subject')
    return jsonify({'subject-to-subject': srsJson})
@app.route('/knowledgeTree/api/v1.0/nodes-edges', methods=['GET'])
@auth.login_required
def get_nodes_edges():
    logging.debug(auth.username() + ':servicing JSON GET nodes & edges')
    refreshFromdb()
    # g = refreshGraph()
    # write json formatted data
    # d = json_graph.node_link_data(g) # node-link format to serialize
    # write json
    return jsonify(json_graph.node_link_data(refreshGraph()))
@app.route('/knowledgeTree/api/v1.0/tree', methods=['GET'])
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
@app.route('/knowledgeTree/api/v1.0/subtree/<string:sub_id>', methods=['GET'])
@auth.login_required
def get_subtree(sub_id):
    logging.debug(auth.username() + ':servicing JSON GET sub-tree')
    refreshFromdb()
    return jsonify(add_name_description(json_graph.tree_data(nx.bfs_tree(refreshGraph(),"aum"),sub_id)))
#  --------------------  all features allowed for editors (edit, create, remove subjects and relatins) below -----------------------------
@app.route('/knowledgeTree/api/v1.0/subject-with-relation', methods=['POST'])
@auth.login_required
def create_subject_with_relation():
    if get_role(auth.username())in ['editor','admin']:
        logging.debug(auth.username() + ':servicing create subject with relation')
        if not request.json or not 'subject' in request.json or not 'related' in request.json or not 'relation' in request.json:
            logging.error('incorrect request:' + str(request.json))
            abort(400)
        dict = {"subject": request.json['subject'], "related": request.json['related'], "relation": request.json['relation']}
        subject2 = dict['subject']
        if not 'id' in subject2 or not 'name' in subject2:
            logging.error('incorrect request:' + str(subject2))
            abort(401)
        subject1id = dict['related']
        if dict.has_key('relation'): relation = dict['relation']
        else: relation = None
        if find_item_json_dict_list(subjectsJson,'id',subject1id) is None:
            return None
        if find_item_json_dict_list(subjectsJson,'id',subject2['id']) is None:
            subj = subject2 #ast.literal_eval(subject2)
            ktm.Subject.create(id=subj['id'],name=subj['name'],description=subj['description'])  # db create row
            subjectsJson.append(subject2)
        return jsonify({'subject': create_relation(subject1id,subject2['id'],relation)})
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route('/knowledgeTree/api/v1.0/subject', methods=['POST'])
@auth.login_required
def create_subject():
    if get_role(auth.username())in ['editor','admin']:
        logging.debug(auth.username() + ':servicing create subject')
        if not request.json or not 'id' in request.json or not 'name' in request.json:
            logging.error('incorrect request:' + str(request.json))
            abort(400)
        sub = {"id": request.json['id'], "name": request.json['name'], "description": request.json.get('description', "")}
        if find_item_json_dict_list(subjectsJson,'id',str(request.json['id'])) is None:
            # subj = ast.literal_eval(str(sub))
            ktm.Subject.create(id=sub['id'],name=sub['name'],description=sub['description'])  # db create row
            subjectsJson.append(sub)
            return jsonify({'subject': sub}), 201
        else:
            sub = {"id-duplicate": request.json['id'], "name": request.json['name'], "description": request.json.get('description', "")}
            return jsonify({'subject': sub}), 409
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route('/knowledgeTree/api/v1.0/subject/<string:sub_id>', methods=['PUT'])
@auth.login_required
def update_subject(sub_id):
    if get_role(auth.username())in ['editor','admin']:
        logging.debug(auth.username() + ':servicing update subject: ' + sub_id)
        if (not request.json) or ('name' in request.json and type(request.json['name']) != unicode) or ('description' in request.json and type(request.json['description']) is not unicode):
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
                return jsonify({'subject': dict}), 201
        logging.error('JSON PUT: id missing - ',sub_id)
        abort(404)  # not found
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route('/knowledgeTree/api/v1.0/subject-with-relation/<string:sub_id>', methods=['DELETE'])
@auth.login_required
def delete_subject_with_relation(sub_id):
    if get_role(auth.username())in ['editor','admin']:
        logging.debug(auth.username() + ':servicing delete subject with relation: ' + sub_id)
        relations = find_relations(sub_id)
        for subject_with_relation in relations:
            subject1 = subject_with_relation['related']
            relation = subject_with_relation['relations']
            delete_relation(subject1,sub_id,relation)# each relation with another subject1 removed
        for subj_index in range(len(subjectsJson)): # remove subject from db & Json list
                subj_as_dict = subjectsJson[subj_index] #ast.literal_eval(subjectsJson[subj_index])
                if subj_as_dict['id'] == sub_id or subj_as_dict[u'id'] == sub_id:
                    subjdbrow = ktm.Subject.get(ktm.Subject.id == subj_as_dict['id'])   # db get/delete row
                    subjdbrow.delete_instance()
                    del subjectsJson[subj_index]
                    break
        return jsonify({'result': True})
@app.route('/knowledgeTree/api/v1.0/subject/<string:sub_id>', methods=['DELETE'])
@auth.login_required
def delete_subject(sub_id):
    if get_role(auth.username())in ['editor','admin']:
        logging.debug(auth.username() + 'servicing delete subject: ' + sub_id)
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
@app.route('/knowledgeTree/api/v1.0/subject-to-subject', methods=['POST'])
@auth.login_required
def create_subject_to_subject():
    if get_role(auth.username())in ['editor','admin']:
        logging.debug(auth.username() + ':servicing subject-to-subject create relation')
        if not request.json or not 'subject1' in request.json or not 'subject2' in request.json or not 'relation' in request.json:
            logging.error('JSON POST incorrect request:' + str(request.json))
            abort(400)
        return jsonify({'result': create_relation(request.json['subject1'],request.json['subject2'],request.json['relation'])})
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route('/knowledgeTree/api/v1.0/subject-to-subject', methods=['DELETE'])
@auth.login_required
def delete_subject_to_subject():
    if get_role(auth.username())in ['editor','admin']:
        logging.debug(auth.username() + ':servicing subject-to-subject delete relation')
        if not request.json or not 'subject1' in request.json or not 'subject2' in request.json or not 'relation' in request.json:
            logging.error('JSON POST incorrect request:' + str(request.json))
            abort(400)
        return jsonify({'result': delete_relation(request.json['subject1'],request.json['subject2'],request.json['relation'])})
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route('/knowledgeTree/api/v1.0/subject-move/<string:sub_id>', methods=['POST'])
@auth.login_required
def move_subject(sub_id):
    if get_role(auth.username())in ['editor','admin']:
        logging.debug(auth.username() + ':servicing subject-to-subject move relation')
        if not request.json or not 'id' in request.json:
            logging.error('JSON POST incorrect request:' + str(request.json))
            abort(400)
        if 'relation' in request.json:
            return jsonify({'result': move_relation(sub_id,request.json['id'],request.json['relation'])})
        else:
            return jsonify({'result': move_relation(sub_id,request.json['id'])})
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route('/knowledgeTree/api/v1.0/shutdown', methods=['POST'])
@auth.login_required
def shutdown():
    if get_role(auth.username())=='admin':
        shutdown_server()
        return jsonify({'result':'Server shutting down...'});
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)

if __name__ == '__main__':
    app.run(debug=True)