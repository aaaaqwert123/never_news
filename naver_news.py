#필요한 라이브러리들
import requests
from bs4 import BeautifulSoup
import tkinter as tk
import pandas as pd
from datetime import datetime

now = datetime.now()  # 현재 날짜 및 시간 정보 가져오기
now_str = str(now)  # 날짜 및 시간 정보를 문자열로 변환

year = str(now.year)  # 연도를 문자열로 변환
month = str(now.month)  # 월을 문자열로 변환
day = str(now.day)  # 일을 문자열로 변환

def crawl_news():
    keywords = entry.get().split(',') #입력값 받는중
    start_date = start_date_entry.get()#입력값 받는중
    end_date = end_date_entry.get()#입력값 받는중
    number = int(article_count_entry.get())#입력값 받는중
    search_results = []

    for key in keywords:#반복문키워드를 전부다 할때까지 반복
        count = 0 #10개를 세줄 카운트
        page = 1 #네이버기사의 페이지를 의미함 1페이지의 10개가 있다
        while count < number: #넘버는 내가 몇개의 기사만 볼껀지 표시하는건데 카운트는 기사를 의미하므로 둘이 같아지면 반복문 종료
            response = requests.get(f"https://search.naver.com/search.naver?where=news&query={key}&sort=0&photo=0&page={page}&field=0&pd=3&ds={start_date}&de={end_date}&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:from{start_date}to{end_date},a:all&start={(page - 1) * 10 + 1}")
            #링크를 response에 저장
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            news_items = soup.find_all("div", class_="news_area")   

            for item in news_items: # 반복한다언제까지? 기사를 전~부 읽어올때까지
                if count >= number: #이때만약 카운트가 넘버보다 같거나 커졌다면? 더이상 기사를 가져오면 안되므로 종료시킨다
                    break

                title_element = item.find("a", class_="news_tit") #html태그중 a를 찾는다
                if not title_element: #만약에 none이라면 건너뛰어라
                    continue
                title = title_element.get_text(strip=True) #트루는 앞뒤를 제거하는데 쓰인다 가져온텍스트에
                url = title_element["href"] #거기에 있는 링크를 url에 넣는다

                date_element = item.find("span", class_="info")#span에 info인걸 찾는다
                if date_element:
                    date = date_element.get_text(strip=True).split()[0]  # 기사 날짜 추출

                    search_results.append({"Keyword": key, "Title": title, "URL": url, "Date": date})#저장한다 
                    count += 1 #카운트를 1해서 기사 하나를 저장햇다고 알린다

            page += 1
    #엑셀 작성코드
    file_name = file_name_entry.get()
    file_path = f"C:\\도제\\test\\1129\\엑셀모음\\{file_name}.xlsx"
    df = pd.DataFrame(search_results)
    df.to_excel(file_path, index=False)
    result_label.config(text=f"검색 결과가 '{file_path}' 파일로 저장되었습니다.")
#이 밑은 import pandas as pd 라이브러리를 쓰는것이다
root = tk.Tk()
root.title("네이버 뉴스 검색")
# 검색어 입력
entry_label = tk.Label(root, text="검색어를 입력하세요(여러 개일 경우 쉼표(,)로 구분):")
entry_label.pack()
entry = tk.Entry(root)
entry.pack()

# 시작 날짜 입력
start_date_label = tk.Label(root, text="시작할 날짜를 입력하세요 (YYYYMMDD 형식):")
start_date_label.pack()
start_date_entry = tk.Entry(root)
start_date_entry.pack()

# 종료 날짜 입력
end_date_label = tk.Label(root, text="종료할 날짜를 입력하세요 (YYYYMMDD 형식):")
end_date_label.pack()
end_date_entry = tk.Entry(root)
current_date = year+month+day
end_date_entry.insert(0, current_date)
end_date_entry.pack() 
print(current_date)

# 기사 갯수 입력
article_count_label = tk.Label(root, text="기사 갯수를 입력해주세요:")
article_count_label.pack()
article_count_entry = tk.Entry(root)
article_count_entry.pack()
article_count_entry.insert(0, '20')  # 기본 값으로 20 입력

# 파일 이름 입력
file_name_label = tk.Label(root, text="파일 이름을 입력하세요:")
file_name_label.pack()
file_name_entry = tk.Entry(root)
file_name_entry.pack()

# 검색 버튼
search_button = tk.Button(root, text="검색", command=crawl_news)
search_button.pack()

# 결과 표시 라벨
result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()