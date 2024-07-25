from bs4 import BeautifulSoup

faq_names =['Recharge & SIM', 'Forfaits mobiles', 'Offres Internet', 'Programme Fidélité', 'Services ', 'Urgences']
faq_paths = ["html/view-page-source.com-inwi.ma_faq_recharge-sim.html","html/view-page-source.com-inwi.ma_faq_offres-internet.html","html/view-page-source.com-inwi.ma_faq_programme-fidelite.html","html/view-page-source.com-inwi.ma_faq_recharge-siminwi.ma_faq_forfaits-mobiles.html","html/view-page-source.com-inwi.ma_faq_services.html","html/view-page-source.com-inwi.ma_faq_urgences.html" ]

def extract_text_with_links(tag):
    parts = []
    for elem in tag.recursiveChildGenerator():
        if isinstance(elem, str):
            parts.append(elem.strip())
        elif elem.name == 'a':
            href = elem.get('href', '')
            parts.append(f"{elem.get_text(strip=True)} ({href})")
    return ' '.join(parts).strip()

def main():
    for faq_name, faq_path in zip(faq_names, faq_paths):
        with open(faq_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        soup = BeautifulSoup(html_content, 'lxml')
        blocks = soup.find_all("div", class_="MuiGrid-root MuiGrid-container mui-131nyov")
        
        txt_output_path = f"files\{faq_name.replace(' ', '_')}.txt"
        with open(txt_output_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(f"# {faq_name}\n\n")
            
            for block in blocks:
                # Block title
                block_title = block.find("h3").text.strip()
                txt_file.write(f"## {block_title}\n")
                
                questions = block.find_all(class_="MuiPaper-root")
                for question in questions:
                    # Question
                    question_text = question.find("h4").text.replace('\u202f', '').strip()
                    txt_file.write(f"Q: {question_text}\n")
                    
                    # Answer
                    question_answer = extract_text_with_links(question.find(id="panel1bh-content"))
                    txt_file.write(f"A: {question_answer}\n\n")
        
        print(f"Saved {txt_output_path}")

if __name__ == "__main__":
    main()