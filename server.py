from flask import Flask, send_file, redirect,  render_template, request
import os, glob, random

root_path = os.getcwd()
abs_path = os.path.join(root_path,'file') # '/storage/emulated/0/Download' # 'C:/Users/e/Desktop/epfs2-main/file' , '/home/user/Desktop/mafia/file'
lst = []
files = os.listdir(abs_path)
for f in files:
    if os.path.isdir(os.path.join(abs_path,f)):
        lst.append(f)        
        
app = Flask(__name__, static_url_path='/static', static_folder = root_path, template_folder = root_path)

@app.route('/')
def index():    
    return render_template('index.html', path = abs_path , all_list = lst , var1 = 1  )
    
@app.route('/<path>')
@app.route('/<path>/<sit>')
def run_game(path,sit=None):
    if not os.path.exists(f'{abs_path}/{path}'):
        return redirect('/')
    if not os.path.isdir(f'{abs_path}/{path}'):
        return redirect('/')

    lst =glob.glob(f"{abs_path}/{path}/*.jpg")
    lst.sort()
    lst=[l.split("/")[-1] for l in lst]
    lst=[l.split("\\")[-1] for l in lst]
    random.shuffle(lst)
    
     		
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
                if int(e[i]):
                    if len(lst) >= int(e[i]):
                        ix1=lst.index(lst3[i])
                        iv1=lst[int(e[i])-1]
                        lst[int(e[i])-1]=lst3[i]
                        lst[ix1]=iv1   
    
    length=len(lst)

    #return f"senario is {path} <br><br>  lst :  {lst} <br><br> lst2 :  {lst2} <br><br> lst3 :  {lst3} <br><br> {length} "
    return render_template('index.html', path = path , abs_path = abs_path , all_list = lst , length = length , var1 = 2 , lst2 = lst2 , lst3 = lst3)
        
    

@app.route('/img/<path>/<filepath>')
def uploader(path,filepath):
    file = f"{abs_path}/{path}/{filepath}"
    return send_file(file)

app.run(host="0.0.0.0")

