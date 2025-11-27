from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.urls import path
import yfinance as yf

MOCK_STOCK_DATA = {
    'GOOG': { "symbol": "GOOG", "company": "Alphabet Inc.", "price": 175.45, "market_cap": "2.1 Trillion", "sector": "Technology", "summary": "Strong performance driven by cloud and advertising sectors." },
    'MSFT': { "symbol": "MSFT", "company": "Microsoft Corp.", "price": 410.12, "market_cap": "3.0 Trillion", "sector": "Technology", "summary": "Leading enterprise AI adoption and cloud computing services." },
    'AAPL': { "symbol": "AAPL", "company": "Apple Inc.", "price": 190.88, "market_cap": "2.9 Trillion", "sector": "Technology", "summary": "Record service revenue, steady but competitive hardware market." },
}


class StockReportView(APIView):
    """
    Handles GET requests for a specific stock report based on the ticker symbol.

    The frontend calls: /api/reports/<TICKER>/
    """

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
            subset_keys = {'currentPrice', 'marketCap', 'averageVolume', 'priceEpsCurrentYear', 'fiftyTwoWeekHigh', 'averageAnalystRating', 'dividendYield', 'fullExchangeName'}
            stock_report = dict((key, value) for key, value in report.items() if key in subset_keys)
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

