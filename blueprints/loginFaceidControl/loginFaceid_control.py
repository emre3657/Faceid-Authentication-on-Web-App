from config import app
from database import connectDatabase
from model import model
from flask import request, redirect, url_for, session, Blueprint
import cv2
import face_recognition
import json
import numpy as np
import base64
import math
import jwt
import datetime

loginFaceid_control_bp = Blueprint('loginFaceid_control', __name__)


@app.route('/loginFaceid', methods=['POST'])
def loginFaceid():
    if request.method == 'POST':
        # Base64 kodlu görüntüyü NumPy dizisine dönüştürme
        img_data = request.form['img']
        img_data = img_data.split(",")[1]  # Veri URL'sinden veri kısmını ayır
        img_bytes = base64.b64decode(img_data)  # Base64 veriyi baytlara dönüştür
        nparr = np.frombuffer(img_bytes, np.uint8)  # Baytları NumPy dizisine dönüştür
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # NumPy dizisini görüntüye dönüştür

        # Yeni boyutlar
        new_width = 400
        new_height = 300

        # Görüntüyü yeniden boyutlandır
        img = cv2.resize(img, (new_width, new_height))
        
        distanceThreshold = 0.45 
        mycursor, mydb = connectDatabase()

        # SQLite sorgusunu çalıştır
        sql = "SELECT face_features FROM faceid"
        mycursor.execute(sql)
            
        # Veri tabanındaki bütün yüz verilerini al.
        yuz_oznitelik = mycursor.fetchall()
        
        yuz_oznitelik_sayac = 0
        for yuz in yuz_oznitelik:
            if yuz[0] != None:
                yuz_oznitelik_sayac += 1
        
        print("yüz veri sayısı:",yuz_oznitelik_sayac)
        
        # Eğer veri tabanında karşılaştırılacak bir veri yok ise:
        if yuz_oznitelik_sayac == 0:
            print("HATA:\nVeri tabaninda yüz verisi yok")
            mydb.close()
            return redirect(url_for('loginFaceid_messages.loginFaceid_warning_empty_database'))          
    
    
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Yüzü tespit et
        face = face_recognition.face_locations(img_rgb)

        # Birden fazla yüz var ise hata ver. HATA: Birden fazla yüz verisi girilemez.
        if len(face)>1:

            return redirect(url_for('loginFaceid_messages.loginFaceid_error_multiple_faces'))

        # Yüz kodunu bul
        encodedface = face_recognition.face_encodings(img_rgb, face)
        
        if len(encodedface) == 1:


            results = model(img, stream=True, verbose=False)
            confidence = 0.6
            classNames = ["fake", "real"]

            for r in results:
                boxes = r.boxes
                for box in boxes:
                    # Bounding Box
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    # cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)
                    # w, h = x2 - x1, y2 - y1
                    # Confidence
                    conf = math.ceil((box.conf[0] * 100)) / 100
                    
                    # Class Name
                    cls = int(box.cls[0])
                    if conf > confidence:
                        if classNames[cls] == 'real':
                            print("confmath:",conf)
            
                            print("This object is real.")
                            # Yüz kodlamasının bittiğini bildir
                            print("Yüz kodlamasi tamamlandi...")  

                        else:
                            print("This object is fake.")
                            return redirect(url_for('loginFaceid_messages.loginFaceid_error_fake_face'))
            
        else:
            return redirect(url_for('loginFaceid_messages.loginFaceid_no_face'))
        
        # Kamera karşsındaki yüz ile veri tabanındaki yüzlerin hiçbiri belli bir oranda eşleşmez ise kullanıcıyı bilgilendirmek gerekir.
        # Bunun için bir sayaç kullanacağız.
        sayac = 0

        # Eşleşen yüz için global değişken
        matched_face = None
        # Eşleşen yüz verisinin mesafe değeri için global değişken
        matched_faceDistance = None
        
        
        if yuz_oznitelik_sayac > 0:
            # Veri tabanında ki yüz verileri  ile kameradan gelen yüz arasında distance hesabı yapma.
            # Buradaki veri öğesi bir str(string)'dır. str'in içinde tuple verileri mevcuttur.
            for veri in yuz_oznitelik:

                if veri[0] is not None:
                
                    # json str veri tipi okur. str veri yapısı içinde tuple'lar mevcuttur.
                    # Tuple veriyi ayıklamamız lazım. json.load(veri[0]) verinin(tuple'nin) ilk elemanını listeye dönüştürür.
                    veri = (json.loads(veri[0]))
                
                    # Distance hesabı. Liste olan yüz verisini işlemeden önce np arrayine dönüştürüyoruz.
                    # Çünkü kıyaslama yapılırken iki veride aynı tipte olması gerekir.
                    faceDis = face_recognition.face_distance(encodedface, np.array(veri))
                    faceDis = round(faceDis[0], 4)
                    print("Face Distance: ",faceDis)

                    if faceDis < distanceThreshold:
                    
                        # sayacı bir (1) artır.
                        sayac +=1
                        matched_face = veri
                        matched_faceDistance = faceDis
                        break
            
            # Koşulu sağlayan yüzün ad verisini alma.
            # İlk önce array halinde olan yüz oznitelik verisini json formatına dönüştürüyoruz.
            mycursor.execute("SELECT username, token FROM faceid WHERE face_features = %s", (json.dumps(matched_face),))

        
            # Bu sorgu bir tuple verisi döndürür. Tuple'in 0. indekside ad sütünunu temsil eder.
            row = mycursor.fetchone()
            if row is not None:
                ad = row[0]
                token = row[1]
                #print(ad)
                print("Token: ", token)
    

            print("Giris Basarili\nWelcome ", ad)
            print("faceDistance: ", matched_faceDistance)
            print(f"sayac: {sayac}")

        
            if token != None:
                session['login_default_data'] = {
                    'token' : token,
                    'ad' : ad.upper(),
                    'face' : json.dumps(matched_face)
                }   
                print("Eski token kullanılmaya devam ediyor")
                print(token)
        
            else:
                token = jwt.encode({'user' : ad.upper(), 'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=10)}, app.config['SECRET_KEY'])
                mycursor.execute("UPDATE faceid set token = %s WHERE face_features = %s", (token, (json.dumps(matched_face))))
            
                session['login_default_data'] = {
                    'token' : token,
                    'ad' : ad.upper(),
                    'face' : json.dumps(matched_face)
                }
                print("session yeniden oluşturuldu")
                print('New Token: ', token)
    
            mydb.commit()
            mydb.close()
        
            # Kullanılan kaynakları serbest bırak
            # cap.release()
            cv2.destroyAllWindows()
            return redirect(url_for('loginFaceid_messages.login_success_faceid'))
        
        # Eğer veri tabanında karşılaştırılacak bir veri var ise:
        """if yuz_oznitelik_sayac > 0:

            # Veri tabanında ki yüz verileri  ile kameradan gelen yüz arasında distance hesabı yapma.
            # Buradaki veri öğesi bir str(string)'dır. str'in içinde tuple verileri mevcuttur.
            for veri in yuz_oznitelik:

                if veri[0] is not None:
                    

                    # json str veri tipi okur. str veri yapısı içinde tuple'lar mevcuttur.
                    # Tuple veriyi ayıklamamız lazım. json.load(veri[0]) verinin(tuple'nin) ilk elemanını listeye dönüştürür.
                    veri = (json.loads(veri[0]))
                    
                    # Distance hesabı. Liste olan yüz verisini işlemeden önce np arrayine dönüştürüyoruz.
                    # Çünkü kıyaslama yapılırken iki veride aynı tipte olması gerekir.
                    faceDis = face_recognition.face_distance(encodedface, np.array(veri))
                    faceDis = round(faceDis[0], 4)
                    print("Face Distance: ",faceDis)

                    if faceDis < distanceThreshold:
                        
                        # sayacı bir (1) artır.
                        sayac +=1
                        matched_face = veri
                        matched_faceDistance = faceDis"""
                       
        
        """if sayac == 1:
            # Koşulu sağlayan yüzün ad verisini alma.
            # İlk önce array halinde olan yüz oznitelik verisini json formatına dönüştürüyoruz.
            mycursor.execute("SELECT username, token FROM faceid WHERE face_features = %s", (json.dumps(matched_face),))

            
            # Bu sorgu bir tuple verisi döndürür. Tuple'in 0. indekside ad sütünunu temsil eder.
            row = mycursor.fetchone()
            if row is not None:
                ad = row[0]
                token = row[1]
                # print(ad)
                print("Token: ", token)
        

            print("Giris Basarili\nWelcome ", ad)
            print("faceDistance: ", matched_faceDistance)
            print(f"sayac: {sayac}")

            
            if token != None:
                session['login_default_data'] = {
                    'token' : token,
                    'ad' : ad.upper(),
                    'face' : json.dumps(matched_face)
                }
                print("Eski token kullanılmaya devam ediyor")
                print(token)
            
            else:
                token = jwt.encode({'user' : ad.upper(), 'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=10)}, app.config['SECRET_KEY'])
                mycursor.execute("UPDATE faceid set token = %s WHERE face_features = %s", (token, (json.dumps(matched_face))))
                
                session['login_default_data'] = {
                    'token' : token,
                    'ad' : ad.upper(),
                    'face' : json.dumps(matched_face)
                }
                print("session yeniden oluşturuldu")
                print('New Token: ', token)
        
            mydb.commit()
            mydb.close()
            
            # Kullanılan kaynakları serbest bırak
            # cap.release()
            cv2.destroyAllWindows()
            return redirect(url_for('loginFaceid_messages.login_success_faceid'))"""


        # Kontrol: Eşleşen yüz yok.
        if sayac == 0:
        # else: 

            print('Unknown face')
            mydb.close()
            
            # Kullanılan kaynakları serbest bırak
            # cap.release()
            cv2.destroyAllWindows()  
            return redirect(url_for('loginFaceid_messages.loginFaceid_error_unknown_face'))
    