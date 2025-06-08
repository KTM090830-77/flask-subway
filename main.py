import os
from email.policy import default

from flask import Flask, render_template, request, jsonify
import requests
import xml.etree.ElementTree as ET
import time

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'))

API_URLS = [
    "http://openapi.seoul.go.kr:8088/50465556696b746d38394c4548506e/json/SeoulMetroFaciInfo/1/1000/",
    "http://openapi.seoul.go.kr:8088/50465556696b746d38394c4548506e/json/SeoulMetroFaciInfo/1001/2000/",
    "http://openapi.seoul.go.kr:8088/50465556696b746d38394c4548506e/json/SeoulMetroFaciInfo/2001/2822/"
]

station_map = {
    "판암(대전대)": 101, "신흥": 102, "대동(우송대)": 103, "대전": 104,
    "중앙로": 105, "중구청": 106, "서대전네거리": 107, "오룡": 108,
    "용문": 109, "탄방": 110, "시청": 111, "정부청사(신협중앙회)": 112,
    "갈마": 113, "월평(한국과학기술원)": 114, "갑천": 115,
    "유성온천(충남대·목원대)": 116, "구암": 117, "현충원(한밭대)": 118,
    "월드컵경기장(노은도매시장)": 119, "노은": 120, "지족(침신대)": 121, "반석(칠성대)": 122
}

def fetch_facility_data():
    data = []
    for url in API_URLS:
        response = requests.get(url)
        if response.status_code == 200:
            try:
                json_data = response.json()
                if 'SeoulMetroFaciInfo' in json_data:
                    data.extend(json_data['SeoulMetroFaciInfo']['row'])
            except requests.exceptions.JSONDecodeError:
                pass
    return data

@app.route('/', methods=['GET', 'POST'])
def index():
    mode = 'seoul'
    search_term = ''
    results = []

    if request.method == 'POST':
        mode = request.form.get('mode', 'seoul')
        search_term = request.form.get('station', '').strip()

        if mode == 'seoul':
            facility_data = fetch_facility_data()
            station_list1 = ["종각", "종로5가", "제기동"]
            station_list2 = ["을지로입구", "상왕십리", "한양대", "뚝섬", "성수", "구의", "강변", "잠실나루", "잠실새내", "삼성", "역삼", "서초", "방배",
                             "신림", "신대방", "문래", "신촌", "이대", "아현", "용답", "신정내거리", "양천구청", "도림천", "용두"]
            station_list3 = ["지축", "구파발", "녹번", "홍제,", "무악재", "독립문", "경복궁", "안국", "동대입구", "금호", "압구정", "신사", "잠원", "매봉",
                             "대치", "학여울", "대청", "일원", "경찰병원"]
            station_list4 = ["불암산", "상계", "쌍문", "수유", "미아", "미아사거리", "길음", "혜화", "명동", "숙대입구", "신용산", "남태령"]
            station_list5 = ["방화", "개화산", "송정", "마곡", "발산", "우장산", "화곡", "신정", "목동", "오목교", "여의나루", "마포", "애오개", "서대문",
                             "광화문", "신금호", "행당", "마장", "답십리", "장한평", "아차산", "광나루", "강동", "굽은다리", "길동", "명일", "고덕",
                             "상일동", "둔촌동", "방이", "개롱", "거여", "거여", "마천", "강일", "미사", "하남풍산", "하남시청", "하남검단산"]
            station_list6 = ["응암", "역촌", "독바위", "구산", "새절", "증산", "월드컵경기장", "마포구청", "망원", "상수", "광흥창", "대흥", "녹사평",
                             "이태원", "한강진", "버티고개", "창신", "안암", "고려대", "월곡", "상월곡", "골곶이", "화랑대", "봉화산"]
            station_list7 = ['수락산', '마들', '중계', '하계', '공릉', '먹골', '중화', '면목', '사가정', '중곡', '용마산', '어린이대공원',
                             '자양(뚝섬한강공원)', '청담', '학동', '논현', '반포', '내방', '남성', '숭실대입구', '상도', '장승배기', '신대방삼거리', '보라매',
                             '신풍', '남구로', '철상', '천왕', '광명사거리']
            
            line_mapping = {"(1)": 1, "(2)": 2, "(3)": 3, "(4)": 4, "(5)": 5, "(6)": 6, "(7)": 7, "(8)": 8, "(9)": 9}
            line_colors = {
                1: "#0052A4", 2: "#00A84D", 3: "#EF7C1C", 4: "#00A5DE",
                5: "#996CAC", 6: "#CD7C2F", 7: "#747F00", 8: "#E6186C", 9: "#BDB092",
            }
            floor_mapping = {"B6": -3, "B5": -2, "BM4": -1.5, "B4": -1, "BM3": -0.5, "B3": 0, "BM2": 0.5, "B2": 1, "B1": 2,
                             "1F": 3, "F1": 3,"M1": 3.5 ,"F2": 4, "F3": 5, "M": 2.5, "지상": 3, "BM1": 1.5}

            for item in facility_data:
                station_full_name = item.get('STN_NM', '')
                if search_term in station_full_name:
                    use_status = item.get('USE_YN', '사용가능')
                    status_colors = {
                        "사용가능": "#599468",
                        "보수중": "#FF7F00",
                        "공사중": "#9B111B"
                    }
                    status_color = status_colors.get(use_status, "#000000")

                    found_line = None
                    line_color = None
                    image_path = None
                    for line_key, line_number in line_mapping.items():
                        if line_key in station_full_name:
                            found_line = line_number
                            line_color = line_colors.get(line_number, "#000000")
                            image_path = f"images/line_{line_number}.png"
                            break
                    if not found_line:
                        if station_full_name in station_list1:
                            found_line = 1
                            line_color = line_colors.get(line_number, "#0052A4")
                            image_path = f"images/line_1.png"
                        elif station_full_name in station_list2:
                            found_line = 2
                            line_color = line_colors.get(line_number, "#0052A4")
                            image_path = f"images/line_2.png"
                        elif station_full_name in station_list3:
                            found_line = 3
                            line_color = line_colors.get(line_number, "#EF7C1C")
                            image_path = f"images/line_3.png"
                        elif station_full_name in station_list4:
                            found_line = 4
                            line_color = line_colors.get(line_number, "#00A5DE")
                            image_path = f"images/line_4.png"
                        elif station_full_name in station_list5:
                            found_line = 5
                            line_color = line_colors.get(line_number, "#996CAC")
                            image_path = f"images/line_5.png"
                        elif station_full_name in station_list6:
                            found_line = 6
                            line_color = line_colors.get(line_number, "#CD7C2F")
                            image_path = f"images/line_6.png"
                        elif station_full_name in station_list7:
                            found_line = 7
                            line_color = line_colors.get(line_number, "#747F00")
                            image_path = f"images/line_7.png"
                        else:
                            found_line = 8
                            line_color = line_colors.get(line_number, "#E6186C")
                            image_path = f"images/line_8.png"
                    facility_type = "엘리베이터" if item.get('ELVTR_SE') == "EV" else "휠체어 리프트" if item.get('ELVTR_SE') == "WL" else "에스컬레이터"
                    floors = item.get('OPR_SEC', 'N/A')

                    direction = "양방향↔"
                    if facility_type in ["에스컬레이터", "휠체어 리프트"] and floors != 'N/A':
                        try:
                            floor_split = floors.split('-')
                            mapped_floors = [floor_mapping.get(floor.strip(), None) for floor in floor_split]
                            if None not in mapped_floors:
                                if len(mapped_floors) == 2:
                                    direction = "하행↓" if mapped_floors[0] > mapped_floors[1] else "상행↑"
                                elif len(mapped_floors) == 1:
                                    direction = "동일 층"
                        except Exception:
                            direction = "오류 발생"

                    results.append({
                        "station": station_full_name,
                        "color": line_color,
                        "image_path": image_path,
                        "type": facility_type,
                        "status": ("사용 가능" if use_status == "사용가능" else "보수 중" if use_status == "보수중" else "공사 중"),
                        "location": item.get('INSTL_PSTN', 'N/A'),
                        "floor": floors,
                        "direction": direction,
                        "status_color": status_color
                    })

        elif mode == 'daejeon':
            if search_term and search_term in station_map:
                station_code = station_map[search_term]
                today = time.strftime("%Y%m%d", time.localtime())
                url = "http://www.djtc.kr/OpenAPI/service/ElevatorInspectionPlanSVC/getInspectionPlan01"
                params = {
                    'serviceKey': 'njUBG9iduEaWuAWiaHIodpH%2Fpq4oho86WbjNIbulfbOQOF8qErnlWxB0WCtaFT3MKj1LU7LbqhJHloWK3MFO2A==',
                    'sDate': today,
                    'eDate': today
                }
                try:
                    response = requests.get(url, params=params)
                    root = ET.fromstring(response.content)

                    for item in root.iter('item'):
                        place = item.find('place')
                        if place is not None and int(place.text) == station_code:
                            results.append({
                                'station': search_term,
                                'place': item.find('place', default='N/A'),
                                'planDt': item.findtext('planDt', default='N/A'),
                                'type': '점검 계획',
                                'location': '-',
                                'floor': '-',
                                'direction': '-',
                                'status': '-',
                                'image_path': 'images/daejeon_icon.png'
                            })
                except Exception as e:
                    results = [{'error': str(e)}]

    return render_template('index.html', mode=mode, search_term=search_term, results=results, daejeon_stations=station_map)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
