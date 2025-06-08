# main.py와 같은 폴더 또는 임의 위치에 다음 스크립트 저장 후 실행
import shutil
import os

# 현재 파일 기준 static/images 경로 계산
base_dir = os.path.abspath(os.path.dirname(__file__))
target_dir = os.path.join(base_dir, 'templates')
os.makedirs(target_dir, exist_ok=True)

# 복사할 경로 설정
source_paths = {
    "image1.png": r"C:\Users\user\PycharmProjects\pythonProject1\venv\Lib\site-packages\pip\templates\image1.png",
    "image2.png": r"C:\Users\user\PycharmProjects\pythonProject1\venv\Lib\site-packages\pip\templates\image2.png",
    "image3.png": r"C:\Users\user\PycharmProjects\pythonProject1\venv\Lib\site-packages\pip\templates\image3.png",
    "image4.png": r"C:\Users\user\PycharmProjects\pythonProject1\venv\Lib\site-packages\pip\templates\image4.png",
    "image5.png": r"C:\Users\user\PycharmProjects\pythonProject1\venv\Lib\site-packages\pip\templates\image6.png",
    "image6.png": r"C:\Users\user\PycharmProjects\pythonProject1\venv\Lib\site-packages\pip\templates\image6.png",
    "image7.png": r"C:\Users\user\PycharmProjects\pythonProject1\venv\Lib\site-packages\pip\templates\image7.png",
    "image8.png": r"C:\Users\user\PycharmProjects\pythonProject1\venv\Lib\site-packages\pip\templates\image8.png"
}

# 이미지 복사
for filename, source_path in source_paths.items():
    dest_path = os.path.join(target_dir, filename)
    try:
        shutil.copy2(source_path, dest_path)
        print(f"{filename} 복사 완료")
    except Exception as e:
        print(f"{filename} 복사 실패: {e}")



