from flask import Flask, send_file, redirect,  render_template, request
import os, glob, random, json

root_path = os.getcwd()
abs_path = os.path.join(root_path,'file') # '/storage/emulated/0/Download' # 'C:/Users/e/Desktop/epfs2-main/file' , '/home/user/Desktop/mafia/file'


def readjson(file):
    with open(file, 'r') as file:
        jsondict = json.load(file)

    return jsondict

allsenario = readjson("file/allsenario.txt")    
        
app = Flask(__name__, static_url_path='/static', static_folder = root_path, template_folder = root_path)

@app.route('/')
def index():
    lst = []
    for i in allsenario:
        lst.append(allsenario[i]['name'])

    
    return render_template('index.html', path = abs_path , all_list = lst , var1 = 1  )

@app.route('/img/<rolename>')
def sendf(rolename):
    file = f"{abs_path}/allrole/{rolename}.jpg"
    return send_file(file)
   
@app.route('/<sen>')
@app.route('/<sen>/<sit>')
def run_game(sen,sit=None):    
    lst = []
    
    for i in allsenario:
        if allsenario[i]['name'] == sen:
            lst = allsenario[i]['roles']            
            
    lst.sort()    
    random.shuffle(lst)
    
    maplst = ['1','2','3','4','5','6','7','8','9','q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l']
    
    file=open(f"{abs_path}/role.txt","r",encoding="utf-8")
    lst2=file.readlines()
    file.close()
    lst2=[l.strip() for l in lst2]
    lst2=[l.split("\n")[0] for l in lst2]
     		
    
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
        
    



@app.route('/uploader' , methods = ['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        files = request.files.getlist("file")
        for f in files:
            f.save(f'{abs_path}/custom/{f.filename}')
    return redirect('/')

app.run(host="0.0.0.0")

