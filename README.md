This project is based on a web application. it was written python programming language. Flask (python framework) and many libraries were used to run it.
As a standard, username or email and password is used to log in a website. 
In addition to the standard login system, 'faceid authentication system' is used to log in a website in this project.
User's faces taken and coded. Coded faces are kept as json type in the database (MySQL).
A face is captured using a webcam. The face is compared with faces in the database.  If the system finds a face that matches a certain percentage, it allows login. 
This system is worked very well with few users.
Also, system has a model. This model cathes fake faces. Thus, spoofing attacks is not allowed. However, this model is not worked 100 pertange accurate. So it must be improved. 
Used model is improved with machine learning. With YOLO model, about 5000 fake and 5000 real images are trained in Google Colaboratory.
MySQL used as a database. It has only one table. Because only faces are controlled for login process.

*** Required Tools *** 
 1 - Vs Code 
 2 - MySQL (You do not need to install it if you use internal database. Like Flask-SQLAlchemy in Flask)
 3 - Ptyhon 3.11.x
Not: Also, you must be install Visual Studio 2022 with C, C++ desktop application extension. Because dlib module needs some extensions to run wheel packages. It is complicated.



That's all.
Thank you, keep coding!
