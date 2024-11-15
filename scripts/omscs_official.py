import requests
from bs4 import BeautifulSoup
import json


if __name__ == '__main__':
    url = "https://omscs.gatech.edu/current-courses"
    response = requests.get(url)

    data_path = "../data/omscs/courses"

    if response.status_code == 200:
        # print(response.text)
        # with open('oms_central.html', 'w') as f:
        #     f.write(response.text)

        soup = BeautifulSoup(response.text, 'html.parser')

        # a_tags = *soup.find_all('a', href=True, attrs={
        #     "data-entity-type": True,
        #     "data-entity-substitution": True
        #     }), sep='\n'
        
        # hrefs = [a['href'] for a in a_tags if a['href'] != '/degree-requirements']

        # for href in hrefs:

        h4_tag = soup.find('h4', string="Current & Ongoing OMS Courses")

        if h4_tag:
            course_ul = h4_tag.find_next_siblings('ul')
            
            if course_ul:

                # * : Foundational course
                # A : Course administered by OMS-Analytics program (still open to OMSCS students)
                # C : Course administered by OMS-Cybersecurity program (still open to OMSCS students)
                for li in course_ul[0].find_all('li'):

                    if a := li.find('a', href=True):

                        href = a['href']

                        course_data = {
                            'course-name': href.lstrip('/'),
                            'foundational': li.text.strip()[0] == '*',
                            'admin': 'CS'
                        }
                            
                        if sup := li.find('sup'):
                            course_data['admin'] = sup.text.strip()

                    response = requests.get(f"https://omscs.gatech.edu{href}")

                    soup = BeautifulSoup(response.text, 'html.parser')
                    # div_tag = soup.find('div', class_="field field--name-field-multi-body field--type-text-with-summary field--label-hidden field__item")
                    
                    # print(f"https://omscs.gatech.edu{href}")
                    # if div_tag:
                    #     # print(href)
                    #     with open(f'../data/oms-official/{href}.txt', 'w') as f:
                    #         for child in list(div_tag.children):
                    #             if child.text.strip():
                    #                 f.write(child.text + "\n")
                    print(href)
                    for header in soup.find_all(['h4', 'h5']):  # all subtitles are h4 and h5

                        # extract all the following <p> texts
                        p_tag = header.find_next_sibling()
                        while p_tag is not None and p_tag.name == 'p': 
                            # print(header.get_text(strip=True))
                            course_data[header.get_text(strip=True)] = p_tag.get_text(strip=True)
                            p_tag = p_tag.find_next_sibling()
                        
                        # if include any lists, added it into the extracted text
                        if p_tag is not None and p_tag.name == 'ul':
                            li_texts = "\n".join(f"- {li.get_text(strip=True)}" for li in p_tag.find_all('li'))

                            if header.get_text(strip=True) not in course_data:
                                course_data[header.get_text(strip=True)] = ""
                            course_data[header.get_text(strip=True)] += "\n" + li_texts
                    
                    with open(f'../data/oms-official/{href}.json', 'w') as f:
                        json.dump(course_data, f, ensure_ascii=False, indent=4)
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
