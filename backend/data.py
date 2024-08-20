import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json
import random
import time

# Cập nhật danh sách các chủ đề
topics = {
    # "Kinh doanh": [
    #     "https://vnexpress.net/kinh-doanh/quoc-te",
    #     "https://dantri.com.vn/kinh-doanh.htm",
    #     "https://vneconomy.vn/tai-chinh.htm",
    #     "https://doanhnhansaigon.vn/kinh-doanh",
    #     "https://thanhnien.vn/kinh-te.htm",
    #     "https://vietnamnet.vn/kinh-doanh",
    #     "https://thoibaotaichinhvietnam.vn/kinh-doanh",
    #     "https://baomoi.com/kinh-doanh.epi",
    # ],
    # "Thể thao": [
    #     "https://vnexpress.net/the-thao",
    #     "https://www.24h.com.vn/the-thao-c101.html",
    #     "https://thethao247.vn/",
    #     "https://bongdaplus.vn/the-thao.html"
    # ],
    # "Giải trí": [
    #     "https://znews.vn/giai-tri.html",
    #     "https://vnexpress.net/giai-tri",
    #     "https://2sao.vn/",
    #     "https://vietnamnet.vn/giai-tri",
    #     "https://dantri.com.vn/giai-tri.htm",
    #     "https://laodong.vn/giai-tri.htm",
    #     "https://soha.vn/giai-tri.htm",
    #     "https://thanhnien.vn/giai-tri.htm",
    #     "https://baomoi.com/giai-tri.epi",
    #     "https://tuoitre.vn/giai-tri.htm",
    #     "https://www.24h.com.vn/giai-tri-c731.html"
    # ],
    "Công nghệ": [
        "https://www.techz.vn/",
        "https://genk.vn/",
        "https://vnexpress.net/so-hoa/cong-nghe",
        "https://vietnamnet.vn/thong-tin-truyen-thong/cong-nghe",
        "https://ictnews.vietnamnet.vn/cong-nghe.htm",
        "https://vnreview.vn/tin-tuc-cong-nghe",
        "https://tuoitre.vn/cong-nghe.htm",
        "https://thanhnien.vn/cong-nghe.htm",
        "https://vtcnews.vn/khoa-hoc-cong-nghe-82.html",
        "https://congan.com.vn/cong-nghe"

    ],
    "Sức khỏe": [
        "https://vnexpress.net/suc-khoe",
        "https://suckhoedoisong.vn/",
        "https://tuoitre.vn/suc-khoe.htm",
        "https://vietnamnet.vn/suc-khoe",
        "https://dantri.com.vn/suc-khoe.htm",
        "https://laodong.vn/suc-khoe.htm",
        "https://alobacsi.com/",
        "https://thanhnien.vn/suc-khoe.htm",
        "https://www.24h.com.vn/suc-khoe-doi-song-c62.html",
        "https://vtcnews.vn/suc-khoe-35.html"

    ],
    "Giáo dục": [
        "https://vnexpress.net/giao-duc",
        "https://giaoducthoidai.vn/giao-duc/",
        "https://tuoitre.vn/giao-duc.htm",
        "https://zingnews.vn/giao-duc.html",
        "https://giaoduc.net.vn/",
        "https://thanhnien.vn/giao-duc.htm",
        "https://baomoi.com/giao-duc.epi",
        "https://vietnamnet.vn/giao-duc"

    ],
    "Du lịch": [
        "https://vnexpress.net/du-lich",
        "https://dulichviet.net.vn/",
        "https://thanhnien.vn/du-lich.html",
        "https://vietnamnet.vn/du-lich",
        "https://zingnews.vn/du-lich.html",
        "https://tuoitre.vn/du-lich.htm",
        "https://tcdulichtphcm.vn/",
        "https://baomoi.com/du-lich.epi"
    ],
    "Khoa học": [
        "https://vnexpress.net/khoa-hoc",
        "https://khoahocphattrien.vn/",
        "https://vietnamnet.vn/giao-duc/khoa-hoc",
        "https://bongdaplus.vn/khoa-hoc.html",
        "https://tintuc.vn/khoa-hoc-cong-nghe.html"
    ],
    "Bất động sản": [
        "https://vnexpress.net/bat-dong-san",
        "https://vietnamnet.vn/bat-dong-san"
    ]
}


ua = UserAgent()

def get_content(url, seen_urls):
    if url in seen_urls:
        return None
    seen_urls.add(url)
    
    headers = {'User-Agent': ua.random}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Loại bỏ các thẻ script, style, header, footer, nav, aside
        for script in soup(["script", "style", "header", "footer", "nav", "aside"]):
            script.decompose()
        
        # Loại bỏ các thẻ có class hoặc id chứa từ khóa liên quan đến quảng cáo, bình luận
        for element in soup.find_all(class_=lambda value: value and ("ad" in value or "banner" in value or "comment" in value)):
            element.decompose()
        
        # Lấy nội dung từ thẻ h1 và thẻ p
        h1_content = soup.find_all('h1')
        p_content = soup.find_all('p')
        
        # Lấy nội dung văn bản từ phần nội dung chính (có thể điều chỉnh cho từng trang)
        main_content = soup.find('article') or soup.find('div', class_='content') or soup.find('div', id='main-content')
        
        # Sử dụng một tập hợp để theo dõi nội dung đã lấy, tránh lặp lại
        seen_texts = set()
        content = []
        
        # Thêm nội dung từ thẻ h1 và p
        for h1 in h1_content:
            text = h1.get_text().strip()
            if text:
                if text not in seen_texts:
                    content.append(text)
                    seen_texts.add(text)
        for p in p_content:
            text = p.get_text().strip()
            if text:
                if text not in seen_texts:
                    content.append(text)
                    seen_texts.add(text)
        
        # Thêm nội dung từ phần tử chính
        if main_content:
            text = main_content.get_text().strip()
            if text:
                if text not in seen_texts:
                    content.append(text)
                    seen_texts.add(text)
        
        # Kết hợp tất cả nội dung vào một chuỗi
        text = '\n'.join(content)
        
        # Xử lý văn bản: loại bỏ khoảng trắng thừa và dòng trống
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        print(f"Error: {e}")
        return None

max_articles_per_topic = 150  # Cập nhật số lượng bài báo tối đa
seen_urls = set()

for topic, urls in topics.items():
    documents = []
    topic_count = 0
    
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        links = soup.find_all('a', href=True)
        
        for link in links:
            if len(documents) >= max_articles_per_topic:
                break
            
            href = link['href']
            if href.startswith('http') and (href.endswith('.html') or href.endswith('.htm') or href.endswith('.gd')):
                content = get_content(href, seen_urls)
                if content:
                    documents.append({
                        "content": content,
                        "topic": topic,
                        "url": href
                    })
                    topic_count += 1
                    print(f"Đã thu thập {len(documents)} bài báo cho chủ đề '{topic}'")
                    
                    time.sleep(random.uniform(1, 3))
        
        if len(documents) >= max_articles_per_topic:
            break
    
    # Lưu các bài báo vào tệp JSON tương ứng với từng chủ đề
    with open(f'documents_{topic}.json', 'w', encoding='utf-8') as f:
        json.dump(documents, f, ensure_ascii=False, indent=4)

    print(f"Đã thu thập và lưu {len(documents)} bài báo vào documents_{topic}.json")
