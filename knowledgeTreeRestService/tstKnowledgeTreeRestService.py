__author__ = 'NarasMG'
import json, requests, unittest #, pprint

# prefix = 'http://ec2-35-165-187-16.us-west-2.compute.amazonaws.com:5000/knowledgeTree/api/v1.0/'
prefix = 'http://127.0.0.1:5000/knowledgeTree/api/v1.0/'
# echoservice = 'http://httpbin.org/post'
def ceasar(plain,shift):  # shift each letter by shift
        return "".join([chr((ord(x)- start(x) + shift) % 26 + start(x)) for (x) in list(plain)])
def start(alphabet): # find distance between alphabet and 'a' or 'A'
            strt = ord('a') if alphabet.islower() else ord('A')
            return strt
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
def restGet(url):
    completeUrl = prefix + url
    print 'Retrieving:',  completeUrl
    response = requests.get(completeUrl,auth=('pankaja',get_password('pankaja')))
    return response
def restPost(url,data):
    completeUrl = prefix + url
    print 'Posting:',  completeUrl
    return requests.post(completeUrl, json = data, auth=('pankaja',get_password('pankaja')))
def restPut(url,data):
    completeUrl = prefix + url
    print 'Putting:',  completeUrl
    return requests.put(completeUrl, json = data, auth=('pankaja',get_password('pankaja')))
def restDelete(url):
    completeUrl = prefix + url
    print 'Deleting:',  completeUrl
    return requests.delete(completeUrl,auth=('pankaja',get_password('pankaja'))) #  headers = {'Content-type': 'application/json'})
class TestUM(unittest.TestCase):
    def setUp(self):
        pass
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
            self.assertEqual(response.status_code,200)
    def test_create_subjects(self):
        # ----------------create a sample subject--------------------------
        response =  restPost('subject',{'id': 'idtest','name': 'name-test','description': 'description-test'})
        self.assertEqual(response.status_code,201)
        self.assertIn('idtest',response.text)
        # ----------------create a duplicate of the subject--------------------------
        '''
        response = restPost('subject',{"id": "idtest", "name": "name-test-duplicate", "description": "description-test-duplicate"})
        self.assertEqual(response.status_code,201)
        # print "attempt to create duplicate:", response.text
        self.assertIn('idtest',response.text,'duplicate created')
        '''
        # ----------------create a parent subject--------------------------
        response =  restPost('subject',{'id': 'idtestParent','name': 'name-test-parent','description': 'description-test-parent'})
        # print 'status:', response.status_code, '\n',response.text
        # create a child subject
        response = restPost('subject-with-relation', \
                        {"subject": {"id": "idtestChild", "name": "name-test-child", "description": "description-test-child"},
                         "related": "idtestParent", "relation": "Anga","sortorder": 65 })
        self.assertEqual(response.status_code,200)
        self.assertEqual ('{"subject":true}',response.text.replace('\n','').replace(' ',''))
        # print 'status:', response.status_code, '\n',response.text.replace('\n','')
        # # pprint.pprint(response.json())

        # create a duplicate child subject
        '''
        response = restPost('subject-with-relation', \
                        {"subject": {"id": "idtestChild", "name": "name-test-child-duplicate", "description": "description-test-child-duplicate"},
                         "related": "idtestParent", "relation": "Anga","sortorder": 65 })
        self.assertEqual(response.status_code,200)
        self.assertEqual ('{"subject":true}',response.text.replace('\n','').replace(' ',''))
        '''
        # ----------------get the parent subject------------------
        response=restGet('subject/idtestParent')
        self.assertEqual(response.status_code,200)
        self.assertEqual( \
        '{"subject":{"description":"description-test-parent","id":"idtestParent","name":"name-test-parent"}}', \
            response.text.replace('\n','').replace(' ',''))
        # print 'status:', response.status_code, '\n',response.text.replace('\n','').replace(' ','')

        # -----------------get the child subject-----------------
        response=restGet('subject/idtestChild')
        self.assertEqual(response.status_code,200)
        self.assertEqual( \
        '{"subject":{"description":"description-test-child","id":"idtestChild","name":"name-test-child"}}', \
            response.text.replace('\n','').replace(' ','').replace(' ',''))
        response=restGet('subject-to-subject')
        # print response.text.replace('\n','').replace(' ','')

        # ------------------check the parent-child relation------------------
        self.assertIn( \
        '{"relation":"Anga","sortorder":65,"subject1":"idtestParent","subject2":"idtestChild"}', \
            response.text.replace('\n','').replace(' ',''))
    def test_modify_subjects(self):
        # -----------------modify the parent----------------------
        response =  restPut('subject/idtestParent',{'id': 'idtestParent','name': 'name-test-parent-update','description': 'description-test-parent-update'})
        # print 'status:', response.status_code, '\n',response.text
        self.assertEqual(response.status_code,201)
        # print 'status:', response.status_code, '\n', response.text.replace('\n','').replace(' ','')
        self.assertEqual( \
        '{"subject":{"description":"description-test-parent-update","id":"idtestParent","name":"name-test-parent-update"}}', \
            response.text.replace('\n','').replace(' ',''))

        # -------------------get the parent--------------------------
        response = restGet('subject/idtestParent')
        self.assertEqual(response.status_code,200)

        # ------------------modify the child & the relation order-------------------------------
        response =  restPut('subject/idtestChild',{'id': 'idtestChild','name': 'name-test-child-update','description': 'description-test-child-update', \
                                                   'relation': 'Dharma','sortorder':'78'})
        self.assertEqual(response.status_code,201)
        # response = restGet('subject/idtestChild')
        # print 'status:', response.status_code, '\n', response.text.replace('\n','').replace(' ','')
        self.assertEqual( \
        '{"subject":{"description":"description-test-child-update","id":"idtestChild","name":"name-test-child-update"}}', \
            response.text.replace('\n','').replace(' ',''))
    def test_remove_subjects(self):
        # ------------------remove the child & its relation-------------
        response = restDelete('subject-with-relation/idtestChild')
        # print 'status:', response.status_code, '\n',response.text
        self.assertEqual(response.status_code,200)
        # ----------------------remove the parent-------------------
        response = restDelete('subject/idtestParent')
        # print 'status:', response.status_code, '\n',response.text
        self.assertEqual(response.status_code,200)
        # ----------------------remove the sample subject-------------------
        response = restDelete('subject/idtest')
        self.assertEqual(response.status_code,200)

    def test_works(self):
        get_services = ['works','work-to-work','work-work-relations']
        for service in get_services:
            response = restGet(service)
            # print response.text
            self.assertEqual(response.status_code,200)
    def test_create_works(self):
        # ----------------create a sample work--------------------------
        response =  restPost('work',{'id': 'idtest','name': 'name-test','description': 'description-test'})
        self.assertEqual(response.status_code,201)
        self.assertIn('idtest',response.text)
        # ----------------create a duplicate of the work--------------------------
        '''
        response = restPost('work',{"id": "idtest", "name": "name-test-duplicate", "description": "description-test-duplicate"})
        self.assertEqual(response.status_code,201)
        # print "attempt to create duplicate:", response.text
        self.assertIn('idtest',response.text,'duplicate created')
        '''
        # ----------------create a parent work--------------------------
        response =  restPost('work',{'id': 'idtestParent','name': 'name-test-parent','description': 'description-test-parent'})
        # print 'status:', response.status_code, '\n',response.text
        # create a child work
        response = restPost('work-with-relation', \
                        {"work": {"id": "idtestChild", "name": "name-test-child", "description": "description-test-child"},
                         "related": "idtestParent", "relation": "derived","sortorder": 65 })
        self.assertEqual(response.status_code,200)
        self.assertEqual ('{"work":true}',response.text.replace('\n','').replace(' ',''))
        # print 'status:', response.status_code, '\n',response.text.replace('\n','')
        # # pprint.pprint(response.json())

        # create a duplicate child work
        '''
        response = restPost('work-with-relation', \
                        {"work": {"id": "idtestChild", "name": "name-test-child-duplicate", "description": "description-test-child-duplicate"},
                         "related": "idtestParent", "relation": "commentary","sortorder": 65 })
        self.assertEqual(response.status_code,200)
        self.assertEqual ('{"subject":true}',response.text.replace('\n','').replace(' ',''))
        '''
        # ----------------get the parent work------------------
        response=restGet('work/idtestParent')
        self.assertEqual(response.status_code,200)
        self.assertEqual( \
        '{"work":{"description":"description-test-parent","id":"idtestParent","name":"name-test-parent"}}', \
            response.text.replace('\n','').replace(' ',''))
        # print 'status:', response.status_code, '\n',response.text.replace('\n','').replace(' ','')

        # -----------------get the child work-----------------
        response=restGet('work/idtestChild')
        self.assertEqual(response.status_code,200)
        self.assertEqual( \
        '{"work":{"description":"description-test-child","id":"idtestChild","name":"name-test-child"}}', \
            response.text.replace('\n','').replace(' ','').replace(' ',''))
        response=restGet('work-to-work')
        # print response.text.replace('\n','').replace(' ','')

        # ------------------check the parent-child relation------------------
        self.assertIn( \
        '{"relation":"derived","sortorder":65,"work1":"idtestParent","work2":"idtestChild"}', \
            response.text.replace('\n','').replace(' ',''))
    def test_modify_works(self):
        # -----------------modify the parent----------------------
        response =  restPut('work/idtestParent',{'id': 'idtestParent','name': 'name-test-parent-update','description': 'description-test-parent-update'})
        # print 'status:', response.status_code, '\n',response.text
        self.assertEqual(response.status_code,201)
        # print 'status:', response.status_code, '\n', response.text.replace('\n','').replace(' ','')
        self.assertEqual( \
        '{"work":{"description":"description-test-parent-update","id":"idtestParent","name":"name-test-parent-update"}}', \
            response.text.replace('\n','').replace(' ',''))

        # -------------------get the parent--------------------------
        response = restGet('work/idtestParent')
        self.assertEqual(response.status_code,200)

        # ------------------modify the child & the relation order-------------------------------
        response =  restPut('work/idtestChild',{'id': 'idtestChild','name': 'name-test-child-update','description': 'description-test-child-update', \
                                                   'relation': 'volume','sortorder':'78'})
        self.assertEqual(response.status_code,201)
        # response = restGet('subject/idtestChild')
        # print 'status:', response.status_code, '\n', response.text.replace('\n','').replace(' ','')
        self.assertEqual( \
        '{"work":{"description":"description-test-child-update","id":"idtestChild","name":"name-test-child-update"}}', \
            response.text.replace('\n','').replace(' ',''))
    def test_remove_works(self):
        # ------------------remove the child & its relation-------------
        response = restDelete('work-with-relation/idtestChild')
        # print 'status:', response.status_code, '\n',response.text
        self.assertEqual(response.status_code,200)
        # ----------------------remove the parent-------------------
        response = restDelete('work/idtestParent')
        # print 'status:', response.status_code, '\n',response.text
        self.assertEqual(response.status_code,200)
        # ----------------------remove the sample subject-------------------
        response = restDelete('work/idtest')
        self.assertEqual(response.status_code,200)


if __name__ == '__main__':
    unittest.main()