#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'NarasMG'
import json, requests, unittest #, pprint
import random

import networkx as nx
from networkx.readwrite import json_graph
restServiceUrl = open('knowledgetreeJSModules/restServiceUrl.csv')
prefix = 'http://' + list(restServiceUrl.readlines())[1][:-1] + '/knowledgeTree/api/v1.0/'
restServiceUrl.close()
# echoservice = 'http://httpbin.org/post'
def ceasar(plain,shift):  # shift each letter by shift
        return "".join([chr((ord(x)- start(x) + shift) % 26 + start(x)) for (x) in list(plain)])
def start(alphabet): # find distance between alphabet and 'a' or 'A'
            strt = ord('a') if alphabet.islower() else ord('A')
            return strt
def get_password(username):
    f = open("credentials_roles.txt")
    auths = json.load(f)
    f.close()
    if username in auths:
        return ceasar(auths[username]["pw"],10);
    return None
def get_role(username):
    f = open("credentials_roles.txt")
    auths = json.load(f)
    f.close()
    if username in auths:
        return auths[username]["role"]
    return None
def restGet(url):
    completeUrl = prefix + url
    # print ('Retrieving:',  completeUrl)
    response = requests.get(completeUrl,auth=('admin',get_password('admin')))
    return response
def restPost(url,data):
    completeUrl = prefix + url
    # print('Posting:url %s jsonData %s'%(completeUrl, data))
    return requests.post(completeUrl, json=data, auth=('admin',get_password('admin')))
def restPut(url,data):
    completeUrl = prefix + url
    # print ('Putting:',  completeUrl)
    return requests.put(completeUrl, json = data, auth=('admin',get_password('admin')))
def restDelete(url):
    completeUrl = prefix + url
    # print ('Deleting:',  completeUrl)
    return requests.delete(completeUrl,auth=('admin',get_password('admin'))) #  headers = {'Content-type': 'application/json'})
def restDeletewithData(url,data):
    completeUrl = prefix + url
    # print ('Deleting:',  completeUrl)
    return requests.delete(completeUrl, json = data, auth=('admin',get_password('admin')))
class TestUM(unittest.TestCase):
    def setUp(self):
        # ------------------remove the child & its relation-------------
        response = restDelete('subject-with-relation/idtestChild')
        # ----------------------remove the parent-------------------
        response = restDelete('subject/idtestParent')
        # ----------------------remove the sample subjects-------------------
        response = restDelete('subject/idtest')
        response = restDelete('subtree/idtestSource')
        response = restDelete('subtree/idtestTarget')
        for id in ['idtestChild1', 'idtestChild2', 'idtestChild3']:
            response = restDelete('subject-with-relation/' + id)
        # ------------------remove the child & its relation-------------
        response = restDelete('work-with-relation/idtestChild')
        # ----------------------remove the parent-------------------
        response = restDelete('work/idtestParent')
        # ----------------------remove the sample work-------------------
        response = restDelete('work/idtest')
        response = restDelete('subtree-work/idtestSource')
        response = restDelete('subtree-work/idtestTarget')
        for id in ['idtestChild1', 'idtestChild2', 'idtestChild3']:
            response = restDelete('work-with-relation/' + id)
        # ------------------remove the child & its relation-------------
        response = restDelete('person-with-relation/idtestChild')
        # ----------------------remove the parent-------------------
        response = restDelete('person/idtestParent')
        # ----------------------remove the sample person-------------------
        response = restDelete('person/idtest')
        # remove the subjects created
        for subject in {'idtest_subject1', 'idtest_subject2', 'idtest_subject3', 'idtest_subject4'}:
            response = restDelete('subtree/' + subject)
        # remove the works created
        for work in {'idtest_work1', 'idtest_work2', 'idtest_work3', 'idtest_work4'}:
            response = restDelete('subtree-work/' + work)
        # remove the persons created
        for person in {'idtest_person1', 'idtest_person2', 'idtest_person3', 'idtest_person4'}:
            response = restDelete('person/' + person)
        # remove the works created
        for work in {'idtest_work1', 'idtest_work2', 'idtest_work3', 'idtest_work4'}:
            response = restDelete('work/' + work)
        # pass
        # restServiceUrl = open('knowledgetreeJSModules//restServiceUrl-remote.csv')
        # prefix = list(restServiceUrl.readlines())[1][:-1] + ':5000/knowledgeTree/api/v1.0/'
        # restServiceUrl.close()
        # self.assertEqual(prefix,'ec2-13-58-244-107.us-east-2.compute.amazonaws.com:5000/knowledgeTree/api/v1.0/')
        # prefix = 'http://ec2-13-58-244-107.us-east-2.compute.amazonaws.com:5000/knowledgeTree/api/v1.0/'

    # f =  open("credentials_roles.txt")
    # print f.readlines()
    # f.close
    # auths = json.load(open("credentials_roles.txt"))
    # print auths, type(auths)
    def test_subjects(self):
        get_services = ['subjects','subject-to-subject','subject-subject-relations']
        for service in get_services:
            response = restGet(service)
            # print response.text
            self.assertEqual(200,response.status_code)
    def test_create_modify_remove_subjects(self):
        # ----------------create a sample subject--------------------------
        response = restPost('subject',{'id': 'idtest','name': 'name-test','description': 'description-test'})
        self.assertEqual(201,response.status_code)
        self.assertIn('idtest',response.text)
        # ----------------create a duplicate of the subject--------------------------
        '''
        response = restPost('subject',{"id": "idtest", "name": "name-test-duplicate", "description": "description-test-duplicate"})
        self.assertEqual(201,response.status_code)
        # print "attempt to create duplicate:", response.text
        self.assertIn('idtest',response.text,'duplicate created')
        '''
        # ----------------create a parent subject--------------------------
        response = restPost('subject',{'id': 'idtestParent','name': 'name-test-parent','description': 'description-test-parent'})
        # print ('create subject status:', response.status_code, '\n',response.text)
        self.assertEqual(201, response.status_code)
        # create a child subject
        response = restPost('subject-with-relation',
                        {"subject": {"id": "idtestChild", "name": "name-test-child", "description": "description-test-child"},
                         "related": "idtestParent", "relation": "Anga","sortorder": 65})
        self.assertEqual(200, response.status_code)
        self.assertEqual ('{"subject":true}', response.text.replace('\n','').replace(' ',''))
        # print( 'status:', response.status_code, '\n', json.loads(response.text.replace('\n','')))
        # # pprint.pprintresponse.json())

        # create a duplicate child subject
        '''
        response = restPost('subject-with-relation', \
                        {"subject": {"id": "idtestChild", "name": "name-test-child-duplicate", "description": "description-test-child-duplicate"},
                         "related": "idtestParent", "relation": "Anga","sortorder": 65 })
        self.assertEqual(200,response.status_code)
        self.assertEqual ('{"subject":true}',response.text.replace('\n','').replace(' ',''))
        '''
        # ----------------get the parent subject------------------
        response = restGet('subject/idtestParent')
        self.assertEqual(200, response.status_code)
        self.assertEqual('{"subject":{"description":"description-test-parent","id":"idtestParent","name":"name-test-parent"}}', \
            response.text.replace('\n','').replace(' ',''))

        # -----------------get the child subject-----------------
        response=restGet('subject/idtestChild')
        self.assertEqual(200,response.status_code)
        self.assertEqual('{"subject":{"description":"description-test-child","id":"idtestChild","name":"name-test-child"}}', \
            response.text.replace('\n','').replace(' ','').replace(' ',''))
        response=restGet('subject-to-subject')
        # print response.text.replace('\n','').replace(' ','')

        # ------------------check the parent-child relation------------------
        self.assertIn('{"relation":"Anga","sortorder":65,"subject1":"idtestParent","subject2":"idtestChild"}', \
            response.text.replace('\n','').replace(' ',''))

        # ----------------create a new target subject--------------------------
        response = restPost('subject',
                            {'id': 'idtestTarget', 'name': 'name-test-target', 'description': 'description-test-target'})
        self.assertEqual(201,response.status_code)
        # ----------------create a source subject--------------------------
        response =  restPost('subject',{'id': 'idtestSource','name': 'name-test-parent','description': 'description-test-parent'})
        # print 'status:', response.status_code, '\n',response.text
        # create child subjects
        for id in ['idtestChild1','idtestChild2','idtestChild3']:
            order = random.choice(range(1,10))
            response = restPost('subject-with-relation', \
                            {"subject": {"id": id, "name": "name-test-child", "description": "description-test-child"},
                             "related": "idtestSource", "relation": "Anga","sortorder": order })
            self.assertEqual(200,response.status_code)
            self.assertEqual ('{"subject":true}',response.text.replace('\n','').replace(' ',''))
        response = restPost('subject-copy/idtestSource',{'id':'idtestTarget'})  # copy source subtree to target
    # def test_modify_subjects(self):
        # -----------------modify the parent----------------------
        response = restPut('subject/idtestParent',{'id': 'idtestParent','name': 'name-test-parent-update','description': 'description-test-parent-update'})
        # print ('status:', response.status_code, '\n',response.text)
        self.assertEqual(201,response.status_code)
        # print ('modify subjects .. status:', response.status_code, '\n', response.text.replace('\n','').replace(' ',''))
        self.assertEqual( \
        '{"subject":{"description":"description-test-parent-update","id":"idtestParent","name":"name-test-parent-update"}}', \
            response.text.replace('\n','').replace(' ',''))

        # -------------------get the parent--------------------------
        response = restGet('subject/idtestParent')
        self.assertEqual(200,response.status_code)

        # ------------------modify the child & the relation order-------------------------------
        response =  restPut('subject/idtestChild',{'id': 'idtestChild','name': 'name-test-child-update','description': 'description-test-child-update', \
                                                   'relation': 'Dharma','sortorder':'78'})
        self.assertEqual(201,response.status_code)
        # response = restGet('subject/idtestChild')
        # print 'status:', response.status_code, '\n', response.text.replace('\n','').replace(' ','')
        self.assertEqual( \
        '{"subject":{"description":"description-test-child-update","id":"idtestChild","name":"name-test-child-update"}}', \
            response.text.replace('\n','').replace(' ',''))
    # def test_remove_subjects(self):
        # ------------------remove the child & its relation-------------
        response = restDelete('subject-with-relation/idtestChild')
        self.assertEqual(200,response.status_code)
        # print('remove subjects ',response.status_code)
        # response = restDelete('subject-with-relation/idtestNewChild')
        # self.assertEqual(200,response.status_code)
        # ----------------------remove the parent-------------------
        response = restDelete('subject/idtestParent')
        self.assertEqual(200,response.status_code)
        # ----------------------remove the sample subjects-------------------
        response = restDelete('subject/idtest')
        self.assertEqual(200,response.status_code)
        response = restDelete('subtree/idtestSource')
        self.assertEqual(200,response.status_code)
        response = restDelete('subtree/idtestTarget')
        self.assertEqual(200,response.status_code)
        for id in ['idtestChild1','idtestChild2','idtestChild3']:
            response = restDelete('subject-with-relation/' + id)
            self.assertEqual(200,response.status_code)
    def test_works(self):
        get_services = ['works','work-to-work','work-work-relations']
        for service in get_services:
            response = restGet(service)
            # print response.text
            self.assertEqual(200,response.status_code)
    def test_create_modify_remove_works(self):
        # ----------------create a sample work--------------------------
        response =  restPost('work',{'id': 'idtest','name': 'name-test','description': 'description-test'})
        self.assertEqual(201,response.status_code)
        self.assertIn('idtest',response.text)
        # ----------------create a duplicate of the work--------------------------
        '''
        response = restPost('work',{"id": "idtest", "name": "name-test-duplicate", "description": "description-test-duplicate"})
        self.assertEqual(201,response.status_code)
        # print "attempt to create duplicate:", response.text
        self.assertIn('idtest',response.text,'duplicate created')
        '''
        # ----------------create a parent work--------------------------
        response = restPost('work',{'id': 'idtestParent','name': 'name-test-parent','description': 'description-test-parent'})
        # print 'status:', response.status_code, '\n',response.text
        self.assertEqual(201,response.status_code)
        # create a child work
        response = restPost('work-with-relation', \
                        {"work": {"id": "idtestChild", "name": "name-test-child", "description": "description-test-child"},
                         "related": "idtestParent", "relation": "derived","sortorder": 65 })
        self.assertEqual(200,response.status_code)
        self.assertEqual ('{"work":true}',response.text.replace('\n','').replace(' ',''))
        # print 'status:', response.status_code, '\n',response.text.replace('\n','')
        # # pprint.pprintresponse.json())

        # create a duplicate child work
        '''
        response = restPost('work-with-relation', \
                        {"work": {"id": "idtestChild", "name": "name-test-child-duplicate", "description": "description-test-child-duplicate"},
                         "related": "idtestParent", "relation": "commentary","sortorder": 65 })
        self.assertEqual(200,response.status_code)
        self.assertEqual ('{"subject":true}',response.text.replace('\n','').replace(' ',''))
        '''
        # ----------------get the parent work------------------
        response=restGet('work/idtestParent')
        self.assertEqual(200,response.status_code)
        self.assertEqual( \
        '{"work":{"description":"description-test-parent","id":"idtestParent","name":"name-test-parent"}}', \
            response.text.replace('\n','').replace(' ',''))
        # print 'status:', response.status_code, '\n',response.text.replace('\n','').replace(' ','')

        # -----------------get the child work-----------------
        response=restGet('work/idtestChild')
        self.assertEqual(200,response.status_code)
        self.assertEqual( \
        '{"work":{"description":"description-test-child","id":"idtestChild","name":"name-test-child"}}', \
            response.text.replace('\n','').replace(' ','').replace(' ',''))
        response=restGet('work-to-work')
        # print response.text.replace('\n','').replace(' ','')

        # ------------------check the parent-child relation------------------
        self.assertIn( \
        '{"relation":"derived","sortorder":65,"work1":"idtestParent","work2":"idtestChild"}', \
            response.text.replace('\n','').replace(' ',''))
        # ----------------create a new target work--------------------------
        response = restPost('work',
                            {'id': 'idtestTarget', 'name': 'name-test-target', 'description': 'description-test-target'})
        self.assertEqual(201,response.status_code)
        # ----------------create a source work--------------------------
        response = restPost('work',{'id': 'idtestSource','name': 'name-test-parent','description': 'description-test-parent'})
        # print 'status:', response.status_code, '\n',response.text
        # create child works
        for id in ['idtestChild1','idtestChild2','idtestChild3']:
            order = random.choice(range(1,10))
            response = restPost('work-with-relation', \
                            {"work": {"id": id, "name": "name-test-child", "description": "description-test-child"},
                             "related": "idtestSource", "relation": "partwhole","sortorder": order })
            self.assertEqual(200,response.status_code)
            self.assertEqual ('{"work":true}',response.text.replace('\n','').replace(' ',''))
        response = restPost('work-copy/idtestSource',{'id':'idtestTarget'})  # copy source subtree to target
    # def test_modify_works(self):
        # -----------------modify the parent----------------------
        response = restPut('work/idtestParent',{'id': 'idtestParent','name': 'name-test-parent-update','description': 'description-test-parent-update'})
        # print ('status:', response.status_code, '\n',response.text)
        self.assertEqual(201,response.status_code)
        # print ('modify works .. status:', response.status_code, '\n', response.text.replace('\n','').replace(' ',''))
        self.assertEqual( \
        '{"work":{"description":"description-test-parent-update","id":"idtestParent","name":"name-test-parent-update"}}', \
            response.text.replace('\n','').replace(' ',''))

        # -------------------get the parent--------------------------
        response = restGet('work/idtestParent')
        self.assertEqual(200,response.status_code)

        # ------------------modify the child & the relation order-------------------------------
        response =  restPut('work/idtestChild',{'id': 'idtestChild','name': 'name-test-child-update','description': 'description-test-child-update', \
                                                   'relation': 'volume','sortorder':'78'})
        self.assertEqual(201,response.status_code)
        # response = restGet('subject/idtestChild')
        # print 'status:', response.status_code, '\n', response.text.replace('\n','').replace(' ','')
        self.assertEqual( \
        '{"work":{"description":"description-test-child-update","id":"idtestChild","name":"name-test-child-update"}}', \
            response.text.replace('\n','').replace(' ',''))
    # def test_remove_works(self):
        # ------------------remove the child & its relation-------------
        response = restDelete('work-with-relation/idtestChild')
        # print 'status:', response.status_code, '\n',response.text
        self.assertEqual(200,response.status_code)
        # ----------------------remove the parent-------------------
        response = restDelete('work/idtestParent')
        # print 'status:', response.status_code, '\n',response.text
        self.assertEqual(200,response.status_code)
        # ----------------------remove the sample work-------------------
        response = restDelete('work/idtest')
        self.assertEqual(200,response.status_code)
        response = restDelete('subtree-work/idtestSource')
        self.assertEqual(200,response.status_code)
        response = restDelete('subtree-work/idtestTarget')
        self.assertEqual(200,response.status_code)
        for id in ['idtestChild1','idtestChild2','idtestChild3']:
            response = restDelete('work-with-relation/' + id)
            self.assertEqual(200,response.status_code)
    def test_subject_to_work(self):
        get_services = ['subject-work-relations','subject-to-work']
        for service in get_services:
            response = restGet(service)
            # print response.text
            self.assertEqual(200,response.status_code)
         # ----------------create sample subjects --------------------------
        for subject in {'idtest_subject1','idtest_subject2','idtest_subject3','idtest_subject4'}:
            response = restPost('subject',{'id': subject,'name': 'name-test','description': 'description-test'})
            self.assertEqual(201,response.status_code)
            self.assertIn(subject,response.text)
        # ----------------create sample works --------------------------
        for work in {'idtest_work1','idtest_work2','idtest_work3','idtest_work4'}:
            response = restPost('work',{'id': work,'name': 'name-test','description': 'description-test'})
            self.assertEqual(201,response.status_code)
            self.assertIn(work,response.text)
        # ----------------create subject work relations --------------------------
        for work in {'idtest_work1','idtest_work2','idtest_work3'}:
            response = restPost('subject-to-work',{'subject': 'idtest_subject1','work': work,'relation': 'pramaana_prameya'})
            self.assertEqual(200,response.status_code)
            self.assertIn('"result":true',response.text.replace('": ','":').replace('\n',''))
            # print('subject-to-work ', response.text)
        for subject in {'idtest_subject2','idtest_subject3','idtest_subject4'}:
            response = restPost('subject-to-work',{'subject': subject,'work': 'idtest_work4','relation': 'pramaana_prameya'})
            self.assertEqual(200,response.status_code)
            self.assertIn('"result":true',response.text.replace('": ','":').replace('\n',''))
        # ----------------get subject-to-work tree--------------------------
        # gsub = restGet('tree-subject-work/idtest_subject1')
        # json.dump(gsub.content, open('jsondata/knowledgeTree-subject-work-tree.json','w'))
        # ----------------get work-to-subject tree--------------------------
        # gwrk = restGet('tree-work-subject/idtest_work4')
        # json.dump(gwrk.content, open('jsondata/knowledgeTree-work-subject-tree.json','w'))
        # ----------------remove all subject work relations created--------------------------
        # for work in {'idtest_work1','idtest_work2','idtest_work3'}:
        #     response =  restDeletewithData('subject-to-work',{'subject': 'idtest_subject1','work': work,'relation': 'pramaana_prameya'})
        #     self.assertEqual(200,response.status_code)
        #     self.assertIn('"result": true',response.text)
        # for subject in {'idtest_subject2','idtest_subject3','idtest_subject4'}:
        #     response =  restDeletewithData('subject-to-work',{'subject': subject,'work': 'idtest_work4','relation': 'pramaana_prameya'})
        #     self.assertEqual(200,response.status_code)
        #     self.assertIn('"result": true',response.text)
        # remove the subjects created
        for subject in {'idtest_subject1','idtest_subject2','idtest_subject3','idtest_subject4'}:
            # response = restDelete('subject/' + subject)
            response = restDelete('subtree/' + subject)
            self.assertEqual(200,response.status_code)
        # remove the works created
        for work in {'idtest_work1','idtest_work2','idtest_work3','idtest_work4'}:
            # response = restDelete('work/' + work)
            response = restDelete('subtree-work/' + work)
            self.assertEqual(200,response.status_code)
    def test_persons(self):
        get_services = ['persons','person-to-person','person-person-relations']
        for service in get_services:
            response = restGet(service)
            # print response.text
            self.assertEqual(200,response.status_code)
    def test_create_modify_remove_persons(self):
        # ----------------create a sample person--------------------------
        response = restPost('person',{"id": "idtest", "first": "first", "last": "last","middle": "middle",   \
                                  "initials": "ini", "nick":"nick", "other":"other", "living":"1","birth":"1955-01-01", \
                                  "biography":"this was a great life, still not dead"})
        self.assertEqual(201,response.status_code)
        self.assertIn('"id":"idtest"',response.text.replace('": ','":').replace('\n',''))
        self.assertIn('"first":"first"',response.text.replace('": ','":').replace('\n',''))
        self.assertIn('"middle":"middle"',response.text.replace('": ','":').replace('\n',''))
        self.assertIn('"last":"last"',response.text.replace('": ','":').replace('\n',''))
        self.assertIn('"nick":"nick"',response.text.replace('": ','":').replace('\n',''))
        self.assertIn('"other":"other"',response.text.replace('": ','":').replace('\n',''))
        self.assertIn('"living":"1"',response.text.replace('": ','":').replace('\n',''))
        self.assertIn('"birth":"1955-01-01"',response.text.replace('": ','":').replace('\n',''))
        self.assertIn('"biography":"this was a great life, still not dead"',response.text.replace('": ','":').replace('\n',''))
        # ----------------create a duplicate of the person--------------------------
        '''
        response = restPost('person',{"id": "idtest", "first": "firstduplicate", "last": "lastduplicate","middle": "middle",   \
                                  "initials": "ini", "nick":"nick", "other":"other"})
        self.assertEqual(201,response.status_code)
        # print "attempt to create duplicate:", response.text
        self.assertIn('idtest',response.text,'duplicate created')
        '''
        # ----------------create a parent person--------------------------
        response = restPost('person',{"id": "idtestParent", "first": "first-parent", "last": "last-parent","middle": "middle-parent",   \
                                  "initials": "ini", "nick":"nick-parent", "other":"other-parent"})
        # print ('create person parent status:', response.status_code, '\n',response.text)
        self.assertEqual(201,response.status_code)
        # create a child person
        response = restPost('person-with-relation',{"person": {"id": "idtestChild","first": "first-child", "last": "last-child","middle": "middle-child",   \
                                  "initials": "ini", "nick":"nick-child", "other":"other-child"},
                         "related": "idtestParent", "relation": "gurushishya"})
        self.assertEqual(200,response.status_code)
        self.assertEqual('{"person":true}',response.text.replace('\n','').replace(' ',''))
        # print 'status:', response.status_code, '\n',response.text.replace('\n','')
        # # pprint.pprintresponse.json())

        # create a duplicate child person
        '''
        response = restPost('person-with-relation', \
                        {"person": {"id": "idtestChild", "name": "name-test-child-duplicate", "description": "description-test-child-duplicate"},
                         "related": "idtestParent", "relation": "commentary","sortorder": 65 })
        self.assertEqual(200,response.status_code)
        self.assertEqual ('{"subject":true}',response.text.replace('\n','').replace(' ',''))
        '''
        # ----------------get the parent person------------------
        response=restGet('person/idtestParent')
        self.assertEqual(200,response.status_code)
        # self.assertEqual( '{"person":{"first":"first-parent","id":"idtestParent","initials":"ini","last":"last-parent","middle":"middle-parent","nick":"nick-parent","other":"other-parent"}', \
        #     response.text.replace('\n','').replace(' ',''))
        # print 'status:', response.status_code, '\n',response.text.replace('\n','').replace(' ','')

        # -----------------get the child person-----------------
        response=restGet('person/idtestChild')
        self.assertEqual(200,response.status_code)
        # self.assertEqual( "{'person':{'last':'last-child','middle':'middle-child','nick':'nick-child','other':'other-child','first':'first-child','id':'idtestChild','initials':'ini'}", \
        #     response.text.replace('\n','').replace(' ','').replace(' ',''))
        response=restGet('person-to-person')
        # print response.text.replace('\n','').replace(' ','')

        # ------------------check the parent-child relation------------------
        self.assertIn('{"person1":"idtestParent","person2":"idtestChild","relation":"gurushishya"}', \
            response.text.replace('\n','').replace(' ',''))
    # def test_modify_persons(self):
        # -----------------modify the parent----------------------
        response = restPut('person/idtestParent',{'id': 'idtestParent','first': 'first-parent-update','last': 'last-parent-update', \
                                                   'death':'2013-6-29'})
        # print ('modify person .. status:', response.status_code, '\n',response.text)
        self.assertEqual(201,response.status_code)
        # print ('modify persons .. status:', response.status_code, '\n', response.text.replace('\n','').replace(' ',''))
        # self.assertEqual( "{'last': 'last-parent-update', 'middle': 'middle', 'nick': 'nick', 'other': 'other', 'first': 'first-parent-update', \
        #                   'id': 'idtest', 'initials': 'ini'}", \
        #     response.text.replace('\n','').replace(' ',''))
        self.assertIn('"first":"first-parent-update"',response.text.replace('": "','":"').replace('\n',''))
        self.assertIn('"last":"last-parent-update"',response.text.replace('": "','":"').replace('\n',''))
        self.assertIn('"middle":null',response.text.replace('": ','":').replace('\n',''))
        self.assertIn('"nick":null',response.text.replace('": ','":').replace('\n',''))
        self.assertIn('"initials":null',response.text.replace('": ','":').replace('\n',''))
        self.assertIn('"other":null',response.text.replace('": ','":').replace('\n',''))
        self.assertIn('"death":"2013-6-29"',response.text.replace('": "','":"').replace('\n',''))

        # -------------------get the parent--------------------------
        response = restGet('person/idtestParent')
        self.assertEqual(200,response.status_code)

        # ------------------modify the child & the relation order-------------------------------
        response = restPut('person/idtestChild',{'id': 'idtestChild','first': 'first-child-update','last': 'last-child-update', \
                                                   'relation': 'classmate'})
        self.assertEqual(201,response.status_code)
        # response = restGet('subject/idtestChild')
        # print 'status:', response.status_code, '\n', response.text.replace('\n','').replace(' ','')
        response_text = response.text.replace('\n','').replace(' ','').replace(' ','')
        self.assertIn('"first":"first-child-update"',response_text.replace('": "','":').replace('\n',''))
        self.assertIn('"last":"last-child-update"',response_text.replace('": "','":').replace('\n',''))
        self.assertIn('"middle":null',response_text.replace('": "','":').replace('\n',''))
        self.assertIn('"nick":null',response_text.replace('": "','":').replace('\n',''))
        self.assertIn('"initials":null',response_text.replace('": "','":').replace('\n',''))
        self.assertIn('"other":null',response_text.replace('": "','":').replace('\n',''))
    # def test_remove_persons(self):
        # ------------------remove the child & its relation-------------
        response = restDelete('person-with-relation/idtestChild')
        # print 'status:', response.status_code, '\n',response.text
        self.assertEqual(200,response.status_code)
        # ----------------------remove the parent-------------------
        response = restDelete('person/idtestParent')
        # print ('remove persons .. status:', response.status_code, '\n',response.text)
        self.assertEqual(200,response.status_code)
        # ----------------------remove the sample person-------------------
        response = restDelete('person/idtest')
        self.assertEqual(200,response.status_code)
    def test_person_to_work(self):
        get_services = ['person-work-relations','person-to-work']
        for service in get_services:
            response = restGet(service)
            # print response.text
            self.assertEqual(200,response.status_code)
         # ----------------create sample persons --------------------------
        for person in {'idtest_person1','idtest_person2','idtest_person3','idtest_person4'}:
            response =  restPost('person',{"id": person, "first": "first", "last": "last","middle": "middle",   \
                                  "initials": "ini", "nick":"nick", "other":"other"})
            self.assertEqual(201,response.status_code)
            self.assertIn(person,response.text)
        # ----------------create sample works --------------------------
        for work in {'idtest_work1','idtest_work2','idtest_work3','idtest_work4'}:
            response =  restPost('work',{'id': work,'name': 'name-test','description': 'description-test'})
            self.assertEqual(201,response.status_code)
            self.assertIn(work,response.text)
        # ----------------create person work relations --------------------------
        for work in {'idtest_work1','idtest_work2','idtest_work3'}:
            response =  restPost('person-to-work',{'person': 'idtest_person1','work': work,'relation': 'pramaana_pramatha'})
            self.assertEqual(200,response.status_code)
            # print('person to work..',response.status_code)
            self.assertIn('"result":true',response.text.replace('": ','":').replace('\n',''))
        for person in {'idtest_person2','idtest_person3','idtest_person4'}:
            response =  restPost('person-to-work',{'person': person,'work': 'idtest_work4','relation': 'pramaana_pramatha'})
            self.assertEqual(200,response.status_code)
            # print('person to work..',response.text)
            self.assertIn('"result":true',response.text.replace('": ','":').replace('\n',''))
        # ----------------get person-to-work tree--------------------------
        # gpers = restGet('tree-person-work/idtest_person1')
        # json.dump(gpers.content, open('jsondata/knowledgeTree-person-work-tree.json','w'))
        # # ----------------get work-to-person tree--------------------------
        # gwrk = restGet('tree-work-person/idtest_work4')
        # json.dump(gwrk.content, open('jsondata/knowledgeTree-work-person-tree.json','w'))
        # ----------------remove all person work relations created--------------------------
        for work in {'idtest_work1','idtest_work2','idtest_work3'}:
            response =  restDeletewithData('person-to-work',{'person': 'idtest_person1','work': work,'relation': 'pramaana_pramatha'})
            self.assertEqual(200,response.status_code)
            self.assertIn('"result":true',response.text.replace('": ','":').replace('\n',''))
        for person in {'idtest_person2','idtest_person3','idtest_person4'}:
            response =  restDeletewithData('person-to-work',{'person': person,'work': 'idtest_work4','relation': 'pramaana_pramatha'})
            self.assertEqual(200,response.status_code)
            self.assertIn('"result":true',response.text.replace('": ','":').replace('\n',''))
        # remove the persons created
        for person in {'idtest_person1','idtest_person2','idtest_person3','idtest_person4'}:
            response = restDelete('person/' + person)
            self.assertEqual(200,response.status_code)
        # remove the works created
        for work in {'idtest_work1','idtest_work2','idtest_work3','idtest_work4'}:
            response = restDelete('work/' + work)
            self.assertEqual(200,response.status_code)
    def tearDown(self):
        # ------------------remove the child & its relation-------------
        response = restDelete('subject-with-relation/idtestChild')
        # ----------------------remove the parent-------------------
        response = restDelete('subject/idtestParent')
        # ----------------------remove the sample subjects-------------------
        response = restDelete('subject/idtest')
        response = restDelete('subtree/idtestSource')
        response = restDelete('subtree/idtestTarget')
        for id in ['idtestChild1','idtestChild2','idtestChild3']:
            response = restDelete('subject-with-relation/' + id)
        # ------------------remove the child & its relation-------------
        response = restDelete('work-with-relation/idtestChild')
        # ----------------------remove the parent-------------------
        response = restDelete('work/idtestParent')
        # ----------------------remove the sample work-------------------
        response = restDelete('work/idtest')
        response = restDelete('subtree-work/idtestSource')
        response = restDelete('subtree-work/idtestTarget')
        for id in ['idtestChild1', 'idtestChild2', 'idtestChild3']:
            response = restDelete('work-with-relation/' + id)
        # ------------------remove the child & its relation-------------
        response = restDelete('person-with-relation/idtestChild')
        # ----------------------remove the parent-------------------
        response = restDelete('person/idtestParent')
        # ----------------------remove the sample person-------------------
        response = restDelete('person/idtest')
        # remove the subjects created
        for subject in {'idtest_subject1','idtest_subject2','idtest_subject3','idtest_subject4'}:
            response = restDelete('subtree/' + subject)
        # remove the works created
        for work in {'idtest_work1','idtest_work2','idtest_work3','idtest_work4'}:
            response = restDelete('subtree-work/' + work)
        # remove the persons created
        for person in {'idtest_person1','idtest_person2','idtest_person3','idtest_person4'}:
            response = restDelete('person/' + person)
        # remove the works created
        for work in {'idtest_work1','idtest_work2','idtest_work3','idtest_work4'}:
            response = restDelete('work/' + work)

if __name__ == '__main__':
    unittest.main()