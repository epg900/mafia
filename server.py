from flask import Flask, send_file, redirect,  render_template, request
import os, glob, random, json

root_path = os.getcwd()
abs_path = os.path.join(root_path,'file') # '/storage/emulated/0/Download' # 'C:/Users/e/Desktop/epfs2-main/file' , '/home/user/Desktop/mafia/file'


def readjson(file):
    f = open(file, 'r', encoding='utf-8')
    jsondict = json.load(f)
    f.close()
    return jsondict

allsenario = {}
if os.path.exists(f'{abs_path}/allsenario.txt'):
    allsenario = readjson("file/allsenario.txt")
else:
    allsenario = readjson("file/allsenario_base.txt")
        
app = Flask(__name__, static_url_path='/static', static_folder = root_path, template_folder = root_path)

@app.route('/')
def index():
    lst = []
    for i in allsenario['a']:
        lst.append(allsenario['a'][i]['name'])

    
    return render_template('index.html', path = abs_path , all_list = lst , var1 = 1  )

@app.route('/img/<rolename>')
def sendf(rolename):
    file = f"{abs_path}/allrole/{rolename}.jpg"
    return send_file(file)
   
@app.route('/<sen>')
@app.route('/<sen>/<sit>')
def run_game(sen,sit=None):    
    lst = []
    
    for i in allsenario['a']:
        if allsenario['a'][i]['name'] == sen:
            lst = allsenario['a'][i]['roles']            
            
    lst.sort()    
    random.shuffle(lst)
    
    maplst = ['1','2','3','4','5','6','7','8','9','q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l']
    
    lst2 = allsenario['b']
    
    lst3=[]
    for l in lst2:
        if l in lst:
            lst3.append(l)
    random.shuffle(lst3)
    
    if sit:
        e=sit                       
        for i,v in enumerate(e):
            ixref = maplst.index(e[i])+1
            if ixref:
                if len(lst) >= ixref:
                    ix1=lst.index(lst3[i])
                    iv1=lst[ixref-1]
                    lst[ixref-1]=lst3[i]
                    lst[ix1]=iv1   
    
    length=len(lst)

    return render_template('index.html', abs_path = abs_path , all_list = lst , length = length , var1 = 2 )       
    

@app.route('/custom')
def custom():
    all_dict = {}    
    for i in allsenario['c']:
        all_dict[i['role']] = i['name']
    length = 36
    return render_template('index.html', abs_path = abs_path , all_list = all_dict , length = length , var1 = 3 ) 

@app.route('/makecustom', methods = ['GET', 'POST'])
def makecustom():
    all_list = []
    if request.method == 'POST':
        all_list = request.form.getlist('roles')

    all_dict = { "name" : request.form.get('senname') , "roles" : all_list }
    length = len(allsenario['a'])
    allsenario['a'][f"{length+1}"] = all_dict
    f = open('file/allsenario.txt', 'w', encoding='utf-8')
    json.dump(allsenario,f,indent=4)
    f.close()
    
    return redirect('/')

@app.route('/delcustoms')
def delcustoms():
    os.remove('file/allsenario.txt')
    return redirect('/') 


@app.route('/uploader' , methods = ['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        files = request.files.getlist("file")
        for f in files:
            f.save(f'{abs_path}/custom/{f.filename}')
    return redirect('/')

app.run(host="0.0.0.0")

