from sentence_transformers import SentenceTransformer, util
from job_finder_app.models import Specialization
import re

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_specializations():
    return list(Specialization.objects.values('website__name', 'name').distinct())

def get_best_specializations_from_cv(cv_text: str, top_k: int = 2):
    specs = get_specializations()
    if not specs:
        return {}

    cv_text_lower = cv_text.lower()
    exact_matches = set()

    spec_names = [spec['name'] for spec in specs]

    for spec_name in spec_names:
        pattern = r'(?<!\w)' + re.escape(spec_name.lower()) + r'(?!\w)'
        if re.search(pattern, cv_text_lower):
            exact_matches.add(spec_name)

    spec_embeddings = model.encode(spec_names, convert_to_tensor=True)
    cv_embedding = model.encode(cv_text, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(cv_embedding, spec_embeddings)[0]

    website_scores = {}

    for i, spec in enumerate(specs):
        score = 1.0 if spec['name'] in exact_matches else float(similarities[i])
        website = spec['website__name']
        if website not in website_scores:
            website_scores[website] = []
        website_scores[website].append((spec['name'], score))

    for website in website_scores:
        website_scores[website].sort(key=lambda x: x[1], reverse=True)
        website_scores[website] = website_scores[website][:top_k]

    return website_scores



def get_experience_level(cv_text):
    text = cv_text.lower()
    year_matches = re.findall(r'(\d+)\s*\+?\s*(?:years|yrs)', text)
    total_years = sum(int(match) for match in year_matches)

    if total_years >= 5:
        return 'senior'
    elif total_years >= 2:
        return 'mid'
    
    if 'senior' in text:
        return 'senior'
    elif 'mid' in text or 'middle' in text:
        return 'mid'
    elif 'junior' in text:
        return 'junior'
    else:
        return 'junior'


