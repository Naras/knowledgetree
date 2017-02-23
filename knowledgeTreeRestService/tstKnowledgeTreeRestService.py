__author__ = 'NarasMG'
import json, requests #, pprint

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
    response = requests.get(completeUrl,auth=('mathi',get_password('mathi')))
    return response
def restPost(url,data):
    completeUrl = prefix + url
    print 'Posting:',  completeUrl
    return requests.post(completeUrl, json = data, auth=('mathi',get_password('mathi')))
def restPut(url,data):
    completeUrl = prefix + url
    print 'Putting:',  completeUrl
    return requests.put(completeUrl, json = data, auth=('mathi',get_password('mathi')))
def restDelete(url):
    completeUrl = prefix + url
    print 'Deleting:',  completeUrl
    return requests.delete(completeUrl,auth=('mathi',get_password('mathi'))) #  headers = {'Content-type': 'application/json'})
def main():
    # f =  open("credentials_roles.txt")
    # print f.readlines()
    # f.close
    # auths = json.load(open("credentials_roles.txt"))
    # print auths, type(auths)
    get_services = ['subjects','subject-to-subject','subject-subject-relations']
    for service in get_services:
        response = restGet(service)
        print 'status:', response.status_code, '\n', response.text

    response =  restPost('subject',{'id': 'idtestParent','name': 'name-test-parent','description': 'description-test-parent'})
    print 'status:', response.status_code, '\n',response.text
    response = restPost('subject-with-relation', \
                    {"subject": {"id": "idtestChild", "name": "name-test-child", "description": "description-test-child"}, "related": "idtestParent", "relation": "Anga" })
    print 'status:', response.status_code, '\n',response.text
    # # pprint.pprint(response.json())
    response =  restPut('subject/idtestParent',{'id': 'idtestParent','name': 'name-test-parent-update','description': 'description-test-parent-update'})
    print 'status:', response.status_code, '\n',response.text
    response = restGet('subject/idtestParent')
    print 'status:', response.status_code, '\n', response.text
    response = restGet('subject/idtestChild')
    print 'status:', response.status_code, '\n', response.text

    response = restDelete('subject-with-relation/idtestChild')
    print 'status:', response.status_code, '\n',response.text
    response = restDelete('subject/idtestParent')
    print 'status:', response.status_code, '\n',response.text

if __name__ == '__main__':
    main()