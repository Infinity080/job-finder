from django.shortcuts import render
from .models import Website
from rest_framework.views import APIView
from rest_framework.response import Response
from .scraping.scraping_manager import ScrapingManager
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from job_finder_app.scraping.scraping_manager import ScrapingManager
from job_finder_app.cv.cv_utils import get_best_specializations_from_cv, get_experience_level
import fitz  # PyMuPDF

def websites_list(request):
    websites = Website.objects.all()
    return render(request, 'job_finder_app/websites_list.html', {'websites': websites})

class JobLinkView(APIView):
    def get(self, request):
        specializations = request.query_params.getlist("specialization")
        exp_level = request.query_params.get("exp_level")

        if not specializations or not exp_level:
            return Response("error")
        
        scraping_manager = ScrapingManager()
        links = scraping_manager.get_jobs_by_specialization(specializations, exp_level)

        return Response({"links": links}, status=status.HTTP_200_OK)

class SpecsView(APIView):
    def get(self, request):
        scraping_manager = ScrapingManager()
        specs = scraping_manager.get_all_specializations()
        return Response(specs)

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

class UploadCVView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        cv_file = request.FILES.get("cv")
        if not cv_file:
            return Response({"error": "No CV file uploaded."}, status=400)

        try:
            cv_text = extract_text_from_pdf(cv_file)
        except Exception as e:
            return Response({"error": f"Failed to read PDF: {str(e)}"}, status=400)

        top_specs = get_best_specializations_from_cv(cv_text)
        exp_level = get_experience_level(cv_text)

        return Response({
            "cv_summary": cv_text[:300],
            "predicted_specializations": top_specs,
            "predicted_experience_level": exp_level
        })

