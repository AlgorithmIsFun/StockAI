from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.urls import path
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import re

class StockReportView(APIView):
    """
    Handles GET requests for a specific stock report based on the ticker symbol.

    The frontend calls: /api/reports/<TICKER>/
    """
    def clean_first_paragraph(self, text):
        clean_text = re.sub(r"\([^\)]*\)", "", text)
        clean_text = re.sub(r"\s+", " ", clean_text).strip()
        clean_text = re.sub(r"\[[^\]]*\]", " ", clean_text)
        clean_text = re.sub(r"([a-z])([A-Z])", r"\1 \2", clean_text)
        clean_text = re.sub(r"\s+", " ", clean_text).strip()
        return clean_text
    def parse_ceo_chair(self, text):
        """
        Extracts only CEO and Chair from a string like:
        "Tim Cook (CEO) Arthur Levinson (chairman)"
        Returns a dictionary: {"CEO": "...", "Chair": "..."}
        """
        result = {"CEO": "Unknown", "Chairman": "Unknown"}
        # Map possible role variants to desired keys
        role_map = {
            "ceo": "CEO",
            "chief executive officer": "CEO",
            "chair": "Chairman",
            "chairman": "Chairman",
            "chairwoman": "Chairman",
            "executive chairman": "Chairman"
        }
        # regex: captures "Name ( roles )"
        pattern = r"([A-Za-z .'-]+)\s*\(\s*([A-Za-z ,and]+)\s*\)"
        matches = re.findall(pattern, text)
        for name, roles_str in matches:
            # Split multiple roles by 'and' or ','
            roles = re.split(r',|and', roles_str)
            for role in roles:
                role_clean = role.strip().lower()
                if role_clean in role_map:
                    result[role_map[role_clean]] = name.strip()
        return result

    def extract_company_info(self, title):
        url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
        html = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }).text
        soup = BeautifulSoup(html, "html.parser")

        result = {}
        canonical = soup.find("link", {"rel": "canonical"})
        if not canonical:
            first_result = soup.select_one(".mw-search-result-heading a")
            if first_result and first_result.get("href"):
                url = "https://en.wikipedia.org" + first_result["href"]
                html = requests.get(url, headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                }).text
                soup = BeautifulSoup(html, "html.parser")

        # -----------------------------
        # 1. Extract FIRST MEANINGFUL PARAGRAPH
        # -----------------------------
        for p in soup.select("p"):
            text = p.get_text(strip=True)
            # skip empty paragraphs or coordinate-only paragraphs
            if text and len(text) > 50:
                result["first_paragraph"] = text
                break

        # -----------------------------
        # 2. Find INFOBOX (ANY variation)
        # -----------------------------
        infobox = soup.find("table", class_=lambda c: c and "infobox" in c)
        if not infobox:
            return result  # no infobox found

        # -----------------------------
        # 3. Extract all rows
        # -----------------------------
        for row in infobox.find_all("tr"):
            header = row.find("th")
            value = row.find("td")
            if not header or not value:
                continue

            field = header.get_text(strip=True).lower()

            # --- KEY PEOPLE ---
            if "key" in field and "people" in field:
                result["key_people"] = value.get_text(" ", strip=True)

            # --- HEADQUARTERS ---
            if "headquarters" in field:
                result["headquarters"] = value.get_text(" ", strip=True)

            if "industry" in field:
                result['industry'] = value.get_text(" ", strip=True)

            if "number of employees" in field:
                result["employees"] = value.get_text(" ", strip=True)

            # --- WEBSITE ---
            if "website" in field:
                link = value.find("a")
                if link:
                    result["website"] = link.get("href")
                else:
                    result["website"] = value.get_text(" ", strip=True)
        return result

    def get(self, request, ticker):
        # Normalize the ticker to match the keys in the data source
        ticker = ticker.upper()
        stock = yf.Ticker(ticker)
        # Simulate a 500 error if the frontend sends 'ERR'
        if ticker == 'ERR':
            # This simulates an unexpected server issue
            return Response(
                {"detail": "The financial data service is temporarily unavailable."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        # Look up the stock data
        report = stock.info
        current_price = report.get('regularMarketPrice')

        print(f"The current price for {ticker} is: ${current_price}")
        if report:
            subset_keys = {'currentPrice', 'marketCap', 'averageVolume', 'priceEpsCurrentYear', 'epsCurrentYear', 'debtToEquity', 'returnOnAssets', 'returnOnEquity', 'priceToBook', 'trailingPegRatio', 'fiftyTwoWeekHigh', 'averageAnalystRating', 'dividendYield', 'payoutRatio', 'fullExchangeName'}
            stock_report = dict((key, value) for key, value in report.items() if key in subset_keys)
            #stock_report = report
            info = self.extract_company_info(report.get('longName') or report.get("shortName"))
            info['first_paragraph'] = self.clean_first_paragraph(info['first_paragraph'])
            key_people = self.parse_ceo_chair(info["key_people"])
            del info["key_people"]
            stock_report.update(info)
            stock_report.update(key_people)
            # Return the report data with a 200 OK status
            return Response(stock_report, status=status.HTTP_200_OK)
        else:
            # Return a 404 Not Found status if the ticker is invalid
            return Response(
                {"detail": f"Stock ticker '{ticker}' not found."},
                status=status.HTTP_404_NOT_FOUND
            )

def reports_list(request):
    # Example static data for now
    reports = [
        {"id": 1, "title": "Sales Report", "status": "Complete"},
        {"id": 2, "title": "User Growth", "status": "Pending"},
        {"id": 3, "title": "Revenue Analysis", "status": "Complete"},
    ]
    return JsonResponse(reports, safe=False)

def users_list(request):
    try:
        # Return all users with id and username
        users = list(User.objects.values("id", "username", "email"))
        return JsonResponse(users, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def hello(request):
    return JsonResponse({"message": "Hello API is working!"})

