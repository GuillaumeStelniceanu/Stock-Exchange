# 📈 Stock Exchange Analysis Toolkit

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Active](https://img.shields.io/badge/status-active-brightgreen.svg)]()

A comprehensive Python-based stock analysis, simulation, and investment strategy toolkit for both US and European markets. This project combines financial data analysis, technical indicators, portfolio optimization, and tax-efficient investment simulations (PEA vs CTO).

## 🚀 Features

### 📊 **Data Analysis & Visualization**
- **Multi-market support**: US (via Twelve Data API) and European (via Yahoo Finance) stocks
- **Interactive charts**: Candlestick charts with technical indicators (RSI, MACD, Bollinger Bands)
- **Technical indicators**: MA20, MA50, MA200, RSI, MACD, Bollinger Bands, Volume analysis
- **Dashboard generation**: Automated HTML reports with Plotly visualizations

### 💼 **Investment Simulation**
- **PEA vs CTO comparison**: French tax-advantaged accounts analysis
- **Monte Carlo simulations**: 1,000+ scenario analysis with risk assessment
- **Dollar-Cost Averaging (DCA)**: Regular investment strategy modeling
- **Portfolio optimization**: Asset allocation and rebalancing strategies

### 🖥️ **GUI Applications**
- **Advanced Stock Simulator**: Interactive Tkinter application with real-time data
- **Investment calculator**: Parameterized simulations with graphical outputs
- **Risk analysis tools**: Value at Risk (VaR), Sharpe ratio, loss probability calculations

### 📈 **Technical Analysis Tools**
- **Stock data fetching**: Historical price data from multiple sources
- **Indicator calculation**: Comprehensive technical analysis toolkit
- **Automated reporting**: CSV and Excel export capabilities

## 📁 Project Structure

STOCK-EXCHANGE-ANALYSIS/  
├── Notebooks/ # Jupyter notebooks for analysis  
│ ├── outputs/ # Generated outputs from notebooks  
│ ├── 01_PEA_CTO_Basics.ipynb # Basic PEA vs CTO comparison  
│ ├── 02_PEA_CTO_DCA.ipynb # DCA strategy analysis  
│ ├── 03_Technical_Analysis.ipynb # Technical indicators tutorial  
│ ├── 04_Portfolio_Optimization.ipynb # Portfolio optimization  
│ ├── simulateur_PEA_CTO.ipynb # Interactive PEA/CTO simulator  
│ └── simulation1.ipynb # Sample simulations  
├── outputs/ # General output directory  
├── src/ # Source code  
│ ├── lancement_simulateur.py # Main launcher script  
│ ├── simulateur_actions_avance.py # Advanced GUI simulator (Monte Carlo)  
│ ├── simulateur_actions.py # Basic GUI simulator  
│ ├── simulation1.py # Simulation modules  
│ ├── simulation2.py  
│ ├── simulation3.py  
│ ├── simulation4.py  
│ └── stock_vizualiser.py # Stock data visualization  
├── requirements.txt # Python dependencies  
├── test.py # Test scripts  
└── README.md # This file  

## 📚 Key Components Explained  
### 1. PEA vs CTO Analysis
- PEA (Plan d'Épargne en Actions): French tax-advantaged account (17.2% tax after 5+ years)  
- CTO (Compte Titres Ordinaire): Regular brokerage account (30% flat tax)  
- Features: DCA simulations, tax impact analysis, long-term performance comparison  

### 2. Monte Carlo Simulation
- Simulates 1,000+ possible future price paths  
- Calculates Value at Risk (VaR) and confidence intervals  
- Provides probability distributions for investment outcomes  

### 3. Technical Analysis Dashboard
- Real-time stock data fetching  
- Multiple technical indicators  
- Interactive HTML dashboards with Plotly  
- Export to CSV/Excel for further analysis  

### 4. Portfolio Optimization
- Modern Portfolio Theory implementation  
- Risk-return optimization  
- Correlation analysis between assets  
- Rebalancing strategy simulations  

## 📊 Sample Analysis
### PEA vs CTO Performance Comparison
The toolkit demonstrates that for French investors:  
- PEA is advantageous for long-term investments (>5 years)  
- Tax savings can reach 12.8% (30% CTO vs 17.2% PEA)  
- DCA strategies significantly reduce timing risk  

Technical Indicators Implemented  
- Trend indicators: Moving Averages (20, 50, 200 days)  
- Momentum indicators: RSI, MACD  
- Volatility indicators: Bollinger Bands  
- Volume analysis: Volume trends and confirmation  

## 🔧 Dependencies
### The project uses the following key libraries:

Data Analysis: pandas, numpy  
Visualization: plotly, matplotlib, seaborn  
Financial Data: yfinance, twelvedata  
GUI Applications: tkinter  
Scientific Computing: scipy  
  
Full list in requirements.txt.  

## ⚠️ Disclaimer
This software is for educational and research purposes only. It is not financial advice. Past performance does not   guarantee future results. Always consult with a qualified financial advisor before making investment decisions.

## Created by Guillaume Stelniceanu - For educational purposes in financial analysis and Python programming.  Happy analyzing! 📊💹