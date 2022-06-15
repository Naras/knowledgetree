__author__ = 'naras_mg'
# libraries
from flask import Flask, jsonify, abort, make_response, request
import json, ast, logging, peewee, flask_httpauth
import networkx as nx
from networkx.readwrite import json_graph
import random, string
from datetime import datetime
import copy
from flask_cors import CORS, cross_origin

auth = flask_httpauth.HTTPBasicAuth()
def ceasar(plain, shift):  # shift each letter by shift
        return "".join([chr((ord(x)- start(x) + shift) % 26 + start(x)) for (x) in list(plain)])
def start(alphabet): # find distance between alphabet and 'a' or 'A'
            strt = ord('a') if alphabet.islower() else ord('A')
            return strt
@auth.get_password
def get_password(username):
    auths = json.load(open("credentials_roles.txt"))
    if username in auths:
        return ceasar(auths[username]["pw"],10)
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
            with ktm.database.atomic() as trans:
                srsNew = ktm.SubjectRelatestoSubject.create(subject1=subject1,subject2=subject2,relation=relation,sortorder=sortorder)
                srsJson.append(dict)
        except peewee.IntegrityError:
            trans.rollback()
            logging.error('%s:Failed to create relation-%s'%(auth.username(), dict))
            return False
    return True
def update_relation(subject2,relation=None,sortorder=None):
    # subject1 = find_relations(subject2)   # a list of subject1s - usually only one expected
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
            logging.error('%s:Failed to update relation - %s'%(auth.username(), dict))
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
        except Exception as e:
            logging.error('%s :Failed to delete relation - %s exception %s' %(auth.username(), dict, e))
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
        db_flds = row.__dict__['__data__']  # get all the db field names/values .. a dictionary
        jsonElement = '{'
        for fld_name,fld_value in db_flds.items():
            if not fld_value is None:
                # print ('name:'+fld_name + ' value:'+fld_value)
                withoutCRLF = str(fld_value).replace('\r\n','')
                withoutCRLF = withoutCRLF.replace('\n','')
                withoutCRLF = withoutCRLF.replace("'", r'\"')
                # if fld_name == 'description':
                #     logging.debug(auth.username() + withoutCRLF)
                jsonElement += "'" + fld_name + "':'" + withoutCRLF + "',"  # escape /r/n
        elem = jsonElement[:-1] + '}'
        # elem = ast.literal_eval(jsonElement2)
        # print elem
        rowsJson.append(ast.literal_eval(elem))
    return rowsJson
def move_relation(subject, newparent, newrelation=None, sortorder=None):  # moves a subject from one parent to another - the subtree moves
    try:
        relations = find_relations(subject)
        if relations != None and relations[0] != None: delete_relation(relations[0]['related'],subject,relations[0]['relation'])
        if newrelation == None: newrelation = relations[0]['relation']
    except Exception as e:
        logging.error('%s :move subject - Failed to delete relation - %s exception %s'%(auth.username(), subject, e))
    return create_relation(newparent, subject, newrelation, sortorder)
def add_name_description(td):
    dictionary = find_item_json_dict_list(subjectsJson,'id',td['id'])
    if not (dictionary == None):
        if 'name' in dictionary: td['name'] = dictionary['name']
        if 'description' in dictionary: td['description'] = dictionary['description']
        parent = find_item_json_dict_list(srsJson,'subject2',td['id']);
        if not (parent == None): td['parent'] = parent;
        rel = find_relations(dictionary['id'])
        if not (rel == []):
            td['relation'] = rel[0]['relation']
            if 'sortorder' in rel[0]: td['sortorder'] = rel[0]['sortorder']
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
        g.nodes[row['id']]['name'] = row['name']
        if 'description' in row: g.nodes[row['id']]['description'] = row['description']
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
def copy_subject(id,target):  # copy a source to a target parent
    row_subject = find_item_json_dict_list(subjectsJson,'id',id)
    if row_subject is None: return None
    row_srs = find_item_json_dict_list(srsJson,'subject2',id)
    if row_srs is None: return None
    newsubject = copy.copy(row_subject)
    newsubject['id'] = (id  + ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(16)))[0:19]
    try:
        ktm.Subject.create(id=newsubject['id'], name=newsubject['name'], description=newsubject['description'])  # db create row
        subjectsJson.append(newsubject)
    except peewee.IntegrityError:
        logging.error('%s :Failed to create new copy of subject- %s %s'%(auth.username(), row_subject['id'], row_subject['name']))
    return create_relation(target,newsubject['id'],row_srs['relation'],row_srs['sortorder'])
def copy_children(id,target):
    children = []
    for item in srsJson:
        if item['subject1'] == id: children.append(item)
    for child in children:
        result = copy_subject(child['subject2'], target)
        copy_children(child['subject2'],target)
    return children
def delete_children(id):
    children = []
    for item in srsJson:
        if item['subject1'] == id:
            children.append(item)
    for child in children: delete_children(child['subject2'])
    relations = find_relations(id)
    for subject_with_relation in relations:
        subject1 = subject_with_relation['related']
        relation = subject_with_relation['relation']
        delete_relation(subject1, id, relation)  # each relation with another subject1 removed
    # check if subject has work connections and remove them
    relations = find_subject_allwork_relations(id)
    for dict in relations: subject_work_delete_relation(dict['subject'],dict['work'],dict['relation'])
    for subj_index in range(len(subjectsJson)):  # remove subject from db & Json list
        subj_as_dict = subjectsJson[subj_index]  # ast.literal_eval(subjectsJson[subj_index])
        if subj_as_dict['id'] == id or subj_as_dict[u'id'] == id:
            subjdbrow = ktm.Subject.get(ktm.Subject.id == subj_as_dict['id'])  # db get/delete row
            subjdbrow.delete_instance()
            del subjectsJson[subj_index]
            break
    return True
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
    if (find_item_json_dict_list(worksJson,'id',work1) is None) or (find_item_json_dict_list(worksJson,'id',work2) is None) or (find_item_json_dict_list(wwrJson,'id',relation) is None):
        return False  # either of the works or relation not valid
    elif work_find_relation(work1,work2) is not None:  # works are already related
        return False
    else:
        try:
            dict = {'work1':work1,'work2':work2,'relation':relation,'sortorder':sortorder}
            with ktm.database.atomic() as trans:
                wrwNew = ktm.WorkRelatestoWork.create(work1=work1,work2=work2,relation=relation,sortorder=sortorder)
                wrwJson.append(dict)
        except peewee.IntegrityError:
            trans.rollback()
            logging.error('%s: Failed to create work relation - %s'%(auth.username(), dict))
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
            logging.error('%s :Failed to update work relation - %s'%(auth.username(), dict))
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
            logging.error('%s :Failed to delete work relation- %s'%(auth.username(), dict))
            return False
def work_refreshGraph():
    g = nx.Graph()
    for row in worksJson:
        g.add_node(row['id'])
        g.nodes[row['id']]['name'] = row['name']
        if 'description' in row: g.nodes[row['id']]['description'] = row['description']
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
        parent = find_item_json_dict_list(wrwJson,'work2',td['id']);
        if not (parent == None): td['parent'] = parent;
        rel = work_find_relations(dict['id'])
        if not (rel==[]):
            td['relation']=rel[0]['relation']
            if 'sortorder' in rel[0]: td['sortorder']=rel[0]['sortorder']
        if 'children' in td:
            for child in td['children']:
                child = work_add_name_description(child)
    return td
def work_move_relation(work,newparent,newrelation=None,sortorder=None):  # moves a work from one parent to another - the subtree moves
    try:
        relations=work_find_relations(work)
        if relations != None and relations[0] != None: work_delete_relation(relations[0]['related'],work,relations[0]['relation'])
        if newrelation == None: newrelation = relations[0]['relation']
    except Exception as e:
        logging.error('%s :move work - Failed to delete relation - %s exception %s'%(auth.username(), work, e))
    return work_create_relation(newparent,work,newrelation,sortorder)

def find_subject_work_relations(subject,work):
    relations = []
    for dict in shwJson:
        if dict['subject'] == subject and dict['work'] == work:
            # print dict
            relations.append(dict)
    return relations
def find_subject_allwork_relations(subject):
    relations = []
    for dict in shwJson:
        if dict['subject'] == subject:
            # print dict
            relations.append(dict)
    return relations
def find_work_allsubject_relations(work):
    relations = []
    for dict in shwJson:
        if dict['work'] == work:
            # print dict
            relations.append(dict)
    return relations
def subject_work_create_relation(subject, work, relation):
    if find_subject_work_relations(subject, work) != []:  # subject/work are already related
        return False
    else:
        try:
            dict = {'subject': subject, 'work': work, 'relation': relation}
            shwJson.append(dict)
            # print 'creating subject_work relation:'+ dict['subject'] + '-'+ dict['work'] + '-'+relation
            ktm.SubjectHasWork.create(subject=subject, work=work, relation=relation)
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
def copy_work(id,target):  # copy a source to a target parent
    row_work = find_item_json_dict_list(worksJson,'id',id)
    if row_work is None: return None
    row_wrw = find_item_json_dict_list(wrwJson,'work2',id)
    if row_wrw is None: return None
    newwork = copy.copy(row_work)
    newwork['id'] = (id  + ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(16)))[0:19]
    try:
        ktm.Work.create(id=newwork['id'], name=newwork['name'], description=newwork['description'])  # db create row
        worksJson.append(newwork)
    except peewee.IntegrityError:
        logging.error('%s: Failed to create new copy of work - %s %s'%(auth.username(), row_work['id'], row_work['name']))
    return work_create_relation(target,newwork['id'],row_wrw['relation'],row_wrw['sortorder'])
def work_copy_children(id,target):
    children = []
    for item in wrwJson:
        if item['work1'] == id: children.append(item)
    for child in children:
        copy_work(child['work2'], target)
        work_copy_children(child['work2'],target)
    return children
def work_delete_children(id):
    children = []
    for item in wrwJson:
        if item['work1'] == id:
            children.append(item)
    for child in children: work_delete_children(child['work2'])
    relations = work_find_relations(id)
    for work_with_relation in relations:
        work1 = work_with_relation['related']
        relation = work_with_relation['relation']
        work_delete_relation(work1, id, relation)  # each relation with another work1 removed
    # check if work has subject  connections and remove them
    relations = find_work_allsubject_relations(id)
    for dict in relations: subject_work_delete_relation(dict['subject'],dict['work'],dict['relation'])
    # check if work has person connections and remove them
    relations = find_work_allperson_relations(id)
    for dict in relations: person_work_delete_relation(dict['person'],dict['work'],dict['relation'])
    for work_index in range(len(worksJson)):  # remove subject   from db & Json list
        work_as_dict = worksJson[work_index]  # ast.literal_eval(subjectsJson[subj_index])
        if work_as_dict['id'] == id or work_as_dict[u'id'] == id:
            workdbrow = ktm.Work.get(ktm.Work.id == work_as_dict['id'])  # db get/delete row
            workdbrow.delete_instance()
            del worksJson[work_index]
            break
    return True

def person_find_relation(person1,person2):
    for dict in prpJson:
        # dict = item #ast.literal_eval(item)
        if (dict['person1'] == person1) and (dict['person2'] == person2):
          return dict['relation']
    return None
def person_find_relations(person):  # find all relations a person has with another person
    relations = []
    for item in prpJson:
        dict = item #ast.literal_eval(item)
        if dict['person2'] == person:
            # print dict
            dictitem = {'related': dict['person1'], 'relation': dict['relation']}
            relations.append(dictitem)
    return relations

def person_create_relation(person1,person2,relation):
    if (find_item_json_dict_list(personsJson,'id',person1) is None) or (find_item_json_dict_list(personsJson,'id',person2) is None) or (find_item_json_dict_list(pprJson,'id',relation) is None):
        return False  # either of the persons or relation not valid
    elif person_find_relation(person1,person2) is not None:  # persons are already related
        return False
    else:
        try:
            dict = {'person1':person1,'person2':person2,'relation':relation}
            with ktm.database.atomic() as trans:
                ktm.PersonRelatestoPerson.create(person1=person1,person2=person2,relation=relation)
                prpJson.append(dict)
        except peewee.IntegrityError:
            trans.rollback()
            logging.error('%s:Failed to create person relation-%s'%(auth.username(), dict))
            return False
    return True
def person_update_relation(person2,relation=None):
    person1 = person_find_relations(person2)[0]['related']   # a list of person1s - usually only one expected
    if (find_item_json_dict_list(personsJson,'id',person1) is None) or (find_item_json_dict_list(personsJson,'id',person2) is None) \
            or (find_item_json_dict_list(wwrJson,'id',relation) is None):
        return False  # either of the persons or relation not valid
    else:
        try:
            # update the person relations on the db
            person_replace_relation(person1,person2,relation)
            prpNew = ktm.PersonRelatestoPerson.get(ktm.PersonRelatestoPerson.person1==person1,ktm.PersonRelatestoPerson.person2==person2)
            if relation is not None:prpNew.relation = relation
            prpNew.save()
        except peewee.IntegrityError:
            logging.error('%s:Failed to update person relation- %s'%(auth.username(), dict))
            return False
    return True
def person_replace_relation(person1,person2,relation=None):
    for dict in prpJson:
        if (dict['person1'] == person1) and (dict['person2'] == person2):
          if relation is not None: dict['relation'] = relation
          return dict
    return None
def person_delete_relation(person1,person2,relation):
    found = False
    for indx in range(len(wrwJson)):  # find and remove the entry in Json array
        dict = prpJson[indx] #ast.literal_eval(wrwJson[indx])
        # print dict
        if (dict['person1'] == person1) and (dict['person2'] == person2) and (dict['relation'] == relation):
            del prpJson[indx]
            found = True
            break;
    if not found: return False
    # if (find_item_json_dict_list(personsJson,'id',person1) is None) or (find_item_json_dict_list(personsJson,'id',person2) is None) or (find_item_json_dict_list(wwrJson,'id',relation) is None):
    #     return False # either of the persons or relation not valid
    else:
        try:
            prp = ktm.PersonRelatestoPerson.get(person1=person1,person2=person2,relation=relation)
            prp.delete_instance()
            return True
        except:
            logging.error('%s:Failed to delete person relation-%s'%(auth.username(), prp.id))  #, dict
            return False
def person_refreshGraph():
    g = nx.Graph()
    for row in personsJson:
        g.add_node(row['id'])
        # if 'first' in row: g.nodes_id[row['id']]['first'] = row['first']
        # if 'last' in row: g.nodes_id[row['id']]['last'] = row['last']
        # if 'middle' in row: g.nodes_id[row['id']]['middle'] = row['middle']
        # if 'nick' in row: g.nodes_id[row['id']]['nick'] = row['nick']
        # if 'other' in row: g.nodes_id[row['id']]['other'] = row['other']
    for row in prpJson:
        g.add_edge(row['person1'],row['person2'])
        g[row['person1']][row['person2']]['relation'] = row['relation']
        # print g[row['person1']][row['person2']]
    return g
def person_refreshFromdb():
    # logging.debug('refresh works and relations from db')
    persons = ktm.Person.select()
    personsJson = entity_json_dict_list(persons)
    prp = ktm.PersonRelatestoPerson.select()
    prpJson = entity_json_dict_list(prp)
def person_add_names(td):
    dict = find_item_json_dict_list(personsJson,'id',td['id'])
    if not (dict == None):
        if 'first' in dict: td['first'] = dict['first']
        if 'last' in dict: td['last'] = dict['last']
        if 'middle' in dict: td['middle'] = dict['middle']
        if 'nick' in dict: td['nick'] = dict['nick']
        if 'other' in dict: td['other'] = dict['other']
        if 'living' in dict: td['living'] = dict['living']
        if 'birth' in dict: td['birth'] = dict['birth']
        if 'death' in dict: td['death'] = dict['death']
        if 'biography' in dict: td['biography'] = dict['biography']
        parent = find_item_json_dict_list(prpJson,'person2',td['id']);
        if not (parent == None): td['parent'] = parent;
        rel = person_find_relations(dict['id'])
        if not (rel==[]):
            td['relation']=rel[0]['relation']
        if 'children' in td:
            for child in td['children']:
                child = person_add_names(child)
    return td
def person_move_relation(person,newparent,newrelation=None):  # moves a person from one parent to another - the subtree moves
    try:
        relations=person_find_relations(person)
        if relations != None and relations[0] != None: person_delete_relation(relations[0]['related'],person,relations[0]['relation'])
        if newrelation == None: newrelation = relations[0]['relation']
    except Exception as e:
        logging.error('%s :move person - Failed to delete relation - %s exception %s'%(auth.username(), person, e))
    return person_create_relation(newparent,person,newrelation)

def find_person_work_relations(person,work):
    relations = []
    for dict in phwJson:
        if dict['person'] == person and dict['work'] == work:
            relations.append(dict)
    return relations
def find_person_allwork_relations(person):
    relations = []
    for dict in phwJson:
        if dict['person'] == person:
            relations.append(dict)
    return relations
def find_work_allperson_relations(work):
    relations = []
    for dict in phwJson:
        if dict['work'] == work:
            relations.append(dict)
    return relations
def person_work_create_relation(person,work,relation):
    if find_person_work_relations(person,work) != []:  # person/work are already related
        return False
    else:
        try:
            dict = {'person':person,'work':work,'relation':relation}
            phwJson.append(dict)
            # print 'creating person_work relation:'+ dict['person'] + '-'+ dict['work'] + '-'+relation
            ktm.PersonHasWork.create(person=person,work=work,relation=relation)
            return True
        except peewee.IntegrityError:
                logging.error('%s:Failed to create person-work relation- %s'%(auth.username(), dict))
                return False
def person_work_delete_relation(person,work,relation):
    found = False
    for indx in range(len(phwJson)):  # find and remove the entry in Json array
        dict = phwJson[indx] #ast.literal_eval(srsJson[indx])
        # print dict
        if (dict['person'] == person) and (dict['work'] == work) and (dict['relation'] == relation):
            del phwJson[indx]
            found = True
            break;
    if not found: return False
    # if (find_item_json_dict_list(personsJson,'id',person1) is None) or (find_item_json_dict_list(personsJson,'id',person2) is None) or (find_item_json_dict_list(ssrJson,'id',relation) is None):
    #     return False # either of the persons or relation not valid
    else:
        try:
            # shw = ktm.PersonHasWork.get(person=person,work=work,relation=relation)
            # shw.delete_instance()
            qry = ktm.PersonHasWork.delete().where(ktm.PersonHasWork.person==person,ktm.PersonHasWork.work==work,ktm.PersonHasWork.relation==relation)
            qry.execute()
            return True
        except:
            logging.error('%s :Failed to delete person-work relation-'+ person + '-' + work + '- %s'%(auth.username(), relation))  #, dict
            return False
def person_work_refreshFromdb():
    # logging.debug('refresh subject-to=worksfrom db')
    phw = ktm.PersonHasWork.select()
    phwJson = entity_json_dict_list(phw)
def person_work_refreshGraph(person):
    g = nx.Graph()
    for row in phwJson:
        if row['person']==person:
            g.add_node(row['person'])
            if row['person'] == row['work']: wrk=row['work']+'_pramaaNa'
            else: wrk=row['work']
            g.add_node(wrk)
            g.add_edge(row['person'],wrk)
            g[row['person']][wrk]['relation'] = row['relation']
    if g.number_of_edges()==0:g.add_node(person) # no work relatons for this person
    return g
def work_person_refreshGraph(work):
    g = nx.Graph()
    for row in phwJson:
        if row['work']==work:
            if row['person'] == row['work']: sub=row['person']+'_pramatha'
            else: sub=row['person']
            g.add_node(sub)
            g.add_node(row['work'])
            g.add_edge(row['work'],sub)
            g[row['work']][sub]['relation'] = row['relation']
            break;
    if g.number_of_edges()==0:g.add_node(work) # no person relatons for this work
    return g
def person_work_add_relation(td):
    # print td
    for elem in td['children']:
        dict = find_item_json_dict_list(phwJson,'work',elem['id'])
        if not (dict == None):
            if 'relation' in dict: elem['relation'] = dict['relation']
    return td
def work_person_add_relation(td):
    # print td
    for elem in td['children']:
        dict = find_item_json_dict_list(phwJson,'person',elem['id'])
        if not (dict == None):
            if 'relation' in dict: elem['relation'] = dict['relation']
    return td

logging.basicConfig(filename='knowledgeTreeJournal.log',format='%(asctime)s %(message)s',level=logging.DEBUG)

app = Flask(__name__)

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
shwJson = entity_json_dict_list(shw)

# person related entities
ppr = ktm.PersonPersonRelation.select()
pprJson = entity_json_dict_list(ppr)
prp = ktm.PersonRelatestoPerson.select()
prpJson = entity_json_dict_list(prp)
persons = ktm.Person.select()
personsJson = entity_json_dict_list(persons)

# person-work cross related entities
pwr = ktm.PersonWorkRelation.select()
pwrJson = entity_json_dict_list(pwr)
phw = ktm.PersonHasWork.select()
phwJson= entity_json_dict_list(phw)

logging.debug('populated Subject, Work, Person  and related in-memory tables')
gs = refreshGraph()
gw = work_refreshGraph()
gp = person_refreshGraph()

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
@cross_origin()
def get_subjects():
    logging.debug('%s:servicing JSON GET All subjects'%auth.username())
    return jsonify({'subjects': subjectsJson})
@app.route(endpoint_prefix + 'subject/<string:sub_id>', methods=['GET'])
@auth.login_required
@cross_origin()
def get_subject(sub_id):
    # sub = [sub for sub in subjectsJson if sub['id'] == str(sub_id)]
    logging.debug('%s:servicing JSON GET: %s'%(auth.username(), sub_id))
    sub = find_item_json_dict_list(subjectsJson,'id',sub_id)
    if sub is None or len(sub) == 0:
        logging.error('%s:JSON GET id missing- %s'%(auth.username(), sub_id))
        abort(404)
    return jsonify({'subject': sub})
@app.route(endpoint_prefix + 'subject-subject-relations', methods=['GET'])
@auth.login_required
@cross_origin()
def get_subject_subject_relations():
    logging.debug('%s:servicing JSON GET All subject_subject_relations'%auth.username())
    return jsonify({'relations': ssrJson})
@app.route(endpoint_prefix + 'subject-to-subject', methods=['GET'])
@auth.login_required
@cross_origin()
def get_subject_relates_subject():
    logging.debug('%s:servicing JSON GET All subject-relates-to-subject'%auth.username())
    return jsonify({'subject-to-subject': srsJson})
@app.route(endpoint_prefix + 'nodes-edges', methods=['GET'])
@auth.login_required
@cross_origin()
def get_nodes_edges():
    logging.debug('%s:servicing JSON GET nodes & edges'%auth.username())
    refreshFromdb()
    # g = refreshGraph()
    # write json formatted data
    # d = json_graph.node_link_data(g) # node-link format to serialize
    # write json
    return jsonify(json_graph.node_link_data(refreshGraph()))
@app.route(endpoint_prefix + 'tree', methods=['GET'])
@auth.login_required
@cross_origin()
def get_tree():
    logging.debug('%s:servicing JSON GET tree'%auth.username())
    refreshFromdb()
    # g = refreshGraph()
    # write json formatted data
    # t = nx.bfs_tree(g,"aum")
    # treedata = json_graph.tree_data(t,"aum")
    # write json
    return jsonify(add_name_description(json_graph.tree_data(nx.bfs_tree(refreshGraph(),"aum"),"aum")))
@app.route(endpoint_prefix + 'subtree/<string:sub_id>', methods=['GET'])
@auth.login_required
@cross_origin()
def get_subtree(sub_id):
    logging.debug('%s:servicing JSON GET sub-tree for <%s>'%(auth.username(), sub_id))
    refreshFromdb()
    return jsonify(add_name_description(json_graph.tree_data(nx.bfs_tree(refreshGraph(),"aum"),sub_id)))
#  --------------------  all features allowed for editors (edit, create, remove subjects and relatins) below -----------------------------
@app.route(endpoint_prefix + 'subject-with-relation', methods=['POST'])
@auth.login_required
def create_subject_with_relation():
    if get_role(auth.username()) in ['editor','admin']:
        logging.debug('%s:servicing create subject with relation:'%auth.username())
        if not request.json or not 'subject' in request.json or not 'related' in request.json or not 'relation' in request.json:
            logging.error('%s:incorrect request- %s'%(auth.username(), request.json))
            abort(400)
        if 'sortorder' in request.json: dict = {"subject": request.json['subject'], "related": request.json['related'], "relation": request.json['relation'],'sortorder':request.json['sortorder']}
        else: dict = {"subject": request.json['subject'], "related": request.json['related'], "relation": request.json['relation']}
        subject2 = dict['subject']
        if not 'id' in subject2 or not 'name' in subject2 or subject2['id'] == ''  or subject2['name'] == '':
            logging.error('%s:incorrect request- %s'%(auth.username(), subject2))
            abort(400)
        subject1id = dict['related']
        if 'relation' in dict: relation = dict['relation']
        else: relation = None
        if 'sortorder' in dict:
            sortorder = dict['sortorder']
            if sortorder=='': sortorder = None
        else: sortorder = None
        if find_item_json_dict_list(subjectsJson,'id',subject1id) is None:  # no subject1
            return None
        if find_item_json_dict_list(subjectsJson,'id',subject2['id']) is not None:
            # duplicate subject2 id .. generate a random id suffix and concatenate
            subject2['id'] = (subject2['id'] + ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(16)))[0:19]
        # subj = subject2 #ast.literal_eval(subject2)
        try:
            with ktm.database.atomic() as trans:
                ktm.Subject.create(id=subject2['id'],name=subject2['name'],description=subject2['description'])  # db create row
                subjectsJson.append(subject2)
                response = create_relation(subject1id,subject2['id'],relation=relation,sortorder=sortorder)
                if not response:
                    trans.rollback()
                    logging.error('%s:Failed to create subject-%s'%(auth.username(), subject2))
                return jsonify({'subject': response})
        except peewee.IntegrityError:
            trans.rollback()
            logging.error('%s:Failed to create subject- %s'%(auth.username(), subject2))
            return jsonify({'subject': False}), 409
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'subject', methods=['POST'])
@auth.login_required
def create_subject():
    if get_role(auth.username())in ['editor','admin']:
        logging.debug('%s:servicing create subject'%auth.username())
        if not request.json or not 'id' in request.json or not 'name' in request.json:
            logging.error('%s:incorrect request- %s'%(auth.username(), request.json))
            abort(400)
        subject = {"id": request.json['id'], "name": request.json['name'], "description": request.json.get('description', "")}
        if find_item_json_dict_list(subjectsJson,'id',str(request.json['id'])) is not None:
            # subj = ast.literal_eval(str(sub))
            # generate a random string and concatenate - changes id to unique 20-char string
            subject['id'] = (subject['id'] + ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(16)))[0:19]
        try:
            ktm.Subject.create(id=subject['id'],name=subject['name'],description=subject['description'])  # db create row
            subjectsJson.append(subject)
            return jsonify({'subject': subject}), 201
        except peewee.IntegrityError:
            logging.error('%s:Failed to create subject- %s'%(auth.username(), subject['id']))
            return jsonify({'subject': subject}), 409
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'subject/<string:sub_id>', methods=['PUT'])
@auth.login_required
def update_subject(sub_id):
    if get_role(auth.username())in ['editor','admin']:
        logging.debug('%s:servicing update subject:%s'%(auth.username(), sub_id))
        if (not request.json):
            logging.error('%s:JSON PUT error incorrect request- %s'%(auth.username(), request.json))
            abort(400)
        for index in range(len(subjectsJson)):
            # json_acceptable_string = subjectsJson[index].replace("'", "\"")
            dict = subjectsJson[index] #ast.literal_eval(subjectsJson[index])
            if dict['id'] == sub_id:
                dict['name'] = request.json.get('name', '')
                dict['description'] = request.json.get('description', '')
                subjectsJson[index] = dict #json.dumps(dict)
                try:
                    subj = ktm.Subject.get(ktm.Subject.id == sub_id)   # db get/update row
                    subj.name = dict['name']
                    subj.description = dict['description']
                    subj.save()
                    if 'relation' in request.json or 'sortorder' in request.json:  # modify subject_to_subject if any change to relation or sort order
                        update_relation(sub_id,request.json.get('relation', None),int(request.json.get('sortorder', None)))
                    return jsonify({'subject': dict}), 201
                except peewee.IntegrityError:
                    logging.error('%s:Failed to update subject- %s'%(auth.username(), subj['id']))
                    return jsonify({'subject': subj}), 409
        logging.error('%s:JSON PUT: id missing- %s'%(auth.username(), sub_id))
        abort(404)  # not found
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'subject-with-relation/<string:sub_id>', methods=['DELETE'])
@auth.login_required
def delete_subject_with_relation(sub_id):
    if get_role(auth.username())in ['editor','admin']:
        logging.debug('%s:servicing delete subject with relation:%s'%(auth.username(), sub_id))
        relations = find_relations(sub_id)
        for subject_with_relation in relations:
            subject1 = subject_with_relation['related']
            relation = subject_with_relation['relation']
            delete_relation(subject1,sub_id,relation)# each relation with another subject1 removed
        for subj_index in range(len(subjectsJson)): # remove subject from db & Json list
                subj_as_dict = subjectsJson[subj_index] #ast.literal_eval(subjectsJson[subj_index])
                if subj_as_dict['id'] == sub_id or subj_as_dict[u'id'] == sub_id:
                    try:
                        subjdbrow = ktm.Subject.get(ktm.Subject.id == subj_as_dict['id'])  # db get/delete row
                        subjdbrow.delete_instance()
                        del subjectsJson[subj_index]
                    except peewee.IntegrityError:
                        logging.error('%s:Failed to delete subject with relation- %s'%(auth.username(), sub_id))
                        return jsonify({'result': False}), 409
                    break
        return jsonify({'result': True})
@app.route(endpoint_prefix + 'subject/<string:sub_id>', methods=['DELETE'])
@auth.login_required
def delete_subject(sub_id):
    if get_role(auth.username()) in ['editor','admin']:
        logging.debug('%s:servicing delete subject:%s'%(auth.username(), sub_id))
        sub = find_item_json_dict_list(subjectsJson,'id',sub_id)
        if sub is None or len(sub) == 0:
            logging.error('%s:incorrect request- %s'%(auth.username(), request.json))
            abort(404)
        # if len(sub) == 0:
        #     return False
        for subj_index in range(len(subjectsJson)):
            subj_as_dict = subjectsJson[subj_index] #ast.literal_eval(subjectsJson[subj_index])
            if (subj_as_dict['id'] == sub['id'] or subj_as_dict[u'id'] == sub['id'] or subj_as_dict['id'] == sub[u'id']) :
                try:
                    subj = ktm.Subject.get(ktm.Subject.id == subj_as_dict['id'])   # db get/delete row
                    subj.delete_instance()
                    del subjectsJson[subj_index]
                except peewee.IntegrityError:
                    logging.error('%s:Failed to delete subject - %s'%(auth.username(), subj.id))
                    return jsonify({'subject': subj.id, 'status': 'Failed'}), 409
                break
        return jsonify({'result': True})
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'subject-to-subject', methods=['POST'])
@auth.login_required
def create_subject_to_subject():
    if get_role(auth.username())in ['editor','admin']:
        logging.debug('%s:servicing subject-to-subject create relation'%auth.username())
        if not request.json or not 'subject1' in request.json or not 'subject2' in request.json or not 'relation' in request.json:
            logging.error('%s:JSON POST incorrect request- %s'%(auth.username(), request.json))
            abort(400)
        return jsonify({'result': create_relation(request.json['subject1'],request.json['subject2'],request.json['relation'])})
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'subject-to-subject', methods=['DELETE'])
@auth.login_required
def delete_subject_to_subject():
    if get_role(auth.username())in ['editor','admin']:
        logging.debug('%s:servicing subject-to-subject delete relation'%auth.username())
        if not request.json or not 'subject1' in request.json or not 'subject2' in request.json or not 'relation' in request.json:
            logging.error('%s:JSON POST incorrect request- %s'%(auth.username(), request.json))
            abort(400)
        return jsonify({'result': delete_relation(request.json['subject1'],request.json['subject2'],request.json['relation'])})
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'subject-move/<string:sub_id>', methods=['POST'])
@auth.login_required
def move_subject(sub_id):
    if get_role(auth.username()) in ['editor','admin']:
        logging.debug('%s:servicing subject-to-subject move subject'%auth.username())
        if not request.json or not 'id' in request.json:
            logging.error('%s:JSON POST incorrect request- %s'%(auth.username(), request.json))
            abort(400)
        if 'relation' in request.json:
            if 'sortorder' in request.json:return jsonify({'result': move_relation(sub_id, request.json['id'], request.json['relation'],request.json['sortorder'])})
            else:return jsonify({'result': move_relation(sub_id,request.json['id'],request.json['relation'])})
        else:
            return jsonify({'result': move_relation(sub_id,request.json['id'])})
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'subject-copy/<string:sub_id>', methods=['POST'])
@auth.login_required
def copy_subtree(sub_id):
    if get_role(auth.username())in ['editor','admin']:
        logging.debug('%s:servicing subject copy subtree: %s to %s'%(auth.username(), sub_id, request.json['id']))
        if not request.json or not 'id' in request.json:
            logging.error('%s:JSON POST incorrect request- %s'%(auth.username(), request.json))
            abort(400)
        return jsonify({'result': copy_children(sub_id,request.json['id'])})
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'subtree/<string:sub_id>', methods=['DELETE'])
@auth.login_required
def remove_subtree(sub_id):
    if get_role(auth.username())in ['editor','admin']:
        logging.debug('%s:servicing remove subtree%s'%(auth.username(), sub_id))
        return jsonify({'result': delete_children(sub_id)})
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
@cross_origin()
def get_works():
    logging.debug('%s:servicing JSON GET All works'%auth.username())
    return jsonify({'works': worksJson})
@app.route(endpoint_prefix + 'work/<string:wrk_id>', methods=['GET'])
@auth.login_required
@cross_origin()
def get_work(wrk_id):
    # sub = [sub for sub in subjectsJson if sub['id'] == str(wrk_id)]
    logging.debug('%s:servicing JSON GET work:%s'%(auth.username(), wrk_id))
    wrk = find_item_json_dict_list(worksJson,'id',wrk_id)
    if wrk is None or len(wrk) == 0:
        logging.error('%s:JSON GET id missing- %s'%(auth.username(), wrk_id))
        abort(404)
    return jsonify({'work': wrk})
@app.route(endpoint_prefix + 'work-work-relations', methods=['GET'])
@auth.login_required
@cross_origin()
def get_work_work_relations():
    logging.debug('%s:servicing JSON GET All work-work-relations'%auth.username())
    return jsonify({'relations': wwrJson})
@app.route(endpoint_prefix + 'work-to-work', methods=['GET'])
@auth.login_required
@cross_origin()
def get_work_relates_work():
    logging.debug('%s:servicing JSON GET All work-relates-to-work'%auth.username())
    return jsonify({'work-to-work': wrwJson})
@app.route(endpoint_prefix + 'nodes-edges-work', methods=['GET'])
@auth.login_required
@cross_origin()
def get_nodes_edges_work():
    logging.debug('%s:servicing JSON GET work nodes & edges'%auth.username())
    work_refreshFromdb()
    # g = refreshGraph()
    # write json formatted data
    # d = json_graph.node_link_data(g) # node-link format to serialize
    # write json
    return jsonify(json_graph.node_link_data(work_refreshGraph()))
@app.route(endpoint_prefix + 'tree-work', methods=['GET'])
@auth.login_required
@cross_origin()
def get_tree_work():
    logging.debug('%s:servicing JSON GET work tree'%auth.username())
    work_refreshFromdb()
    # g = refreshGraph()
    # write json formatted data
    # t = nx.bfs_tree(g,"aum")
    # treedata = json_graph.tree_data(t,"aum")
    # write json
    return jsonify(work_add_name_description(json_graph.tree_data(nx.bfs_tree(work_refreshGraph(),"all"),"all")))
@app.route(endpoint_prefix + 'subtree-work/<string:wrk_id>', methods=['GET'])
@auth.login_required
@cross_origin()
def get_subtree_work(wrk_id):
    logging.debug('%s:servicing JSON GET work sub-tree for <'%(auth.username(), wrk_id + '>'))
    work_refreshFromdb()
    return jsonify(work_add_name_description(json_graph.tree_data(nx.bfs_tree(work_refreshGraph(),"all"),wrk_id)))
#  --------------------  all features allowed for editors (edit, create, remove subjects and relatins) below -----------------------------
@app.route(endpoint_prefix + 'work-with-relation', methods=['POST'])
@auth.login_required
@cross_origin()
def create_work_with_relation():
    if get_role(auth.username())in ['editor','admin']:
        logging.debug('%s:servicing create work with relation:'%auth.username())
        if not request.json or not 'work' in request.json or not 'related' in request.json or not 'relation' in request.json:
            logging.error('%s:incorrect request- %s'%(auth.username(), request.json))
            abort(400)
        if 'sortorder' in request.json: dict = {"work": request.json['work'], "related": request.json['related'], "relation": request.json['relation'],'sortorder':request.json['sortorder']}
        else: dict = {"work": request.json['work'], "related": request.json['related'], "relation": request.json['relation']}
        work2 = dict['work']
        if not 'id' in work2 or not 'name' in work2 or work2['id'] == ''  or work2['name'] == '':
            logging.error('%s:incorrect request- %s'%(auth.username(), str(work2)))
            abort(400)
        work1id = dict['related']
        if 'relation' in dict: relation = dict['relation']
        else: relation = None
        if 'sortorder' in dict:
            sortorder = dict['sortorder']
            if sortorder=='': sortorder = None
        else: sortorder = None
        if find_item_json_dict_list(worksJson,'id',work1id) is None:  # no work1
            return None
        if find_item_json_dict_list(worksJson,'id',work2['id']) is not None:
            # duplicate work2 id .. generate a random id suffix and concatenate
            work2['id'] = (work2['id'] + ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(16)))[0:19]
        # workx = work2 #ast.literal_eval(work2)
        try:
            with ktm.database.atomic() as trans:
                ktm.Work.create(id=work2['id'],name=work2['name'],description=work2['description'])  # db create row
                worksJson.append(work2)
                response = work_create_relation(work1id,work2['id'],relation=relation,sortorder=sortorder)
                if not response:
                    trans.rollback()
                    logging.error('%s:Failed to create work-%s'%(auth.username(), work2))
                return jsonify({'work': response})
        except peewee.IntegrityError:
            trans.rollback()
            logging.error('%s:Failed to create work-%s'%(auth.username(), work2))
            return jsonify({'work': False})
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'work', methods=['POST'])
@auth.login_required
@cross_origin()
def create_work():
    if get_role(auth.username())in ['editor','admin']:
        logging.debug('%s:servicing create work'%auth.username())
        if not request.json or not 'id' in request.json or not 'name' in request.json:
            logging.error('%s:incorrect request- %s'%(auth.username(), request.json))
            abort(400)
        work = {"id": request.json['id'], "name": request.json['name'], "description": request.json.get('description', "")}
        if find_item_json_dict_list(worksJson,'id',str(request.json['id'])) is not None:
            # subj = ast.literal_eval(str(sub))
            # generate a random string and concatenate - changes id to unique 20-char string
            work['id'] = (work['id'] + ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(16)))[0:19]
        try:
            ktm.Work.create(id=work['id'],name=work['name'],description=work['description'])  # db create row
            worksJson.append(work)
            return jsonify({'work': work}), 201
        except:
            logging.error('%s:Failed to create work- %s'%(auth.username(), work['id']))
            return jsonify({'work': work}), 409
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'work/<string:wrk_id>', methods=['PUT'])
@auth.login_required
@cross_origin()
def update_work(wrk_id):
    if get_role(auth.username())in ['editor','admin']:
        logging.debug('%s:servicing update work:%s'%(auth.username(), wrk_id))
        if (not request.json):
            logging.error('%s:JSON PUT error incorrect request- %s'%(auth.username(), request.json))
            abort(400)
        for index in range(len(worksJson)):
            # json_acceptable_string = subjectsJson[index].replace("'", "\"")
            dict = worksJson[index] #ast.literal_eval(subjectsJson[index])
            if dict['id'] == wrk_id:
                dict['name'] = request.json.get('name', '')
                dict['description'] = request.json.get('description', '')
                worksJson[index] = dict #json.dumps(dict)
                try:
                    workx = ktm.Work.get(ktm.Work.id == wrk_id)   # db get/update row
                    workx.name = dict['name']
                    workx.description = dict['description']
                    workx.save()
                    if 'relation' in request.json or 'sortorder' in request.json:  # modify work_to_work if any change to relation or sort order
                        work_update_relation(wrk_id,request.json.get('relation', None),int(request.json.get('sortorder', None)))
                    return jsonify({'work': dict}), 201
                except peewee.IntegrityError:
                    logging.error('%s:Failed to update work- %s'%(auth.username(), workx['id']))
                    return jsonify({'work': workx}), 409
        logging.error('%s:JSON PUT: id missing- %s'%(auth.username(), wrk_id))
        abort(404)  # not found
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'work-with-relation/<string:wrk_id>', methods=['DELETE'])
@auth.login_required
@cross_origin()
def delete_work_with_relation(wrk_id):
    if get_role(auth.username())in ['editor','admin']:
        logging.debug('%s:servicing delete work with relation:%s'%(auth.username(), wrk_id))
        relations = work_find_relations(wrk_id)
        for work_with_relation in relations:
            work1 = work_with_relation['related']
            relation = work_with_relation['relation']
            work_delete_relation(work1,wrk_id,relation)# each relation with another work1 removed
        for work_index in range(len(worksJson)): # remove work from db & Json list
                work_as_dict = worksJson[work_index] #ast.literal_eval(subjectsJson[subj_index])
                if work_as_dict['id'] == wrk_id or work_as_dict[u'id'] == wrk_id:
                    try:
                        workdbrow = ktm.Work.get(ktm.Work.id == work_as_dict['id'])   # db get/delete row
                        workdbrow.delete_instance()
                        del worksJson[work_index]
                    except peewee.IntegrityError:
                        logging.error('%s:Failed to  delete work with relation- %s'%(auth.username(), wrk_id))
                        return jsonify({'result': False}), 409
                    break
        return jsonify({'result': True})
@app.route(endpoint_prefix + 'work/<string:wrk_id>', methods=['DELETE'])
@auth.login_required
@cross_origin()
def delete_work(wrk_id):
    if get_role(auth.username())in ['editor','admin']:
        logging.debug('%s:servicing delete subject: %s'%(auth.username(), wrk_id))
        wrk = find_item_json_dict_list(worksJson,'id',wrk_id)
        if wrk is None or len(wrk) == 0:
            logging.error('%s:incorrect request- %s'%(auth.username(), request.json))
            abort(404)
        # if len(wrk) == 0:
        #     return False
        for work_index in range(len(worksJson)):
            work_as_dict = worksJson[work_index] #ast.literal_eval(worksJson[work_index])
            if (work_as_dict['id'] == wrk['id'] or work_as_dict[u'id'] == wrk['id'] or work_as_dict['id'] == wrk[u'id']) :
                try:
                    workx = ktm.Work.get(ktm.Work.id == work_as_dict['id'])   # db get/delete row
                    workx.delete_instance()
                    del worksJson[work_index]
                except peewee.IntegrityError:
                    logging.error('%s:Failed to create subject- %s'%(auth.username(), workx['id']))
                    return jsonify({'result': False}), 409
                break
        return jsonify({'result': True})
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'work-to-work', methods=['POST'])
@auth.login_required
@cross_origin()
def create_work_to_work():
    if get_role(auth.username())in ['editor','admin']:
        logging.debug('%s:servicing work-to-work create relation'%auth.username())
        if not request.json or not 'work1' in request.json or not 'work2' in request.json or not 'relation' in request.json:
            logging.error('%s:JSON POST incorrect request- %s'%(auth.username(), request.json))
            abort(400)
        return jsonify({'result': work_create_relation(request.json['work1'],request.json['work2'],request.json['relation'])})
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'work-to-work', methods=['DELETE'])
@auth.login_required
@cross_origin()
def delete_work_to_work():
    if get_role(auth.username())in ['editor','admin']:
        logging.debug('%s:servicing work-to-work delete relation'%auth.username())
        if not request.json or not 'work1' in request.json or not 'work2' in request.json or not 'relation' in request.json:
            logging.error('%s:JSON POST incorrect request- %s'%(auth.username(), request.json))
            abort(400)
        return jsonify({'result': work_delete_relation(request.json['work1'],request.json['work2'],request.json['relation'])})
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'work-move/<string:wrk_id>', methods=['POST'])
@auth.login_required
@cross_origin()
def move_work(wrk_id):
    if get_role(auth.username())in ['editor','admin']:
        logging.debug('%s:servicing work-to-work move relation'%auth.username())
        if not request.json or not 'id' in request.json:
            logging.error('%s:JSON POST incorrect request- %s'%(auth.username(), request.json))
            abort(400)
        if 'relation' in request.json:
            if 'sortorder' in request.json:return jsonify({'result': work_move_relation(wrk_id,request.json['id'],request.json['relation'],request.json['sortorder'])})
            else:return jsonify({'result': work_move_relation(wrk_id,request.json['id'],request.json['relation'])})
        else:
            return jsonify({'result': work_move_relation(wrk_id,request.json['id'])})
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'work-copy/<string:wrk_id>', methods=['POST'])
@auth.login_required
@cross_origin()
def work_copy_subtree(wrk_id):
    if get_role(auth.username())in ['editor','admin']:
        logging.debug('%s:servicing work copy subtree:%s to %s'%(auth.username(), wrk_id, str(request.json['id'])))
        if not request.json or not 'id' in request.json:
            logging.error('%s:JSON POST incorrect request- %s'%(auth.username(), request.json))
            abort(400)
        return jsonify({'result': work_copy_children(wrk_id,request.json['id'])})
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'subtree-work/<string:wrk_id>', methods=['DELETE'])
@auth.login_required
@cross_origin()
def work_remove_subtree(wrk_id):
    if get_role(auth.username())in ['editor','admin']:
        logging.debug('%s:servicing remove subtree %s'%(auth.username(), wrk_id))
        return jsonify({'result': work_delete_children(wrk_id)})
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)

#------------------------------------ subject-work related selects -----------------------
#  --------------------  all features allowed for normal users(view works and relations) below -----------------------------
@app.route(endpoint_prefix + 'subject-work-relations', methods=['GET'])
@auth.login_required
@cross_origin()
def get_subject_work_relations():
    logging.debug('%s:servicing JSON GET All possible subject-work-relations'%auth.username())
    return jsonify({'relations': wsrJson})
@app.route(endpoint_prefix + 'subject-to-work', methods=['GET'])
@auth.login_required
@cross_origin()
def get_subject_relatesto_work():
    logging.debug('%s:servicing JSON GET All subject-relates-to-work'%auth.username())
    return jsonify({'subject-to-work': shwJson})
@app.route(endpoint_prefix + 'subject-to-work', methods=['POST'])
@auth.login_required
@cross_origin()
def create_subject_to_work():
    if get_role(auth.username())in ['editor','admin']:
        logging.debug('%s:servicing subject-to-work create relation'%auth.username())
        if not request.json or not 'subject' in request.json or not 'work' in request.json or not 'relation' in request.json:
            logging.error('%s:JSON POST incorrect request- %s'%(auth.username(), request.json))
            abort(400)
        return jsonify({'result': subject_work_create_relation(request.json['subject'],request.json['work'],request.json['relation'])})
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'subject-to-work', methods=['DELETE'])
@auth.login_required
@cross_origin()
def delete_subject_to_work():
    if get_role(auth.username())in ['editor','admin']:
        logging.debug('%s:servicing subject-to-work delete relation'%auth.username())
        if not request.json or not 'subject' in request.json or not 'work' in request.json or not 'relation' in request.json:
            logging.error('%s:JSON POST incorrect request- %s'%(auth.username(), request.json))
            abort(400)
        return jsonify({'result': subject_work_delete_relation(request.json['subject'],request.json['work'],request.json['relation'])})
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'tree-subject-work/<string:subject>', methods=['GET'])
@auth.login_required
@cross_origin()
def get_tree_subject_to_work(subject):
    logging.debug('%s:servicing JSON GET subject-work tree'%auth.username())
    subject_work_refreshFromdb();
    return jsonify(subject_work_add_relation(json_graph.tree_data(nx.bfs_tree(subject_work_refreshGraph(subject),subject),subject)))
@app.route(endpoint_prefix + 'tree-work-subject/<string:work>', methods=['GET'])
@auth.login_required
@cross_origin()
def get_tree_work_to_subject(work):
    logging.debug('%s:servicing JSON GET work-subject tree'%auth.username())
    subject_work_refreshFromdb();
    return jsonify(work_subject_add_relation(json_graph.tree_data(nx.bfs_tree(work_subject_refreshGraph(work),work),work)))

#------------------------------------ person related selects -----------------------
#  --------------------  all features allowed for normal users(view persons and relations) below -----------------------------
@app.route(endpoint_prefix + 'persons', methods=['GET'])
@auth.login_required
@cross_origin()
def get_persons():
    logging.debug('%s:servicing JSON GET All persons'%auth.username())
    return jsonify({'persons': personsJson})
@app.route(endpoint_prefix + 'person/<string:prs_id>', methods=['GET'])
@auth.login_required
@cross_origin()
def get_person(prs_id):
    # sub = [sub for sub in subjectsJson if sub['id'] == str(prs_id)]
    logging.debug('%s:servicing JSON GET person: %s'%(auth.username(), prs_id))
    prs = find_item_json_dict_list(personsJson,'id',prs_id)
    if prs is None or len(prs) == 0:
        logging.error('%s:JSON GET id missing- %s'%(auth.username(), prs_id))
        abort(404)
    return jsonify({'person': prs})
@app.route(endpoint_prefix + 'person-person-relations', methods=['GET'])
@auth.login_required
@cross_origin()
def get_person_person_relations():
    logging.debug('%s:servicing JSON GET All person-person-relations'%auth.username())
    return jsonify({'relations': pprJson})
@app.route(endpoint_prefix + 'person-to-person', methods=['GET'])
@auth.login_required
@cross_origin()
def get_person_relates_person():
    logging.debug('%s:servicing JSON GET All person-relates-to-person'%auth.username())
    return jsonify({'person-to-person': prpJson})
@app.route(endpoint_prefix + 'nodes-edges-person', methods=['GET'])
@auth.login_required
@cross_origin()
def get_nodes_edges_person():
    logging.debug('%s:servicing JSON GET person nodes & edges'%auth.username())
    person_refreshFromdb()
    # gp = refreshGraph()
    # write json formatted data
    # d = json_graph.node_link_data(gp) # node-link format to serialize
    # write json
    return jsonify(json_graph.node_link_data(person_refreshGraph()))
@app.route(endpoint_prefix + 'tree-person', methods=['GET'])
@auth.login_required
@cross_origin()
def get_tree_person():
    logging.debug('%s:servicing JSON GET person tree'%auth.username())
    person_refreshFromdb()
    # g = refreshGraph()
    # write json formatted data
    # t = nx.bfs_tree(g,"aum")
    # treedata = json_graph.tree_data(t,"aum")
    # write json
    return jsonify(person_add_names(json_graph.tree_data(nx.bfs_tree(person_refreshGraph(),"all"),"all")))
@app.route(endpoint_prefix + 'subtree-person/<string:prs_id>', methods=['GET'])
@auth.login_required
@cross_origin()
def get_subtree_person(prs_id):
    logging.debug('%s:servicing JSON GET person sub-tree for <'%(auth.username(), prs_id + '>'))
    person_refreshFromdb()
    return jsonify(person_add_names(json_graph.tree_data(nx.bfs_tree(person_refreshGraph(),"all"),prs_id)))
#  --------------------  all features allowed for editors (edit, create, remove subjects and relations) below -----------------------------
@app.route(endpoint_prefix + 'person-with-relation', methods=['POST'])
@auth.login_required
@cross_origin()
def create_person_with_relation():
    if get_role(auth.username())in ['editor','admin']:
        logging.debug('%s:servicing create person with relation:'%auth.username())
        if not request.json or not 'person' in request.json or not 'related' in request.json or not 'relation' in request.json:
            logging.error('%s:incorrect request- %s'%(auth.username(), request.json))
            abort(400)
        dict = {"person": request.json['person'], "related": request.json['related'], "relation": request.json['relation']}
        person2 = dict['person']
        if not 'id' in person2 or person2['id'] == '':
            logging.error('%s:incorrect request- %s'%(auth.username(), str(person2)))
            abort(400)
        person1id = dict['related']
        if 'relation' in dict: relation = dict['relation']
        else: relation = None
        if find_item_json_dict_list(personsJson,'id',person1id) is None:  # no person1
            return None
        if find_item_json_dict_list(personsJson,'id',person2['id']) is not None:
            # duplicate person2 id .. generate a random id suffix and concatenate
            person2['id'] = (person2['id'] + ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(16)))[0:19]
        # personx = person2 #ast.literal_eval(person2)
        # print "creating person-with-relation-2:", person2
        if 'first' in person2: first = person2['first']
        else: first = None
        if 'middle' in person2: middle = person2['middle']
        else: middle = None
        if 'last' in person2: last = person2['last']
        else: last = None
        if 'nick' in person2: nick = person2['nick']
        else: nick = None
        if 'other' in person2: other = person2['other']
        else: other = None
        if 'other' in person2: other = person2['other']
        else: other = None
        if 'initials' in person2: initials = person2['initials']
        else: initials = None
        if 'living' in person2: living = person2['living']
        else: living = '1'
        if 'birth' in person2: birth = person2['birth']
        else: birth = None
        if 'death' in person2: death = person2['death']
        else: death = None
        if 'biography' in person2: biography = person2['biography']
        else: biography = None
        if str(living) == '1':
            death = None
        else:
            if datetime.strptime(death, '%Y-%m-%d') < datetime.strptime(birth, '%Y-%m-%d'):
            # if person['death'] < person['birth']:
                logging.error('%s:death-' + str(death) + ' before birth- %s'%(auth.username(), str(birth) + '.. set to birth date'))
                death = birth
        try:
            with ktm.database.atomic() as trans:
                ktm.Person.create(id=person2['id'],first=first,last=last,middle=middle,nick=nick,other=other,initials=initials, \
                                  living=living,birth=birth,death=death,biography=biography)  # db create row
                personsJson.append(person2)
                response = person_create_relation(person1id,person2['id'],relation=relation)
                if not response:
                    trans.rollback()
                    logging.error('%s:Failed to create person-%s'%(auth.username(), person2))
                return jsonify({'person': response})
        except peewee.IntegrityError:
            trans.rollback()
            logging.error('%s:Failed to create person-%s'%(auth.username(), person2))
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'person', methods=['POST'])
@auth.login_required
@cross_origin()
def create_person():
    if get_role(auth.username())in ['editor','admin']:
        logging.debug('%s:servicing create person'%auth.username())
        if not request.json or not 'id' in request.json:
            logging.error('%s:incorrect request- %s'%(auth.username(), request.json))
            abort(400)
        person = {"id": request.json['id'], "first": request.json.get('first',''), "last": request.json.get('last', ""), "middle": request.json.get('middle', ""), \
                  "nick": request.json.get('nick', ""), "initials": request.json.get('initials', ""), "other": request.json.get('other', ""), \
                  "living": request.json.get('living', ""), "birth": request.json.get('birth', ""), "death": request.json.get('death', ""), \
                  "biography": request.json.get('biography', "")}
        if person['living'] == '1':
            person['death'] = None
        else:
            if person['death'] != '':
                if datetime.strptime(person['death'], '%Y-%m-%d') < datetime.strptime(person['birth'], '%Y-%m-%d'):
                    # if person['death'] < person['birth']:
                    logging.error('%s:death-' + str(person['death']) + ' before birth- %s'%(auth.username(), str(person['birth']) + '.. set to birth date'))
                    person['death'] = person['birth']
        if find_item_json_dict_list(personsJson,'id',str(request.json['id'])) is not None:
            # subj = ast.literal_eval(str(sub))
            # generate a random string and concatenate - changes id to unique 20-char string
            person['id'] = (person['id'] + ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(16)))[0:19]
        try:
            ktm.Person.create(id=person['id'],first=person['first'],last=person['last'],middle=person['middle'],nick=person['nick'],other=person['other'], \
                              initials=person['initials'])  # db create row
            personsJson.append(person)
            return jsonify({'person': person}), 201
        except peewee.IntegrityError:
            logging.error('%s:Failed to create person- %s'%(auth.username(), person['id']))
            return jsonify({'person': person}), 409
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'person/<string:prs_id>', methods=['PUT'])
@auth.login_required
@cross_origin()
def update_person(prs_id):
    if get_role(auth.username())in ['editor','admin']:
        logging.debug('%s:servicing update person:%s'%(auth.username(), prs_id))
        if (not request.json):
            logging.error('%s:JSON PUT error incorrect request- %s'%(auth.username(), request.json))
            abort(400)
        for index in range(len(personsJson)):
            # json_acceptable_string = subjectsJson[index].replace("'", "\"")
            dict = personsJson[index] #ast.literal_eval(subjectsJson[index])
            if dict['id'] == prs_id:
                dict['first'] = request.json.get('first', None)
                dict['last'] = request.json.get('last', None)
                dict['middle'] = request.json.get('middle', None)
                dict['initials'] = request.json.get('initials', None)
                dict['nick'] = request.json.get('nick', None)
                dict['other'] = request.json.get('other', None)
                dict['living'] = request.json.get('living', None)
                dict['birth'] = request.json.get('birth', None)
                dict['death'] = request.json.get('death', None)
                dict['biography'] = request.json.get('biography', None)
                personsJson[index] = dict #json.dumps(dict)
                try:
                    personx = ktm.Person.get(ktm.Person.id == prs_id)   # db get/update row
                    personx.first = dict['first']
                    personx.last = dict['last']
                    personx.middle = dict['middle']
                    personx.initials = dict['initials']
                    personx.nick = dict['nick']
                    personx.other = dict['other']
                    personx.living = dict['living']
                    personx.birth = dict['birth']
                    if personx.living == '1': personx.death = None
                    else:
                        personx.death = dict['death']
                        if personx.death != None and personx.birth != None and personx.death < personx.birth:
                            logging.error('%s:death-' + str(personx.death) + ' before birth- %s'%(auth.username(), str(personx.birth) + '.. set to birth date' ))
                            personx.death = personx.birth
                    personx.biography = dict['biography']
                    personx.save()
                    if 'relation' in request.json:  # modify person_to_person if any change to relation or sort order
                        person_update_relation(prs_id,request.json.get('relation', None))
                    return jsonify({'person': dict}), 201
                except peewee.IntegrityError:
                    logging.error('%s:Failed to update person- %s'%(auth.username(), personx['id']))
                    return jsonify({'person': personx}), 409
        logging.error('%s:JSON PUT - id missing- %s'%(auth.username(), prs_id))
        abort(404)  # not found
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'person-with-relation/<string:prs_id>', methods=['DELETE'])
@auth.login_required
@cross_origin()
def delete_person_with_relation(prs_id):
    if get_role(auth.username())in ['editor','admin']:
        logging.debug('%s:servicing delete person with relation:%s'%(auth.username(), prs_id))
        relations = person_find_relations(prs_id)
        for person_with_relation in relations:
            person1 = person_with_relation['related']
            relation = person_with_relation['relation']
            person_delete_relation(person1,prs_id,relation)# each relation with another person1 removed
        for person_index in range(len(personsJson)): # remove person from db & Json list
                person_as_dict = personsJson[person_index] #ast.literal_eval(subjectsJson[subj_index])
                if person_as_dict['id'] == prs_id or person_as_dict[u'id'] == prs_id:
                    try:
                        persondbrow = ktm.Person.get(ktm.Person.id == person_as_dict['id'])   # db get/delete row
                        persondbrow.delete_instance()
                        del personsJson[person_index]
                    except peewee.IntegrityError:
                        logging.error('%s:failed to delete person with relation:  %s'%(auth.username(), prs_id))
                        return jsonify({'result': False}), 409
                    break
        return jsonify({'result': True})
@app.route(endpoint_prefix + 'person/<string:prs_id>', methods=['DELETE'])
@auth.login_required
@cross_origin()
def delete_person(prs_id):
    if get_role(auth.username()) in ['editor','admin']:
        logging.debug('%s: servicing delete subject: %s'%(auth.username(), prs_id))
        prs = find_item_json_dict_list(personsJson,'id',prs_id)
        if prs is None or len(prs) == 0:
            logging.error('%s: incorrect request - %s'%(auth.username(), prs_id))
            abort(404)
        # if len(wrk) == 0:
        #     return False
        for person_index in range(len(personsJson)):
            person_as_dict = personsJson[person_index] #ast.literal_eval(personsJson[person_index])
            if (person_as_dict['id'] == prs['id'] or person_as_dict[u'id'] == prs['id'] or person_as_dict['id'] == prs[u'id']) :
                try:
                    personx = ktm.Person.get(ktm.Person.id == person_as_dict['id'])   # db get/delete row
                    personx.delete_instance()
                    del personsJson[person_index]
                except peewee.IntegrityError:
                    logging.error('%s: Failed to delete person - %s'%((auth.username(), personx['id'])))
                    return jsonify({'result': False}), 409
                break
        return jsonify({'result': True})
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'person-to-person', methods=['POST'])
@auth.login_required
@cross_origin()
def create_person_to_person():
    if get_role(auth.username())in ['editor','admin']:
        logging.debug('%s:servicing person-to-person create relation'%auth.username())
        if not request.json or not 'person1' in request.json or not 'person2' in request.json or not 'relation' in request.json:
            logging.error('%s: JSON POST incorrect request - %s'%(auth.username(), request.json))
            abort(400)
        return jsonify({'result': person_create_relation(request.json['person1'],request.json['person2'],request.json['relation'])})
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'person-to-person', methods=['DELETE'])
@auth.login_required
@cross_origin()
def delete_person_to_person():
    if get_role(auth.username())in ['editor','admin']:
        logging.debug('%s:servicing person-to-person delete relation'%auth.username())
        if not request.json or not 'person1' in request.json or not 'person2' in request.json or not 'relation' in request.json:
            logging.error('%s:JSON POST incorrect request- %s'%(auth.username(), request.json))
            abort(400)
        return jsonify({'result': person_delete_relation(request.json['person1'],request.json['person2'],request.json['relation'])})
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'person-move/<string:prs_id>', methods=['POST'])
@auth.login_required
@cross_origin()
def move_person(prs_id):
    if get_role(auth.username())in ['editor','admin']:
        logging.debug('%s:servicing person-to-person move relation'%auth.username())
        if not request.json or not 'id' in request.json:
            logging.error('%s :JSON POST incorrect request- %s'%(auth.username(), request.json))
            abort(400)
        if 'relation' in request.json:
            return jsonify({'result': person_move_relation(prs_id,request.json['id'],request.json['relation'])})
        else:
            return jsonify({'result': person_move_relation(prs_id,request.json['id'])})
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
#------------------------------------ person-person related selects -----------------------
#  --------------------  all features allowed for normal users(view persons and relations) below -----------------------------
@app.route(endpoint_prefix + 'person-work-relations', methods=['GET'])
@auth.login_required
@cross_origin()
def get_person_work_relations():
    logging.debug('%s:servicing JSON GET All possible person-work-relations'%auth.username())
    return jsonify({'relations': pwrJson})
@app.route(endpoint_prefix + 'person-to-work', methods=['GET'])
@auth.login_required
@cross_origin()
def get_person_relatesto_work():
    logging.debug('%s:servicing JSON GET All person-relates-to-work'%auth.username())
    return jsonify({'person-to-work': phwJson})
@app.route(endpoint_prefix + 'person-to-work', methods=['POST'])
@auth.login_required
@cross_origin()
def create_person_to_work():
    if get_role(auth.username())in ['editor','admin']:
        logging.debug('%s:servicing person-to-work create relation'%auth.username())
        if not request.json or not 'person' in request.json or not 'work' in request.json or not 'relation' in request.json:
            logging.error('%s:JSON POST incorrect request- %s'%(auth.username(), request.json))
            abort(400)
        return jsonify({'result': person_work_create_relation(request.json['person'],request.json['work'],request.json['relation'])})
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'person-to-work', methods=['DELETE'])
@auth.login_required
@cross_origin()
def delete_person_to_work():
    if get_role(auth.username())in ['editor','admin']:
        logging.debug('%s:servicing person-to-work delete relation'%auth.username())
        if not request.json or not 'person' in request.json or not 'work' in request.json or not 'relation' in request.json:
            logging.error('%s:JSON POST incorrect request- %s'%(auth.username(), request.json))
            abort(400)
        return jsonify({'result': person_work_delete_relation(request.json['person'],request.json['work'],request.json['relation'])})
    else: return make_response(jsonify({'error': 'Not authorized'}), 401)
@app.route(endpoint_prefix + 'tree-person-work/<string:person>', methods=['GET'])
@auth.login_required
@cross_origin()
def get_tree_person_to_work(person):
    logging.debug('%s:servicing JSON GET person-work tree'%auth.username())
    person_work_refreshFromdb();
    return jsonify(person_work_add_relation(json_graph.tree_data(nx.bfs_tree(person_work_refreshGraph(person),person),person)))
@app.route(endpoint_prefix + 'tree-work-person/<string:work>', methods=['GET'])
@auth.login_required
@cross_origin()
def get_tree_work_to_person(work):
    logging.debug('%s:servicing JSON GET work-person tree'%auth.username())
    person_work_refreshFromdb();
    return jsonify(work_person_add_relation(json_graph.tree_data(nx.bfs_tree(work_person_refreshGraph(work),work),work)))

# summary totals
@app.route(endpoint_prefix + 'counts', methods=['GET'])
@auth.login_required
@cross_origin()
def get_summary_counts():
    return jsonify({"subjects":len(subjectsJson), "works":len(worksJson), "persons":len(persons), \
      "subject-to-subject":len(srsJson), "work-to-work":len(wrwJson), \
      "person-to-person":len(prpJson)})
def countsBynode(nodeList,keyname):
    count = {}
    for node in nodeList:
        if node[keyname] not in count: count[node[keyname]] = 1
        else:
            # print ('key: %s count: %d' (node[keyname],count[node_id[keyname]]))
            count[node[keyname]] += 1
    return count
@app.route(endpoint_prefix + 'node-counts', methods=['GET'])
@auth.login_required
@cross_origin()
def get_node_counts():
    subject_counts = countsBynode(srsJson, 'subject1')
    work_counts = countsBynode(wrwJson, 'work1')
    person_counts = countsBynode(prpJson, 'person1')
    return jsonify({"subject_counts": subject_counts, "work_counts": work_counts, "person_counts": person_counts})
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)