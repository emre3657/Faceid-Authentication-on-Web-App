from database import connectDatabase
from model import model
from flask import render_template, request, redirect, session, flash, url_for, Blueprint
import cv2
import face_recognition
import json
import numpy as np
import base64
import math


signupFaceid_control_bp = Blueprint('signupFaceid_control', __name__)

@signupFaceid_control_bp.route('/signupFaceid', methods=['POST', 'GET'])
def signupFaceid():

    if request.method == 'POST':
        if 'signup_data' in session:
            distanceThreshold = 0.45

            mycursor, mydb = connectDatabase()
            
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

            #img = cv2.resize(img, (0, 0), None, 0.25, 0.25) # Görüntüyü boyutlandır.
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # BGR to RGB çünkü: OpenCV BGR kullanır ama face_recognition RGB'İ kullanır.
            
            
            # Yüzü tespit et
            face_location = face_recognition.face_locations(img_rgb)


            # Birden fazla yüz var ise hata ver. HATA: Birden fazla yüz verisi girilemez.
            if len(face_location)>1:
                print("HATA: \nBirden fazla yüz algilanmasi")
                
                flash('Multiple faces detected!', 'error')
                flash('There should be only one face on the camera frame!', 'warning')

                img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)

                # Dikdörtgen çizmek için her yüz konumu üzerinde döngü yapın
                for (top, right, bottom, left) in face_location:
                    # Dikdörtgen çizme
                    box_face = cv2.rectangle(img_bgr, (left, top), (right, bottom), (0, 0, 255), 2)

                # image sol üst köşeye 'ERROR' yazdırma.
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img_bgr, 'ERROR', (10, 30), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
                
                # Görüntüyü Base64 formatına kodlayın
                _, buffer = cv2.imencode('.jpg', img_bgr)
                img_str = base64.b64encode(buffer).decode('utf-8')
                
                # return redirect(url_for('signupFaceid_error_multiple_faces'))--> bu route çalışmıyor.
                return render_template('faceid.html', img_str=img_str)

                
            
            # Yüz kodunu bul
            encodedface = face_recognition.face_encodings(img_rgb, face_location)

            
            if len(encodedface) == 1:

                results = model(img, stream=True, verbose=False)
                confidence = 0.7
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
                                print("Conf:", conf)
                                print("This object is real.")
                                
                                # Yüz kodlamasının bittiğini bildir
                                print("Yüz kodlamasi tamamlandi...")
                
                            else:
                                print("Conf:", conf)
                                print("This object is fake.")
                                img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)

                                # Dikdörtgen çizmek için her yüz konumu üzerinde döngü yapın
                                for (top, right, bottom, left) in face_location:
                                    # Dikdörtgen çizme
                                    box_face = cv2.rectangle(img_bgr, (left, top), (right, bottom), (0, 0, 255), 2)

                                # image sol üst köşeye 'ERROR' yazdırma.
                                font = cv2.FONT_HERSHEY_SIMPLEX
                                cv2.putText(img_bgr, 'ERROR', (10, 30), font, 1, (0, 0, 255), 2, cv2.LINE_AA)

                                # Kullanıcı adını görüntü üzerine yazdırma
                                cv2.putText(box_face, "FAKE", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                                
                                # Görüntüyü Base64 formatına kodlayın
                                _, buffer = cv2.imencode('.jpg', img_bgr)
                                img_str = base64.b64encode(buffer).decode('utf-8')
                            
                                flash('Fake face detected!', 'error')
                                return render_template('faceid.html', img_str=img_str)

            
            else:
                print("HATA: Yüz algilanamadi\nKameranin yüzünüzü gördüğünden emin olun!")
                flash('No face detected! Please try again', 'warning')

                img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
                
                # Sol üst köşeye Captured Face metnini eklemek için OpenCV'yi kullanarak görüntüyü işleyin
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img_bgr, 'ERROR', (10, 30), font, 1, (0, 0, 255), 2, cv2.LINE_AA)

                # Görüntüyü Base64 formatına kodlayın
                _, buffer = cv2.imencode('.jpg', img_bgr)
                img_str = base64.b64encode(buffer).decode('utf-8')
                
                # return redirect(url_for('signupFaceid_warning_no_face')) --> bu route çalışmıyor.
                return render_template('faceid.html', img_str=img_str)
            
            
            # Veri tabanından yüz verilerini alma."
            sql = "SELECT face_features FROM faceid"
            mycursor.execute(sql)
            yuz_oznitelik = mycursor.fetchall()

            # session'dan email verisini al
            email = session.get('signup_data', {}).get('email')

            yuz_oznitelik_sayac = 0
            for yuz in yuz_oznitelik:
                if yuz[0] != None:
                    yuz_oznitelik_sayac += 1

            
            # Veri tabanında hiçbir veri yok ise:
            if yuz_oznitelik_sayac == 0:

                # Yüz özniteliğini JSON formatına dönüştür
                yuz_oznitelik_json = json.dumps(encodedface[0].tolist())

                # Kullanıcı verilerini güncelle
                sql = "UPDATE faceid SET face_features = %s WHERE email = %s"
                val = (yuz_oznitelik_json, email)
                mycursor.execute(sql, val)

                # Veritabanındaki değişiklikleri kaydet
                mydb.commit()
                mydb.close()

                # session'da ki veriyi sil.
                session.pop('signup_data', None)
                

                print("Kullanici başarıyla faceid aldı")
                
                img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
                
                # Dikdörtgen çizmek için her yüz konumu üzerinde döngü yapın
                for (top, right, bottom, left) in face_location:
                    # Dikdörtgen çizme
                    box_face = cv2.rectangle(img_bgr, (left, top), (right, bottom), (0, 255, 0), 2)

                # Sol üst köşeye Captured Face metnini eklemek için OpenCV'yi kullanarak görüntüyü işleyin
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img_bgr, 'Captured Face', (10, 30), font, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

                flash('Face ID have gotten successfully!', 'success')
                # flash('Registration completed! You can exit now', 'info')
                
                # Görüntüyü Base64 formatına kodlayın
                _, buffer = cv2.imencode('.jpg', img_bgr)
                img_str = base64.b64encode(buffer).decode('utf-8')

            
                return render_template('faceid.html', img_str =img_str)
                # return redirect(url_for('signup_success_faceid')) ---> işe yaramadı.
            
            # else durumu veri tabanında yüz öznitelik verisi var ise: yuz_oznitelik_sayac > 0
            else :
                
                sayac = 0
                
                yuz = None
                
                # Veri tabanında ki yüz verileri  ile kameradan gelen yüz arasında distance hesabı yapma.
                for veri in yuz_oznitelik:
                    
                    
                    if veri[0] is not None:  # veri[0] None değilse devam et
                    
                        # json str veri tipi okur. str veri yapısı içinde tuple'lar mevcuttur.
                        # Tuple veriyi ayıklamamız lazım. json.load(veri[0]) verinin(tuple'nin) ilk elemanını listeye dönüştürür.
                        veri = (json.loads(veri[0]))

                        # Distance hesabı. Liste olan yüz verisini işlemeden önce np arrayine dönüştürüyoruz.
                        # Çünkü kıyaslama yapılırken iki veride aynı tipte olması gerekir.
                        faceDis = face_recognition.face_distance(encodedface, np.array(veri))
                        faceDis = round(faceDis[0], 4)
                        

                        if faceDis < distanceThreshold:

                            # sayacı bir(1) artır.
                            sayac +=1

                            # yuz verisini değiştir
                            if yuz == None:
                                yuz = veri
                            
                            # Face distance'ı göster.
                            
                            print(f"faceDistance: {faceDis}")
                            if sayac == 1:
                                break
                    

                if sayac == 0:
                    
                    # Yüz özniteliğini JSON formatına dönüştür
                    yuz_oznitelik_json = json.dumps(encodedface[0].tolist())

                    # Kullanıcı verilerini güncelle
                    sql = "UPDATE faceid SET face_features = %s WHERE email = %s"
                    val = (yuz_oznitelik_json, email)
                    mycursor.execute(sql, val)
                    
                    # Veritabanındaki değişiklikleri kaydet
                    mydb.commit()

                    mydb.close()

                    # session'da ki verileri sil.
                    session.pop('signup_data', None)

                    print("Kullanici başariyla face id aldı.")
                    #return redirect(url_for('signup_success_faceid'))

                    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
                    
                    # Dikdörtgen çizmek için her yüz konumu üzerinde döngü yapın
                    for (top, right, bottom, left) in face_location:
                        # Dikdörtgen çizme
                        box_face = cv2.rectangle(img_bgr, (left, top), (right, bottom), (0, 255, 0), 2)
                    
                    # Sol üst köşeye Captured Face metnini eklemek için OpenCV'yi kullanarak görüntüyü işleyin
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(img_bgr, 'Captured Face', (10, 30), font, 0.8, (255, 255, 255), 2, cv2.LINE_AA)


                    flash('Face ID have gotten successfully!', 'success')
                    # flash('Registration completed! You can exit now', 'info')
                    
                    # Görüntüyü Base64 formatına kodlayın
                    _, buffer = cv2.imencode('.jpg', img_bgr)
                    img_str = base64.b64encode(buffer).decode('utf-8')
                    
                    return render_template('faceid.html', img_str=img_str)
                    
                
                else: # if sayac != 0:
            
                    print("Kayit Başarisiz...\nHATA: Kullanici zaten kayitli!")
                    # Veri tabanından bu yüze ait username verisini alma.w
                    sql = "SELECT username FROM faceid WHERE face_features = %s"
                    val = (json.dumps(yuz),)  # Placeholder'ı burada kullanmalısınız ve veri demetinin bir tuple olması gerekir
                    mycursor.execute(sql, val)
                    username = mycursor.fetchone()[0]  # Sorgu sonucunu al
                    mydb.close()

                    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
                    
                    # Dikdörtgen çizmek için her yüz konumu üzerinde döngü yapın
                    for (top, right, bottom, left) in face_location:
                        # Dikdörtgen çizme
                        box_face = cv2.rectangle(img_bgr, (left, top), (right, bottom), (0, 0, 255), 2)

                    # image sol üst köşeye 'ERROR' yazdırma.
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(img_bgr, 'ERROR', (10, 30), font, 1, (0, 0, 255), 2, cv2.LINE_AA)

                    # Kullanıcı adını görüntü üzerine yazdırma
                    cv2.putText(box_face, username.upper(), (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

                    # Görüntüyü Base64 formatına kodlayın
                    _, buffer = cv2.imencode('.jpg', img_bgr)
                    img_str = base64.b64encode(buffer).decode('utf-8')

                    
                    # return redirect(url_for('signup_error_faceid'))
                    flash('You already created an account with your face!', 'error')
                    flash('Cannot create multiple accounts with one face!', 'warning')
                    flash('Can exit and continue with email and password!', 'info')

                    return render_template('faceid.html', img_str=img_str)
        else:
            flash('Registration completed!', 'info')
            return redirect(url_for('pages.login_page'))
    else:
        return redirect(url_for('pages.signup_page'))
