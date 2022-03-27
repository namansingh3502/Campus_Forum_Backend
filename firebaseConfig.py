import pyrebase

config = {
  "apiKey": "AIzaSyAVtLAwxP1GoVjE-ceIvnwAzDU60yBQd8E",
  "authDomain": "forum-image-storage.firebaseapp.com",
  "storageBucket": "forum-image-storage.appspot.com",
  "messagingSenderId": "953034613348",
  "appId": "1:953034613348:web:2b1034598336bd17d43571",
  "measurementId": "G-LZHLJRL8S3",
  "databaseURL": ""
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
