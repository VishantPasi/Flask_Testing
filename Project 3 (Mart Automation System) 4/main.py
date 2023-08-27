from flask import Flask,render_template,request,session,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import barcode 
from barcode.writer import ImageWriter
import json

local_server=True
with open('config.json','r') as c:
    params = json.load(c)["params"]


app = Flask(__name__)
app.secret_key = 'super-secret-key'


if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
     app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
db = SQLAlchemy(app)

class Purchase_info(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(120), nullable=False)
    product_name = db.Column(db.String(120), nullable=False)
    product_mrp = db.Column(db.Float, nullable=False)
    product_quant = db.Column(db.Integer, nullable=True)
    product_mrp_final = db.Column(db.Float, nullable=False)
    product_weight = db.Column(db.Float, nullable=False)
    product_weight_final = db.Column(db.Float, nullable=False)


class Product_info(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(120), nullable=False)
    product_name = db.Column(db.String(120), nullable=False)
    product_quant = db.Column(db.Integer, nullable=False)
    product_mrp = db.Column(db.Float, nullable=False)
    product_weight = db.Column(db.Float, nullable=False)

@app.route("/")
@app.route("/home")
def home():
     
            
            purchase = Purchase_info.query.filter_by().all()
            return render_template("index.html",params=params,purchase=purchase)

    
@app.route("/veri",methods = ['GET','POST'])
def veri():
     if request.method == "POST":
        username = request.form.get('Username')
        userpass = request.form.get('Password')
        
        if username == "" or username == None:
             print("Eroor in 0nd block")
             return redirect("/home")
        elif username==params['user_name'] and userpass == params['user_pass']:
            session['user'] = username
            print("Eroor in dashadmin")
            return redirect("/dashadmin")
        elif username==params['nor_user'] and userpass == params['nor_pass']:
            session['user'] = username
            print("Eroor in dashinfo")
            return redirect("/dashinfo")
        elif username != params['user_name'] and userpass != params['user_pass']:
            print("Eroor in 1nd block")
            return redirect("/home")
        elif username != params['nor_user'] and userpass != params['nor_pass']:
            print("Eroor in newd block")
            return redirect("/home")
        elif ((username != params['user_name'] and userpass == params['user_pass']) or (username == params['user_name'] and userpass != params['user_pass'])) or ((username != params['nor_user'] and userpass == params['nor_pass']) or (username == params['nor_user'] and userpass != params['nor_pass']))  :
            print("Eroor in 2nd block")
            return redirect("/home")
        
        
        
        
        
        
        
@app.route("/dashadmin" ,methods=['GET','POST'])
def dashadmin():
    if "user" in session and session['user']==params['user_name']:
            posts = Product_info.query.all()
            return render_template("dash_admin.html",params=params,purchase=posts)
    else:
            return redirect("error.html")
    

@app.route("/dashinfo" ,methods=['GET','POST'])
def dashinfo():
    
    if "user" in session and session['user']==params['nor_user']:
            
            post = Purchase_info.query.all()
            return render_template("dash_info.html",params=params,purchase=post)
    
    else:
            return redirect("error.html")


@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/home')
     
@app.route("/edit_a/<string:sno>", methods = ['GET','POST'])
def edita(sno):
    if "user" in session and session['user']==params['user_name']:
        if request.method == 'POST':
                box_product_id = request.form.get('product_id')
                box_product_name = request.form.get('product_name')
                box_product_mrp = request.form.get('product_mrp')
                box_product_quantity = request.form.get('product_quantity')   
                date = datetime.now()
                
                if sno == '0':
                    post = Product_info(product_id = box_product_id,product_name = box_product_name, product_mrp = box_product_mrp ,product_quant = box_product_quantity)
                    db.session.add(post)
                    db.session.commit()
                    return redirect('/dashadmin')
                else:
                
                    post = Product_info.query.filter_by(sno=sno).first()
                    if  post != None:
                        post.product_id = box_product_id
                        post.product_name = box_product_name
                        post.product_mrp = box_product_mrp
                        post.product_quant = box_product_quantity
                        post.date=date
                
                        db.session.commit()
                        return redirect('/dashadmin')
                    else:
                        return redirect("error.html")
        post = Product_info.query.filter_by(sno=sno).first()
        return render_template('edit_a.html',params=params,post=post,sno=sno)
    else:
         return render_template("error.html")
    
@app.route("/edit_u/<string:sno>", methods = ['GET','POST'])
def editu(sno):
    if "user" in session and session['user']==params['nor_user']:
        if request.method == 'POST':
                box_product_id = request.form.get('product_id')
                box_product_name = request.form.get('product_name')
                box_product_mrp = request.form.get('product_mrp')
                box_product_quantity = request.form.get('product_quantity') 
                box_product_weight = request.form.get('product_weight') 
                
                
                if sno == '0':
                    post = Purchase_info(product_id = box_product_id,product_name = box_product_name, product_mrp = box_product_mrp ,product_quant = box_product_quantity,product_weight= box_product_weight)
                    db.session.add(post)
                    db.session.commit()
                    return redirect('/dashinfo')
                else:
                
                    post = Purchase_info.query.filter_by(sno=sno).first()
                    if  post != None:
                        post.product_id = box_product_id
                        post.product_name = box_product_name
                        post.product_mrp = box_product_mrp
                        post.product_quant = box_product_quantity
                        post.product_mrp_final=(float(box_product_mrp)*float(box_product_quantity))
                        post.product_weight_final = (float(box_product_quantity)*float(box_product_weight))
                
                        db.session.commit()
                        return redirect('/dashinfo')
                    else:
                        return redirect("error.html")
        post = Purchase_info.query.filter_by(sno=sno).first()
        return render_template('edit_u.html',params=params,post=post,sno=sno)
    else:
         return render_template("error.html")


    
@app.route("/delete_a/<string:sno>", methods = ['GET','POST'])
def deletea(sno):
    if "user" in session and session['user']==params['user_name']:
        post = Product_info.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
        return redirect('/dashadmin')
    else:
         return render_template("error.html")
    
@app.route("/delete_u/<string:sno>", methods = ['GET','POST'])
def deleteu(sno):
    if "user" in session and session['user']==params['nor_user']:
        post = Purchase_info.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
        return redirect('/dashinfo')
    else:
         return render_template("error.html")

@app.route("/0",methods=['GET','POST'])   
def fetch():
        if request.method == 'POST':
            pro = request.form.get("prod_id")
            p_id = pro
            print(pro)
            return redirect("/0/"+p_id)

@app.route("/0/<string:product_id>" ,methods=['GET','POST'])
def ed(product_id):
            
                
                post = Product_info.query.all()
                    
                
            
                
                if  post != None:
                        
                            post1 = Product_info.query.filter_by(product_id=product_id).first()
                            if post1 != None:
                                pr_id =  post1.product_id
                                pr_name = post1.product_name
                                pr_mrp = post1.product_mrp
                                pr_quant = post1.product_quant
                                pr_weight = post1.product_weight
                                


                                pur =  Purchase_info(product_id = pr_id, product_name = pr_name, product_mrp = pr_mrp,product_quant = pr_quant,product_mrp_final=pr_mrp*pr_quant,product_weight = pr_weight,product_weight_final = pr_weight*pr_quant )
                                db.session.add(pur)
                                db.session.commit()
                                return redirect("/dashinfo")
                            else:
                                return render_template("wrong_product.html")
                return render_template("dash_info.html",pro = product_id)



@app.route("/success")
def success():
      return render_template("success.html")

@app.route("/barcode/<string:sno>" ,methods=['GET','POST'])
def bar(sno):
    if "user" in session and session['user']==params['user_name']:
        post = Product_info.query.filter_by(sno=sno).first()
        pro_id = post.product_id

        hr = barcode.get_barcode_class('code128')
        
        Hr =hr(pro_id)
        Hr.save("C:/Users/Vishant-PC/Desktop/Programs/FLASK/Project 3 (Mart Automation System) 4/static/Assets/imgs/Id")
        return render_template("bar.html",params=params)
    else:
        return redirect("error.html")

@app.route("/Bill" ,methods=['GET','POST'])
def bill():
    if "user" in session and session['user']==params['nor_user']:
        post = Purchase_info.query.all()
        date=datetime.now()
        return render_template("Bill.html",purchase=post,date =date)




app.run(debug=True, host ='0.0.0.0')