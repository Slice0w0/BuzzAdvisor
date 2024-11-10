import requests
from bs4 import BeautifulSoup
import json


if __name__ == '__main__':
    url = "https://www.omscentral.com/"
    response = requests.get(url)

        
    if response.status_code == 200:
        # print(response.text)
        # with open('oms_central.html', 'w') as f:
        #     f.write(response.text)

        soup = BeautifulSoup(response.text, 'html.parser')
        
        script_tag = soup.find('script', id="__NEXT_DATA__")
        if script_tag:
            json_data = json.loads(script_tag.string)
            
            with open("next_data.json", "w") as json_file:
                json.dump(json_data, json_file, indent=4)
            
            course_info = json_data['props']['pageProps']['courses']
            slugs = [course['slug'] for course in course_info]
            codes = [course['codes'][0] for course in course_info]

            for slug, code in zip(slugs, codes):
                response = requests.get(f"{url}courses/{slug}/reviews")

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    script_tag = soup.find('script', id="__NEXT_DATA__")

                    if script_tag:
                        json_data = json.loads(script_tag.string)

                    with open(f"data/oms-central/review/{code}.json", "w") as json_file:
                        json.dump(json_data, json_file, indent=4)

                    print(f"finish {url}courses/{slug}/reviews")
                
                else:
                    print(f"{url}courses/{slug}/reviews")
        else:
            print("Script tag with id '__NEXT_DATA__' not found.")
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
