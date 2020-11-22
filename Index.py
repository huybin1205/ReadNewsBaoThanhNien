#import thư viện gTTS, nó được mô hình hóa từ Google speech
from gtts import gTTS
#import thư viện os để xử lý file
import os

f = open("content.txt","r",encoding="utf-8")
content = f.read()
print("Xin chờ! Chúng tôi đang xử lý...")
print("Có thể sẽ mất nhiều thời gian nếu nội dung dài!")
f.close()
#Xử lý
tts = gTTS(text=content, lang='vi')
#lưu file
tts.save("speech.mp3")
#mở file
os.startfile("speech.mp3")