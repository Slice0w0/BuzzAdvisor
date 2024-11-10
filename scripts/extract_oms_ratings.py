import json

if __name__ == '__main__':
    with open('../data/oms-central/oms-central.json', 'r') as f:
        data = json.load(f)

    courses = data['props']['pageProps']['courses']

    fields = ['name', 'description', 'syllabus', 'isFoundational', 'slug', 'codes', 'reviewCount', 'rating', 'difficulty', 'workload']
    relevant_info = [
        {
            field: course[field] for field in fields if field in course
        }
        for course in courses
    ]

    with open('data/oms-central/oms-central-processed.json', 'w') as f:
        json.dump(relevant_info, f)