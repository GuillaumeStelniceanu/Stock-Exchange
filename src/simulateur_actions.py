"""
Simulateur d'actions avec interface graphique
Permet de simuler l'évolution d'une action sur différentes périodes
avec gestion de la fiscalité PEA/CTO
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
from datetime import datetime
import yfinance as yf
import warnings
warnings.filterwarnings('ignore')

class ActionSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulateur d'Investissement Actions")
        self.root.geometry("1200x800")
        
        # Variables de simulation
        self.setup_variables()
        self.setup_ui()
        
    def setup_variables(self):
        """Initialise les variables de simulation"""
        self.ticker_var = tk.StringVar(value="AAPL")
        self.initial_price_var = tk.DoubleVar(value=150.0)
        self.investment_var = tk.DoubleVar(value=5000.0)
        self.years_var = tk.IntVar(value=5)
        self.return_var = tk.DoubleVar(value=8.0)
        self.volatility_var = tk.DoubleVar(value=20.0)
        self.account_type_var = tk.StringVar(value="PEA")
        self.monthly_investment_var = tk.DoubleVar(value=100.0)
        self.dividend_yield_var = tk.DoubleVar(value=1.5)
        
        # Pour stocker les résultats
        self.simulation_results = None
        
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        # Style
        self.setup_styles()
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuration des poids
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # ===== PANEL GAUCHE : PARAMÈTRES =====
        left_panel = ttk.Frame(main_frame)
        left_panel.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Section Action
        action_frame = ttk.LabelFrame(left_panel, text="Action", padding="10")
        action_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.create_action_section(action_frame)
        
        # Section Investissement
        invest_frame = ttk.LabelFrame(left_panel, text="Investissement", padding="10")
        invest_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.create_investment_section(invest_frame)
        
        # Section Paramètres
        params_frame = ttk.LabelFrame(left_panel, text="Paramètres de Simulation", padding="10")
        params_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.create_params_section(params_frame)
        
        # Section Fiscalité
        tax_frame = ttk.LabelFrame(left_panel, text="Fiscalité", padding="10")
        tax_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.create_tax_section(tax_frame)
        
        # Boutons
        button_frame = ttk.Frame(left_panel)
        button_frame.pack(fill=tk.X, pady=20)
        
        self.create_buttons(button_frame)
        
        # ===== PANEL DROIT : RÉSULTATS =====
        right_panel = ttk.Frame(main_frame)
        right_panel.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_panel.columnconfigure(0, weight=1)
        right_panel.rowconfigure(0, weight=1)
        
        # Graphique
        graph_frame = ttk.LabelFrame(right_panel, text="Évolution de l'investissement", padding="10")
        graph_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        graph_frame.columnconfigure(0, weight=1)
        graph_frame.rowconfigure(0, weight=1)
        
        self.fig, self.ax = plt.subplots(figsize=(10, 6), facecolor='#f8f9fa')
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Résultats détaillés
        results_frame = ttk.LabelFrame(right_panel, text="Résultats détaillés", padding="10")
        results_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.create_results_section(results_frame)
        
    def setup_styles(self):
        """Configure les styles de l'interface"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Couleurs personnalisées
        self.colors = {
            'bg': '#f5f5f5',
            'fg': '#333333',
            'accent': '#2196F3',
            'success': '#4CAF50',
            'warning': '#FF9800',
            'danger': '#F44336',
            'pea': '#2196F3',
            'cto': '#FF5722'
        }
        
    def create_action_section(self, parent):
        """Crée la section action"""
        # Ticker
        ttk.Label(parent, text="Symbole:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        ticker_frame = ttk.Frame(parent)
        ticker_frame.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        self.ticker_entry = ttk.Entry(ticker_frame, textvariable=self.ticker_var, width=12)
        self.ticker_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(ticker_frame, text="Actualiser", 
                  command=self.fetch_current_price, width=10).pack(side=tk.LEFT)
        
        # Prix initial
        ttk.Label(parent, text="Prix initial (€):").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(parent, textvariable=self.initial_price_var, width=15).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Rendement dividende
        ttk.Label(parent, text="Rendement dividende (%):").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(parent, textvariable=self.dividend_yield_var, width=15).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Actions populaires
        ttk.Label(parent, text="Actions rapides:").grid(row=3, column=0, sticky=tk.W, pady=5)
        
        quick_frame = ttk.Frame(parent)
        quick_frame.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        popular_stocks = [
            ("AAPL", "Apple"),
            ("MSFT", "Microsoft"),
            ("GOOGL", "Google"),
            ("AMZN", "Amazon"),
            ("NVDA", "NVIDIA"),
            ("TTE.PA", "Total"),
            ("AI.PA", "Air Liquide")
        ]
        
        for i, (ticker, name) in enumerate(popular_stocks):
            btn = ttk.Button(quick_frame, text=ticker, width=6,
                           command=lambda t=ticker: self.set_ticker(t))
            btn.pack(side=tk.LEFT, padx=2)
        
    def create_investment_section(self, parent):
        """Crée la section investissement"""
        # Investissement initial
        ttk.Label(parent, text="Investissement initial (€):").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(parent, textvariable=self.investment_var, width=15).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Investissement mensuel
        ttk.Label(parent, text="Investissement mensuel (€):").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(parent, textvariable=self.monthly_investment_var, width=15).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Durée
        ttk.Label(parent, text="Durée (années):").grid(row=2, column=0, sticky=tk.W, pady=5)
        
        years_frame = ttk.Frame(parent)
        years_frame.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        years = [1, 3, 5, 10, 15, 20, 30]
        for year in years:
            ttk.Radiobutton(years_frame, text=str(year), 
                          variable=self.years_var, value=year).pack(side=tk.LEFT, padx=2)
        
    def create_params_section(self, parent):
        """Crée la section paramètres"""
        # Rendement annuel
        ttk.Label(parent, text="Rendement annuel estimé (%):").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        return_frame = ttk.Frame(parent)
        return_frame.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Entry(return_frame, textvariable=self.return_var, width=8).pack(side=tk.LEFT, padx=(0, 5))
        
        # Boutons rapides pour rendement
        quick_returns = [5, 8, 10, 12, 15]
        for ret in quick_returns:
            ttk.Button(return_frame, text=f"{ret}%", width=4,
                      command=lambda r=ret: self.return_var.set(r)).pack(side=tk.LEFT, padx=1)
        
        # Volatilité
        ttk.Label(parent, text="Volatilité (%):").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        vol_frame = ttk.Frame(parent)
        vol_frame.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Entry(vol_frame, textvariable=self.volatility_var, width=8).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Scale(vol_frame, from_=5, to=50, variable=self.volatility_var,
                 orient=tk.HORIZONTAL, length=120).pack(side=tk.LEFT)
        
    def create_tax_section(self, parent):
        """Crée la section fiscalité"""
        # Type de compte
        ttk.Label(parent, text="Type de compte:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        account_frame = ttk.Frame(parent)
        account_frame.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Radiobutton(account_frame, text="PEA (17.2% après 5 ans)",
                       variable=self.account_type_var, value="PEA").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(account_frame, text="CTO (30% PFU)",
                       variable=self.account_type_var, value="CTO").pack(side=tk.LEFT, padx=5)
        
        # Explication fiscale
        info_text = "• PEA: Prélèvements sociaux après 5 ans\n• CTO: Flat tax (30%) chaque année"
        ttk.Label(parent, text=info_text, font=('Arial', 9), 
                 foreground='#666666').grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)
        
    def create_buttons(self, parent):
        """Crée les boutons d'action"""
        ttk.Button(parent, text="🎯 Lancer la Simulation", 
                  command=self.run_simulation, style="Accent.TButton",
                  padding=10).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        ttk.Button(parent, text="🔄 Réinitialiser", 
                  command=self.reset_values, padding=10).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(parent, text="💾 Exporter", 
                  command=self.export_results, padding=10).pack(side=tk.LEFT, padx=5)
        
        # Style pour le bouton principal
        style = ttk.Style()
        style.configure("Accent.TButton", 
                       background=self.colors['accent'],
                       foreground='white',
                       font=('Arial', 10, 'bold'))
        
    def create_results_section(self, parent):
        """Crée la section résultats"""
        # Créer un notebook pour les résultats
        self.results_notebook = ttk.Notebook(parent)
        self.results_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Onglet Résumé
        summary_tab = ttk.Frame(self.results_notebook)
        self.results_notebook.add(summary_tab, text="Résumé")
        
        self.create_summary_tab(summary_tab)
        
        # Onglet Détails
        details_tab = ttk.Frame(self.results_notebook)
        self.results_notebook.add(details_tab, text="Détails")
        
        self.create_details_tab(details_tab)
        
    def create_summary_tab(self, parent):
        """Crée l'onglet résumé"""
        # Cadre pour les indicateurs
        indicators_frame = ttk.Frame(parent)
        indicators_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Indicateurs clés
        self.summary_indicators = {}
        
        indicators = [
            ("Valeur finale", "final_value"),
            ("Gain total", "total_gain"),
            ("Impôts payés", "tax_paid"),
            ("Rendement annuel", "annual_return"),
            ("Nombre d'actions", "shares"),
            ("Dividendes reçus", "dividends")
        ]
        
        for i, (label, key) in enumerate(indicators):
            frame = ttk.LabelFrame(indicators_frame, text=label, padding="5")
            frame.grid(row=i//2, column=i%2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
            
            value_label = ttk.Label(frame, text="-", font=('Arial', 12, 'bold'))
            value_label.pack()
            
            self.summary_indicators[key] = value_label
        
        # Configuration des poids
        for i in range(2):
            indicators_frame.columnconfigure(i, weight=1)
        
    def create_details_tab(self, parent):
        """Crée l'onglet détails"""
        # Zone de texte pour les détails
        self.details_text = tk.Text(parent, height=15, font=('Courier', 10), wrap=tk.WORD)
        self.details_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(parent, command=self.details_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.details_text.config(yscrollcommand=scrollbar.set)
        
    def set_ticker(self, ticker):
        """Définit le ticker sélectionné"""
        self.ticker_var.set(ticker)
        self.fetch_current_price()
        
    def fetch_current_price(self):
        """Récupère le prix actuel depuis Yahoo Finance"""
        ticker = self.ticker_var.get().strip().upper()
        
        if not ticker:
            messagebox.showwarning("Avertissement", "Veuillez entrer un symbole d'action")
            return
        
        try:
            # Ajouter .PA pour les actions françaises si nécessaire
            if not any(ext in ticker for ext in ['.PA', '.DE', '.AS', '.MI']):
                # Essayer différentes bourses
                for exchange in ['', '.PA', '.DE']:
                    try:
                        full_ticker = ticker + exchange
                        stock = yf.Ticker(full_ticker)
                        hist = stock.history(period="1d")
                        
                        if not hist.empty:
                            current_price = hist['Close'].iloc[-1]
                            self.initial_price_var.set(round(float(current_price), 2))
                            
                            # Afficher aussi des infos sur l'action
                            info = stock.info
                            company_name = info.get('longName', ticker)
                            dividend_yield = info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 1.5
                            self.dividend_yield_var.set(round(dividend_yield, 2))
                            
                            messagebox.showinfo("Prix récupéré", 
                                              f"{company_name} ({full_ticker})\n"
                                              f"Prix actuel: {current_price:.2f} €\n"
                                              f"Dividende: {dividend_yield:.2f}%")
                            break
                    except:
                        continue
                else:
                    messagebox.showerror("Erreur", f"Impossible de récupérer le prix pour {ticker}")
            else:
                # Ticker avec extension déjà présente
                stock = yf.Ticker(ticker)
                hist = stock.history(period="1d")
                
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    self.initial_price_var.set(round(float(current_price), 2))
                    
                    messagebox.showinfo("Prix récupéré", 
                                      f"Prix actuel de {ticker}: {current_price:.2f} €")
                else:
                    messagebox.showerror("Erreur", f"Impossible de récupérer le prix pour {ticker}")
                    
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération: {str(e)}")
    
    def simulate_stock_price(self, initial_price, years, annual_return, volatility, dividend_yield):
        """Simule le prix d'une action avec marche aléatoire et dividendes"""
        months = years * 12
        
        # Paramètres mensuels
        monthly_return = annual_return / 100 / 12
        monthly_vol = volatility / 100 / np.sqrt(12)
        monthly_dividend = dividend_yield / 100 / 12
        
        # Génération aléatoire
        np.random.seed(int(datetime.now().timestamp()))
        price_shocks = np.random.normal(monthly_return, monthly_vol, months)
        
        # Simulation
        prices = [initial_price]
        dividends = [0]
        
        for i in range(months):
            # Nouveau prix avec choc aléatoire
            new_price = prices[-1] * (1 + price_shocks[i])
            
            # Ajouter l'effet dividende (réinvesti)
            dividend_amount = prices[-1] * monthly_dividend
            new_price += dividend_amount
            
            prices.append(new_price)
            dividends.append(dividend_amount)
        
        return np.array(prices), np.array(dividends)
    
    def calculate_investment_value(self, price_series, dividend_series, initial_investment, 
                                   monthly_investment, account_type, years):
        """Calcule la valeur de l'investissement avec fiscalité"""
        months = years * 12
        
        # Nombre d'actions initial
        initial_shares = initial_investment / price_series[0]
        
        # Simulation mois par mois
        shares = initial_shares
        total_invested = initial_investment
        total_dividends = 0
        value_history = []
        shares_history = []
        
        for month in range(1, months + 1):
            # Dividendes du mois (réinvestis)
            if month < len(dividend_series):
                dividend_per_share = dividend_series[month]
                dividend_total = shares * dividend_per_share
                total_dividends += dividend_total
                
                # Réinvestissement des dividendes
                dividend_shares = dividend_total / price_series[month]
                shares += dividend_shares
            
            # Investissement mensuel
            if monthly_investment > 0:
                monthly_shares = monthly_investment / price_series[month]
                shares += monthly_shares
                total_invested += monthly_investment
            
            # Valeur actuelle
            current_value = shares * price_series[month]
            value_history.append(current_value)
            shares_history.append(shares)
        
        # Résultats bruts
        final_value_brut = value_history[-1]
        total_gain_brut = final_value_brut - total_invested
        
        # Fiscalité
        if account_type == "PEA":
            # PEA: PS après 5 ans (17.2%)
            if years >= 5:
                tax_rate = 0.172
            else:
                tax_rate = 0.0
        else:
            # CTO: Flat tax 30% (avec possibilité de déduction des pertes)
            tax_rate = 0.30
        
        # Calcul des impôts
        tax_paid = total_gain_brut * tax_rate if total_gain_brut > 0 else 0
        
        # Résultats nets
        final_value_net = final_value_brut - tax_paid
        total_gain_net = total_gain_brut - tax_paid
        
        # Rendement annualisé
        if total_invested > 0:
            cagr = ((final_value_net / total_invested) ** (1/years) - 1) * 100
        else:
            cagr = 0
        
        return {
            'final_value_brut': final_value_brut,
            'final_value_net': final_value_net,
            'total_invested': total_invested,
            'total_gain_brut': total_gain_brut,
            'total_gain_net': total_gain_net,
            'tax_paid': tax_paid,
            'tax_rate': tax_rate,
            'cagr': cagr,
            'total_dividends': total_dividends,
            'final_shares': shares,
            'value_history': value_history,
            'shares_history': shares_history,
            'price_history': price_series[1:],  # Exclure le prix initial
            'months': months
        }
    
    def run_simulation(self):
        """Lance la simulation complète"""
        try:
            # Récupération des paramètres
            ticker = self.ticker_var.get()
            initial_price = self.initial_price_var.get()
            initial_investment = self.investment_var.get()
            monthly_investment = self.monthly_investment_var.get()
            years = self.years_var.get()
            annual_return = self.return_var.get()
            volatility = self.volatility_var.get()
            account_type = self.account_type_var.get()
            dividend_yield = self.dividend_yield_var.get()
            
            # Validation
            if initial_price <= 0:
                messagebox.showerror("Erreur", "Le prix initial doit être positif")
                return
            
            if initial_investment <= 0:
                messagebox.showerror("Erreur", "L'investissement initial doit être positif")
                return
            
            # Simulation
            price_series, dividend_series = self.simulate_stock_price(
                initial_price, years, annual_return, volatility, dividend_yield
            )
            
            self.simulation_results = self.calculate_investment_value(
                price_series, dividend_series, initial_investment, 
                monthly_investment, account_type, years
            )
            
            # Mise à jour de l'interface
            self.update_chart(ticker, account_type, years)
            self.update_summary()
            self.update_details()
            
            messagebox.showinfo("Succès", "Simulation terminée avec succès!")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la simulation:\n{str(e)}")
    
    def update_chart(self, ticker, account_type, years):
        """Met à jour le graphique"""
        if not self.simulation_results:
            return
        
        self.ax.clear()
        
        # Données
        months = self.simulation_results['months']
        time_axis = np.arange(months) / 12  # Convertir en années
        
        # Courbe de la valeur du portefeuille
        self.ax.plot(time_axis, self.simulation_results['value_history'], 
                    label="Valeur du portefeuille", 
                    color=self.colors['accent'], linewidth=3, alpha=0.8)
        
        # Courbe du prix de l'action (mise à l'échelle)
        price_scaled = (self.simulation_results['price_history'] / 
                       self.simulation_results['price_history'][0] * 
                       self.simulation_results['value_history'][0])
        
        self.ax.plot(time_axis, price_scaled, 
                    label="Prix de l'action (relatif)", 
                    color='gray', linewidth=1, alpha=0.5, linestyle='--')
        
        # Lignes horizontales pour les repères
        self.ax.axhline(y=self.simulation_results['total_invested'], 
                       color='black', linestyle=':', alpha=0.3, 
                       label=f"Investissement: {self.simulation_results['total_invested']:,.0f} €")
        
        self.ax.axhline(y=self.simulation_results['final_value_brut'], 
                       color='red', linestyle='--', alpha=0.5, 
                       label=f"Valeur brute: {self.simulation_results['final_value_brut']:,.0f} €")
        
        self.ax.axhline(y=self.simulation_results['final_value_net'], 
                       color='green', linestyle='--', alpha=0.5, 
                       label=f"Valeur nette: {self.simulation_results['final_value_net']:,.0f} €")
        
        # Configuration
        self.ax.set_xlabel("Années", fontsize=12)
        self.ax.set_ylabel("Valeur (€)", fontsize=12)
        
        title_color = self.colors['pea'] if account_type == "PEA" else self.colors['cto']
        self.ax.set_title(
            f"Simulation: {ticker} - {years} ans ({account_type})", 
            fontsize=14, fontweight='bold', color=title_color
        )
        
        self.ax.grid(True, alpha=0.3)
        self.ax.legend(loc='upper left', fontsize=9)
        
        # Formater l'axe Y
        self.ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f} €'))
        
        # Ajouter une zone colorée pour les gains/pertes
        invest_line = self.simulation_results['total_invested']
        y_min, y_max = self.ax.get_ylim()
        
        if y_min < invest_line:
            self.ax.fill_between(time_axis, y_min, invest_line, 
                                alpha=0.1, color='red', label='Perte potentielle')
        
        if y_max > invest_line:
            self.ax.fill_between(time_axis, invest_line, y_max, 
                                alpha=0.1, color='green', label='Gain potentiel')
        
        self.fig.tight_layout()
        self.canvas.draw()
    
    def update_summary(self):
        """Met à jour le résumé des résultats"""
        if not self.simulation_results:
            return
        
        results = self.simulation_results
        
        # Formater les valeurs
        def format_currency(value):
            return f"{value:,.2f} €"
        
        def format_percentage(value):
            return f"{value:.2f}%"
        
        def format_shares(value):
            return f"{value:,.2f}"
        
        # Mise à jour des indicateurs
        self.summary_indicators['final_value'].config(
            text=format_currency(results['final_value_net']),
            foreground='green' if results['final_value_net'] > results['total_invested'] else 'red'
        )
        
        self.summary_indicators['total_gain'].config(
            text=format_currency(results['total_gain_net']),
            foreground='green' if results['total_gain_net'] > 0 else 'red'
        )
        
        self.summary_indicators['tax_paid'].config(
            text=format_currency(results['tax_paid']),
            foreground='orange' if results['tax_paid'] > 0 else 'black'
        )
        
        self.summary_indicators['annual_return'].config(
            text=format_percentage(results['cagr']),
            foreground='green' if results['cagr'] > 0 else 'red'
        )
        
        self.summary_indicators['shares'].config(
            text=format_shares(results['final_shares'])
        )
        
        self.summary_indicators['dividends'].config(
            text=format_currency(results['total_dividends'])
        )
    
    def update_details(self):
        """Met à jour les détails textuels"""
        if not self.simulation_results:
            return
        
        results = self.simulation_results
        
        # Construire le texte détaillé
        details = f"""
{'='*60}
RÉSULTATS DÉTAILLÉS DE LA SIMULATION
{'='*60}

PARAMÈTRES INITIAUX:
• Action: {self.ticker_var.get()}
• Prix initial: {self.initial_price_var.get():.2f} €
• Investissement initial: {self.investment_var.get():.2f} €
• Investissement mensuel: {self.monthly_investment_var.get():.2f} €
• Durée: {self.years_var.get()} ans
• Rendement estimé: {self.return_var.get():.1f}%
• Volatilité: {self.volatility_var.get():.1f}%
• Type de compte: {self.account_type_var.get()}
• Rendement dividende: {self.dividend_yield_var.get():.1f}%

{'='*60}
RÉSULTATS FINANCIERS:
{'='*60}

INVESTISSEMENT TOTAL:
• Capital investi: {results['total_invested']:,.2f} €

VALEUR FINALE:
• Valeur brute: {results['final_value_brut']:,.2f} €
• Gain brut: {results['total_gain_brut']:,.2f} €

FISCALITÉ ({self.account_type_var.get()}):
• Taux d'imposition: {results['tax_rate']*100:.1f}%
• Impôts payés: {results['tax_paid']:,.2f} €

RÉSULTATS NETS:
• Valeur nette: {results['final_value_net']:,.2f} €
• Gain net: {results['total_gain_net']:,.2f} €

INDICATEURS DE PERFORMANCE:
• Rendement annualisé (CAGR): {results['cagr']:.2f}%
• Dividendes totaux reçus: {results['total_dividends']:,.2f} €
• Nombre final d'actions: {results['final_shares']:,.2f}

{'='*60}
ANALYSE:
{'='*60}
"""
        
        # Ajouter une analyse qualitative
        if results['cagr'] > 10:
            details += "• 📈 Performance EXCELLENTE (>10% annuel)\n"
        elif results['cagr'] > 5:
            details += "• 📊 Performance BONNE (5-10% annuel)\n"
        elif results['cagr'] > 0:
            details += "• ✅ Performance POSITIVE mais modérée\n"
        else:
            details += "• ⚠️ Performance NÉGATIVE\n"
        
        if results['tax_paid'] > 0:
            if self.account_type_var.get() == "PEA":
                details += f"• 🏦 PEA: Économie fiscale de {(0.30 - results['tax_rate'])*100:.1f}% vs CTO\n"
            else:
                details += "• 💰 CTO: Flat tax appliquée chaque année\n"
        
        if results['total_dividends'] > 0:
            details += f"• 💵 Dividendes: {results['total_dividends']/results['total_invested']*100:.1f}% du capital investi\n"
        
        # Effacer et insérer le texte
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(1.0, details)
        
        # Mettre en forme certaines parties
        self.details_text.tag_add("title", "1.0", "3.0")
        self.details_text.tag_config("title", font=('Courier', 11, 'bold'))
        
    def reset_values(self):
        """Réinitialise tous les paramètres"""
        self.ticker_var.set("AAPL")
        self.initial_price_var.set(150.0)
        self.investment_var.set(5000.0)
        self.monthly_investment_var.set(100.0)
        self.years_var.set(5)
        self.return_var.set(8.0)
        self.volatility_var.set(20.0)
        self.account_type_var.set("PEA")
        self.dividend_yield_var.set(1.5)
        
        # Réinitialiser le graphique
        self.ax.clear()
        self.ax.text(0.5, 0.5, "Prêt à simuler\n\nCliquez sur 'Lancer la Simulation'", 
                    ha='center', va='center', transform=self.ax.transAxes, 
                    fontsize=14, color='gray')
        self.ax.set_title("Simulateur d'Investissement Actions", fontsize=16)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.canvas.draw()
        
        # Réinitialiser les résultats
        for indicator in self.summary_indicators.values():
            indicator.config(text="-", foreground='black')
        
        self.details_text.delete(1.0, tk.END)
        
        self.simulation_results = None
    
    def export_results(self):
        """Exporte les résultats au format CSV"""
        if not self.simulation_results:
            messagebox.showwarning("Avertissement", "Veuillez d'abord lancer une simulation")
            return
        
        try:
            # Demander le fichier de destination
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[
                    ("Fichiers CSV", "*.csv"),
                    ("Fichiers Excel", "*.xlsx"),
                    ("Tous les fichiers", "*.*")
                ],
                initialfile=f"simulation_{self.ticker_var.get()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )
            
            if filename:
                # Préparer les données
                data = {
                    'Paramètre': [
                        'Ticker', 'Prix initial', 'Investissement initial', 
                        'Investissement mensuel', 'Durée (années)', 'Rendement estimé',
                        'Volatilité', 'Type compte', 'Rendement dividende'
                    ],
                    'Valeur': [
                        self.ticker_var.get(),
                        self.initial_price_var.get(),
                        self.investment_var.get(),
                        self.monthly_investment_var.get(),
                        self.years_var.get(),
                        self.return_var.get(),
                        self.volatility_var.get(),
                        self.account_type_var.get(),
                        self.dividend_yield_var.get()
                    ]
                }
                
                df_params = pd.DataFrame(data)
                
                # Ajouter les résultats
                results_data = {
                    'Résultat': [
                        'Valeur finale brute', 'Valeur finale nette',
                        'Investissement total', 'Gain brut', 'Gain net',
                        'Impôts payés', 'Taux imposition', 'CAGR',
                        'Dividendes totaux', 'Nombre d\'actions final'
                    ],
                    'Valeur': [
                        self.simulation_results['final_value_brut'],
                        self.simulation_results['final_value_net'],
                        self.simulation_results['total_invested'],
                        self.simulation_results['total_gain_brut'],
                        self.simulation_results['total_gain_net'],
                        self.simulation_results['tax_paid'],
                        self.simulation_results['tax_rate'] * 100,
                        self.simulation_results['cagr'],
                        self.simulation_results['total_dividends'],
                        self.simulation_results['final_shares']
                    ],
                    'Unité': [
                        '€', '€', '€', '€', '€', '€', '%', '%', '€', 'actions'
                    ]
                }
                
                df_results = pd.DataFrame(results_data)
                
                # Sauvegarder
                if filename.endswith('.csv'):
                    df_params.to_csv(filename, index=False)
                    # Sauver les résultats dans un second fichier
                    results_filename = filename.replace('.csv', '_resultats.csv')
                    df_results.to_csv(results_filename, index=False)
                elif filename.endswith('.xlsx'):
                    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                        df_params.to_excel(writer, sheet_name='Paramètres', index=False)
                        df_results.to_excel(writer, sheet_name='Résultats', index=False)
                
                messagebox.showinfo("Succès", f"Résultats exportés dans:\n{filename}")
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'export:\n{str(e)}")

def main():
    """Fonction principale"""
    root = tk.Tk()
    
    # Centrer la fenêtre
    window_width = 1200
    window_height = 800
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # Créer l'application
    app = ActionSimulatorGUI(root)
    
    # Lancer la boucle principale
    root.mainloop()

if __name__ == "__main__":
    main()