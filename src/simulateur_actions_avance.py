"""
Simulateur d'actions avancé avec Monte Carlo et comparaison PEA/CTO
Version complète avec interface graphique professionnelle
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class AdvancedStockSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("💰 Simulateur d'Actions Avancé")
        self.root.geometry("1400x900")
        
        # Configuration des couleurs
        self.setup_colors()
        
        # Variables globales
        self.simulation_results = {}
        self.monte_carlo_results = None
        
        # Initialisation de l'interface
        self.setup_ui()
        
    def setup_colors(self):
        """Configuration du thème couleur"""
        self.colors = {
            'bg_light': '#f8f9fa',
            'bg_dark': '#343a40',
            'primary': '#007bff',
            'secondary': '#6c757d',
            'success': '#28a745',
            'danger': '#dc3545',
            'warning': '#ffc107',
            'info': '#17a2b8',
            'light': '#f8f9fa',
            'dark': '#343a40',
            'pea': '#20c997',
            'cto': '#fd7e14',
            'chart_1': '#1f77b4',
            'chart_2': '#ff7f0e',
            'chart_3': '#2ca02c',
            'chart_4': '#d62728'
        }
        
    def setup_ui(self):
        """Configuration de l'interface utilisateur"""
        # Style
        self.setup_styles()
        
        # Frame principal avec scrollbar
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas avec scrollbar
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Contenu de l'interface
        self.create_header(scrollable_frame)
        self.create_input_section(scrollable_frame)
        self.create_advanced_section(scrollable_frame)
        self.create_visualization_section(scrollable_frame)
        self.create_results_section(scrollable_frame)
        
    def setup_styles(self):
        """Configuration des styles ttk"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configuration des styles personnalisés
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Subtitle.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Accent.TButton', font=('Arial', 10, 'bold'), padding=10)
        style.configure('Success.TButton', background=self.colors['success'], foreground='white')
        style.configure('Primary.TButton', background=self.colors['primary'], foreground='white')
        
    def create_header(self, parent):
        """Crée l'en-tête de l'application"""
        header_frame = ttk.Frame(parent, padding="20")
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Titre
        title_label = ttk.Label(
            header_frame,
            text="💰 SIMULATEUR D'INVESTISSEMENT AVANCÉ",
            style='Title.TLabel',
            foreground=self.colors['primary']
        )
        title_label.pack()
        
        # Sous-titre
        subtitle_label = ttk.Label(
            header_frame,
            text="Simulation Monte Carlo • Comparaison PEA/CTO • Analyse de risque",
            font=('Arial', 11),
            foreground=self.colors['secondary']
        )
        subtitle_label.pack(pady=(5, 0))
        
    def create_input_section(self, parent):
        """Crée la section de saisie des paramètres"""
        input_frame = ttk.LabelFrame(parent, text="📊 Paramètres de Base", padding="15")
        input_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Variables
        self.ticker_var = tk.StringVar(value="AAPL")
        self.initial_price_var = tk.DoubleVar(value=150.0)
        self.investment_var = tk.DoubleVar(value=10000.0)
        self.monthly_investment_var = tk.DoubleVar(value=500.0)
        self.years_var = tk.IntVar(value=10)
        self.annual_return_var = tk.DoubleVar(value=8.0)
        self.volatility_var = tk.DoubleVar(value=20.0)
        self.dividend_yield_var = tk.DoubleVar(value=1.5)
        
        # Grille pour les paramètres
        row = 0
        
        # Ligne 1: Ticker et prix
        ttk.Label(input_frame, text="Symbole de l'action:").grid(row=row, column=0, sticky=tk.W, pady=5)
        
        ticker_frame = ttk.Frame(input_frame)
        ticker_frame.grid(row=row, column=1, sticky=tk.W, pady=5)
        
        self.ticker_entry = ttk.Entry(ticker_frame, textvariable=self.ticker_var, width=10)
        self.ticker_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(ticker_frame, text="Prix actuel", 
                  command=self.fetch_current_price).pack(side=tk.LEFT, padx=2)
        
        ttk.Label(input_frame, text="Prix initial (€):").grid(row=row, column=2, sticky=tk.W, padx=20, pady=5)
        ttk.Entry(input_frame, textvariable=self.initial_price_var, width=10).grid(row=row, column=3, sticky=tk.W, pady=5)
        
        row += 1
        
        # Ligne 2: Investissements
        ttk.Label(input_frame, text="Investissement initial (€):").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(input_frame, textvariable=self.investment_var, width=10).grid(row=row, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(input_frame, text="Investissement mensuel (€):").grid(row=row, column=2, sticky=tk.W, padx=20, pady=5)
        ttk.Entry(input_frame, textvariable=self.monthly_investment_var, width=10).grid(row=row, column=3, sticky=tk.W, pady=5)
        
        row += 1
        
        # Ligne 3: Durée
        ttk.Label(input_frame, text="Durée (années):").grid(row=row, column=0, sticky=tk.W, pady=5)
        
        years_frame = ttk.Frame(input_frame)
        years_frame.grid(row=row, column=1, sticky=tk.W, pady=5)
        
        years_options = [1, 3, 5, 10, 15, 20, 30]
        for year in years_options:
            ttk.Radiobutton(years_frame, text=str(year), 
                          variable=self.years_var, value=year).pack(side=tk.LEFT, padx=2)
        
        row += 1
        
        # Ligne 4: Rendement et volatilité
        ttk.Label(input_frame, text="Rendement annuel estimé (%):").grid(row=row, column=0, sticky=tk.W, pady=5)
        
        return_frame = ttk.Frame(input_frame)
        return_frame.grid(row=row, column=1, sticky=tk.W, pady=5)
        
        ttk.Entry(return_frame, textvariable=self.annual_return_var, width=8).pack(side=tk.LEFT, padx=(0, 5))
        
        # Boutons rapides pour rendement
        for ret in [5, 8, 10, 12, 15]:
            ttk.Button(return_frame, text=f"{ret}%", width=4,
                      command=lambda r=ret: self.annual_return_var.set(r)).pack(side=tk.LEFT, padx=1)
        
        ttk.Label(input_frame, text="Volatilité (%):").grid(row=row, column=2, sticky=tk.W, padx=20, pady=5)
        
        vol_frame = ttk.Frame(input_frame)
        vol_frame.grid(row=row, column=3, sticky=tk.W, pady=5)
        
        ttk.Entry(vol_frame, textvariable=self.volatility_var, width=8).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Scale(vol_frame, from_=5, to=50, variable=self.volatility_var,
                 orient=tk.HORIZONTAL, length=100).pack(side=tk.LEFT)
        
        row += 1
        
        # Ligne 5: Dividende
        ttk.Label(input_frame, text="Rendement dividende (%):").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(input_frame, textvariable=self.dividend_yield_var, width=10).grid(row=row, column=1, sticky=tk.W, pady=5)
        
        # Boutons d'action rapides
        action_frame = ttk.Frame(input_frame)
        action_frame.grid(row=row, column=2, columnspan=2, sticky=tk.E, pady=5)
        
        ttk.Button(action_frame, text="Simulation Simple", 
                  command=self.run_simple_simulation,
                  style='Primary.TButton').pack(side=tk.LEFT, padx=2)
        
        ttk.Button(action_frame, text="Monte Carlo", 
                  command=self.run_monte_carlo,
                  style='Success.TButton').pack(side=tk.LEFT, padx=2)
        
    def create_advanced_section(self, parent):
        """Crée la section des paramètres avancés"""
        advanced_frame = ttk.LabelFrame(parent, text="⚙️ Paramètres Avancés", padding="15")
        advanced_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Variables avancées
        self.monte_carlo_sims_var = tk.IntVar(value=1000)
        self.confidence_level_var = tk.DoubleVar(value=95.0)
        self.scenarios_var = tk.IntVar(value=3)
        self.inflation_rate_var = tk.DoubleVar(value=2.0)
        self.tax_scenario_var = tk.StringVar(value="current")
        
        # Grille pour paramètres avancés
        row = 0
        
        # Monte Carlo
        ttk.Label(advanced_frame, text="Simulations Monte Carlo:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(advanced_frame, textvariable=self.monte_carlo_sims_var, width=10).grid(row=row, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(advanced_frame, text="Niveau de confiance (%):").grid(row=row, column=2, sticky=tk.W, padx=20, pady=5)
        ttk.Entry(advanced_frame, textvariable=self.confidence_level_var, width=10).grid(row=row, column=3, sticky=tk.W, pady=5)
        
        row += 1
        
        # Scénarios
        ttk.Label(advanced_frame, text="Nombre de scénarios:").grid(row=row, column=0, sticky=tk.W, pady=5)
        
        scenarios_frame = ttk.Frame(advanced_frame)
        scenarios_frame.grid(row=row, column=1, sticky=tk.W, pady=5)
        
        for scenario in [1, 3, 5]:
            ttk.Radiobutton(scenarios_frame, text=str(scenario), 
                          variable=self.scenarios_var, value=scenario).pack(side=tk.LEFT, padx=2)
        
        # Inflation
        ttk.Label(advanced_frame, text="Taux d'inflation (%):").grid(row=row, column=2, sticky=tk.W, padx=20, pady=5)
        ttk.Entry(advanced_frame, textvariable=self.inflation_rate_var, width=10).grid(row=row, column=3, sticky=tk.W, pady=5)
        
        row += 1
        
        # Scénarios fiscaux
        ttk.Label(advanced_frame, text="Scénario fiscal:").grid(row=row, column=0, sticky=tk.W, pady=5)
        
        tax_frame = ttk.Frame(advanced_frame)
        tax_frame.grid(row=row, column=1, columnspan=3, sticky=tk.W, pady=5)
        
        tax_scenarios = [
            ("current", "Actuel (PEA 17.2%, CTO 30%)"),
            ("optimistic", "Optimiste (baisse des taxes)"),
            ("pessimistic", "Pessimiste (hausse des taxes)")
        ]
        
        for value, text in tax_scenarios:
            ttk.Radiobutton(tax_frame, text=text, 
                          variable=self.tax_scenario_var, value=value).pack(side=tk.LEFT, padx=10)
        
    def create_visualization_section(self, parent):
        """Crée la section de visualisation"""
        viz_frame = ttk.Frame(parent)
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Notebook pour les différents graphiques
        self.viz_notebook = ttk.Notebook(viz_frame)
        self.viz_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Onglet 1: Simulation simple
        self.simple_tab = ttk.Frame(self.viz_notebook)
        self.viz_notebook.add(self.simple_tab, text="Simulation Simple")
        
        self.fig_simple = Figure(figsize=(10, 6), facecolor=self.colors['bg_light'])
        self.ax_simple = self.fig_simple.add_subplot(111)
        self.canvas_simple = FigureCanvasTkAgg(self.fig_simple, self.simple_tab)
        self.canvas_simple.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Onglet 2: Monte Carlo
        self.monte_tab = ttk.Frame(self.viz_notebook)
        self.viz_notebook.add(self.monte_tab, text="Monte Carlo")
        
        self.fig_monte = Figure(figsize=(10, 6), facecolor=self.colors['bg_light'])
        self.ax_monte = self.fig_monte.add_subplot(111)
        self.canvas_monte = FigureCanvasTkAgg(self.fig_monte, self.monte_tab)
        self.canvas_monte.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Onglet 3: Comparaison PEA/CTO
        self.comparison_tab = ttk.Frame(self.viz_notebook)
        self.viz_notebook.add(self.comparison_tab, text="Comparaison PEA/CTO")
        
        self.fig_comp = Figure(figsize=(10, 6), facecolor=self.colors['bg_light'])
        self.ax_comp = self.fig_comp.add_subplot(111)
        self.canvas_comp = FigureCanvasTkAgg(self.fig_comp, self.comparison_tab)
        self.canvas_comp.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Onglet 4: Distribution des résultats
        self.distribution_tab = ttk.Frame(self.viz_notebook)
        self.viz_notebook.add(self.distribution_tab, text="Distribution")
        
        self.fig_dist = Figure(figsize=(10, 6), facecolor=self.colors['bg_light'])
        self.ax_dist = self.fig_dist.add_subplot(111)
        self.canvas_dist = FigureCanvasTkAgg(self.fig_dist, self.distribution_tab)
        self.canvas_dist.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def create_results_section(self, parent):
        """Crée la section des résultats"""
        results_frame = ttk.LabelFrame(parent, text="📈 Résultats", padding="15")
        results_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Cadre pour les résultats principaux
        main_results_frame = ttk.Frame(results_frame)
        main_results_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Indicateurs de performance
        self.results_widgets = {}
        
        metrics = [
            ("Valeur finale", "final_value", "€"),
            ("Gain total", "total_gain", "€"),
            ("CAGR", "cagr", "%"),
            ("Sharpe Ratio", "sharpe", ""),
            ("VaR 95%", "var_95", "€"),
            ("Probabilité de perte", "loss_prob", "%")
        ]
        
        for i, (label, key, unit) in enumerate(metrics):
            frame = ttk.LabelFrame(main_results_frame, text=label, padding="5")
            frame.grid(row=i//3, column=i%3, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
            
            value_label = ttk.Label(frame, text="-", font=('Arial', 14, 'bold'))
            value_label.pack()
            
            unit_label = ttk.Label(frame, text=unit, font=('Arial', 10))
            unit_label.pack()
            
            self.results_widgets[key] = value_label
        
        # Configuration des poids
        for i in range(3):
            main_results_frame.columnconfigure(i, weight=1)
        
        # Boutons d'action
        action_frame = ttk.Frame(results_frame)
        action_frame.pack(fill=tk.X)
        
        ttk.Button(action_frame, text="📊 Comparer PEA vs CTO", 
                  command=self.compare_pea_cto).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(action_frame, text="📋 Générer Rapport", 
                  command=self.generate_report).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(action_frame, text="💾 Exporter Données", 
                  command=self.export_data).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(action_frame, text="🔄 Réinitialiser", 
                  command=self.reset_all).pack(side=tk.LEFT, padx=5)
        
    def fetch_current_price(self):
        """Récupère le prix actuel de l'action"""
        ticker = self.ticker_var.get().strip().upper()
        
        if not ticker:
            messagebox.showwarning("Avertissement", "Veuillez entrer un symbole d'action")
            return
        
        try:
            # Essayer différentes bourses
            exchanges = ['', '.PA', '.DE', '.AS', '.MI', '.BR']
            
            for exchange in exchanges:
                try:
                    full_ticker = ticker + exchange
                    stock = yf.Ticker(full_ticker)
                    hist = stock.history(period="5d")
                    
                    if not hist.empty and len(hist) > 0:
                        current_price = hist['Close'].iloc[-1]
                        self.initial_price_var.set(round(float(current_price), 2))
                        
                        # Récupérer des infos supplémentaires
                        info = stock.info
                        
                        # Dividende
                        if 'dividendYield' in info and info['dividendYield']:
                            dividend_yield = info['dividendYield'] * 100
                            self.dividend_yield_var.set(round(dividend_yield, 2))
                        
                        # Volatilité historique (52 semaines)
                        if '52WeekChange' in info and info['52WeekChange']:
                            hist_volatility = abs(info['52WeekChange']) * 100
                            self.volatility_var.set(min(round(hist_volatility, 1), 50))
                        
                        messagebox.showinfo(
                            "Prix récupéré",
                            f"✅ {full_ticker}: {current_price:.2f} €\n"
                            f"Dividende: {self.dividend_yield_var.get():.1f}%\n"
                            f"Volatilité historique: {self.volatility_var.get():.1f}%"
                        )
                        return
                        
                except:
                    continue
            
            messagebox.showerror("Erreur", f"Impossible de récupérer le prix pour {ticker}")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération: {str(e)}")
    
    def simulate_price_path(self, initial_price, years, annual_return, volatility, dividend_yield, random_seed=None):
        """Simule un chemin de prix avec marche aléatoire"""
        if random_seed is not None:
            np.random.seed(random_seed)
        
        months = years * 12
        
        # Paramètres mensuels
        monthly_return = annual_return / 100 / 12
        monthly_vol = volatility / 100 / np.sqrt(12)
        monthly_dividend = dividend_yield / 100 / 12
        
        # Génération des rendements
        returns = np.random.normal(monthly_return, monthly_vol, months)
        
        # Simulation des prix
        prices = [initial_price]
        
        for i in range(months):
            new_price = prices[-1] * (1 + returns[i])
            
            # Ajout des dividendes (réinvestis)
            dividend_amount = prices[-1] * monthly_dividend
            new_price += dividend_amount
            
            prices.append(new_price)
        
        return np.array(prices)
    
    def calculate_portfolio_value(self, price_path, initial_investment, monthly_investment, years):
        """Calcule la valeur du portefeuille"""
        months = years * 12
        
        # Actions initiales
        initial_shares = initial_investment / price_path[0]
        
        # Simulation mois par mois
        shares = initial_shares
        total_invested = initial_investment
        values = []
        
        for month in range(1, months + 1):
            # Investissement mensuel
            if monthly_investment > 0:
                monthly_shares = monthly_investment / price_path[month]
                shares += monthly_shares
                total_invested += monthly_investment
            
            # Valeur courante
            current_value = shares * price_path[month]
            values.append(current_value)
        
        final_value = values[-1] if values else 0
        
        return {
            'final_value': final_value,
            'total_invested': total_invested,
            'total_gain': final_value - total_invested,
            'final_shares': shares,
            'value_history': values,
            'price_history': price_path[1:]
        }
    
    def apply_taxation(self, portfolio_results, account_type, years, tax_scenario="current"):
        """Applique la fiscalité selon le type de compte"""
        gain = portfolio_results['total_gain']
        
        # Détermination des taux selon le scénario
        if tax_scenario == "optimistic":
            pea_rate = 0.15  # Baisse hypothétique
            cto_rate = 0.25
        elif tax_scenario == "pessimistic":
            pea_rate = 0.20  # Hausse hypothétique
            cto_rate = 0.35
        else:  # current
            pea_rate = 0.172
            cto_rate = 0.30
        
        # Application de la fiscalité
        if account_type == "PEA":
            if years >= 5:
                tax_rate = pea_rate
            else:
                tax_rate = 0.0
        else:  # CTO
            tax_rate = cto_rate
        
        # Calcul des impôts
        tax_paid = max(gain, 0) * tax_rate
        
        # Résultats après impôts
        final_value_net = portfolio_results['final_value'] - tax_paid
        total_gain_net = gain - tax_paid
        
        # Calcul du CAGR
        if portfolio_results['total_invested'] > 0:
            cagr = ((final_value_net / portfolio_results['total_invested']) ** (1/years) - 1) * 100
        else:
            cagr = 0
        
        return {
            **portfolio_results,
            'final_value_net': final_value_net,
            'total_gain_net': total_gain_net,
            'tax_paid': tax_paid,
            'tax_rate': tax_rate,
            'cagr': cagr,
            'account_type': account_type
        }
    
    def run_simple_simulation(self):
        """Exécute une simulation simple"""
        try:
            # Récupération des paramètres
            params = self.get_simulation_params()
            
            # Simulation du prix
            price_path = self.simulate_price_path(
                params['initial_price'],
                params['years'],
                params['annual_return'],
                params['volatility'],
                params['dividend_yield'],
                random_seed=42  # Seed fixe pour la reproductibilité
            )
            
            # Calcul du portefeuille
            portfolio = self.calculate_portfolio_value(
                price_path,
                params['initial_investment'],
                params['monthly_investment'],
                params['years']
            )
            
            # Application de la fiscalité PEA
            self.simulation_results['PEA'] = self.apply_taxation(
                portfolio, "PEA", params['years'], params['tax_scenario']
            )
            
            # Application de la fiscalité CTO
            self.simulation_results['CTO'] = self.apply_taxation(
                portfolio, "CTO", params['years'], params['tax_scenario']
            )
            
            # Mise à jour des visualisations
            self.update_simple_chart()
            self.update_results_display()
            
            messagebox.showinfo("Succès", "Simulation simple terminée!")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la simulation:\n{str(e)}")
    
    def run_monte_carlo(self):
        """Exécute une simulation Monte Carlo"""
        try:
            params = self.get_simulation_params()
            n_simulations = self.monte_carlo_sims_var.get()
            
            # Stockage des résultats
            pea_results = []
            cto_results = []
            all_simulations = []
            
            # Barre de progression
            progress_window = self.show_progress("Simulation Monte Carlo en cours...", n_simulations)
            
            # Exécution des simulations
            for i in range(n_simulations):
                # Simulation du prix
                price_path = self.simulate_price_path(
                    params['initial_price'],
                    params['years'],
                    params['annual_return'],
                    params['volatility'],
                    params['dividend_yield'],
                    random_seed=i  # Seed différente pour chaque simulation
                )
                
                # Calcul du portefeuille
                portfolio = self.calculate_portfolio_value(
                    price_path,
                    params['initial_investment'],
                    params['monthly_investment'],
                    params['years']
                )
                
                # Application des fiscalités
                pea_result = self.apply_taxation(portfolio, "PEA", params['years'], params['tax_scenario'])
                cto_result = self.apply_taxation(portfolio, "CTO", params['years'], params['tax_scenario'])
                
                pea_results.append(pea_result['final_value_net'])
                cto_results.append(cto_result['final_value_net'])
                all_simulations.append(price_path)
                
                # Mise à jour de la barre de progression
                if progress_window and i % 10 == 0:
                    progress_window.update_progress(i + 1)
            
            # Fermeture de la fenêtre de progression
            if progress_window:
                progress_window.destroy()
            
            # Calcul des statistiques
            self.monte_carlo_results = {
                'pea_results': np.array(pea_results),
                'cto_results': np.array(cto_results),
                'all_simulations': all_simulations,
                'params': params
            }
            
            # Mise à jour des visualisations
            self.update_monte_carlo_chart()
            self.update_distribution_chart()
            self.update_monte_carlo_results()
            
            messagebox.showinfo("Succès", f"Monte Carlo terminé!\n{len(pea_results)} simulations effectuées.")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de Monte Carlo:\n{str(e)}")
    
    def compare_pea_cto(self):
        """Compare les performances PEA vs CTO"""
        if not self.simulation_results:
            messagebox.showwarning("Avertissement", "Veuillez d'abord exécuter une simulation")
            return
        
        try:
            pea_result = self.simulation_results['PEA']
            cto_result = self.simulation_results['CTO']
            
            # Calcul des différences
            diff_value = pea_result['final_value_net'] - cto_result['final_value_net']
            diff_gain = pea_result['total_gain_net'] - cto_result['total_gain_net']
            diff_tax = cto_result['tax_paid'] - pea_result['tax_paid']
            
            # Mise à jour du graphique de comparaison
            self.update_comparison_chart()
            
            # Affichage des résultats
            comparison_text = (
                f"📊 COMPARAISON PEA vs CTO\n"
                f"{'='*40}\n"
                f"🔵 PEA:\n"
                f"  Valeur finale: {pea_result['final_value_net']:,.2f} €\n"
                f"  Gain net: {pea_result['total_gain_net']:,.2f} €\n"
                f"  Impôts payés: {pea_result['tax_paid']:,.2f} €\n"
                f"  CAGR: {pea_result['cagr']:.2f}%\n\n"
                f"🔴 CTO:\n"
                f"  Valeur finale: {cto_result['final_value_net']:,.2f} €\n"
                f"  Gain net: {cto_result['total_gain_net']:,.2f} €\n"
                f"  Impôts payés: {cto_result['tax_paid']:,.2f} €\n"
                f"  CAGR: {cto_result['cagr']:.2f}%\n\n"
                f"📈 DIFFÉRENCES:\n"
                f"  Avantage PEA: {diff_value:,.2f} €\n"
                f"  Gain supplémentaire: {diff_gain:,.2f} €\n"
                f"  Économie fiscale: {diff_tax:,.2f} €\n"
            )
            
            # Créer une fenêtre de résultats
            result_window = tk.Toplevel(self.root)
            result_window.title("Comparaison détaillée PEA/CTO")
            result_window.geometry("500x600")
            
            text_widget = tk.Text(result_window, font=('Courier', 10), wrap=tk.WORD)
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            text_widget.insert(1.0, comparison_text)
            text_widget.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la comparaison:\n{str(e)}")
    
    def get_simulation_params(self):
        """Récupère tous les paramètres de simulation"""
        return {
            'ticker': self.ticker_var.get(),
            'initial_price': self.initial_price_var.get(),
            'initial_investment': self.investment_var.get(),
            'monthly_investment': self.monthly_investment_var.get(),
            'years': self.years_var.get(),
            'annual_return': self.annual_return_var.get(),
            'volatility': self.volatility_var.get(),
            'dividend_yield': self.dividend_yield_var.get(),
            'tax_scenario': self.tax_scenario_var.get(),
            'inflation_rate': self.inflation_rate_var.get()
        }
    
    def update_simple_chart(self):
        """Met à jour le graphique de simulation simple"""
        if not self.simulation_results:
            return
        
        self.ax_simple.clear()
        
        pea_result = self.simulation_results['PEA']
        months = self.years_var.get() * 12
        time_axis = np.arange(months) / 12
        
        # Courbe PEA
        if 'value_history' in pea_result:
            self.ax_simple.plot(time_axis, pea_result['value_history'], 
                              label='PEA', color=self.colors['pea'], linewidth=2)
        
        # Ligne d'investissement total
        self.ax_simple.axhline(y=pea_result['total_invested'], 
                             color='gray', linestyle='--', alpha=0.5,
                             label=f"Investissement: {pea_result['total_invested']:,.0f} €")
        
        # Configuration
        self.ax_simple.set_xlabel("Années")
        self.ax_simple.set_ylabel("Valeur (€)")
        self.ax_simple.set_title(f"Simulation: {self.ticker_var.get()} - {self.years_var.get()} ans")
        self.ax_simple.legend()
        self.ax_simple.grid(True, alpha=0.3)
        
        # Format de l'axe Y
        self.ax_simple.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f} €'))
        
        self.fig_simple.tight_layout()
        self.canvas_simple.draw()
    
    def update_monte_carlo_chart(self):
        """Met à jour le graphique Monte Carlo"""
        if not self.monte_carlo_results:
            return
        
        self.ax_monte.clear()
        
        pea_results = self.monte_carlo_results['pea_results']
        cto_results = self.monte_carlo_results['cto_results']
        
        # Calcul des percentiles
        percentiles = [5, 25, 50, 75, 95]
        pea_percentiles = np.percentile(pea_results, percentiles)
        cto_percentiles = np.percentile(cto_results, percentiles)
        
        # Box plot
        bp_data = [pea_results, cto_results]
        bp = self.ax_monte.boxplot(bp_data, patch_artist=True, labels=['PEA', 'CTO'])
        
        # Couleurs
        bp['boxes'][0].set_facecolor(self.colors['pea'])
        bp['boxes'][1].set_facecolor(self.colors['cto'])
        
        # Configuration
        self.ax_monte.set_ylabel("Valeur finale nette (€)")
        self.ax_monte.set_title("Distribution des résultats - Monte Carlo")
        self.ax_monte.grid(True, alpha=0.3)
        
        # Ajouter des annotations pour les percentiles
        for i, (label, values) in enumerate([('PEA', pea_percentiles), ('CTO', cto_percentiles)]):
            for j, (p, val) in enumerate(zip(percentiles, values)):
                if j == 2:  # Médiane
                    self.ax_monte.text(i + 1, val, f'{val:,.0f} €', 
                                     ha='center', va='bottom', fontweight='bold')
        
        self.fig_monte.tight_layout()
        self.canvas_monte.draw()
    
    def update_comparison_chart(self):
        """Met à jour le graphique de comparaison"""
        if not self.simulation_results:
            return
        
        self.ax_comp.clear()
        
        pea_result = self.simulation_results['PEA']
        cto_result = self.simulation_results['CTO']
        
        # Données pour le graphique à barres
        categories = ['Valeur finale', 'Gain net', 'Impôts payés', 'CAGR']
        pea_values = [
            pea_result['final_value_net'],
            pea_result['total_gain_net'],
            pea_result['tax_paid'],
            pea_result['cagr']
        ]
        cto_values = [
            cto_result['final_value_net'],
            cto_result['total_gain_net'],
            cto_result['tax_paid'],
            cto_result['cagr']
        ]
        
        x = np.arange(len(categories))
        width = 0.35
        
        # Barres
        bars1 = self.ax_comp.bar(x - width/2, pea_values, width, label='PEA', color=self.colors['pea'])
        bars2 = self.ax_comp.bar(x + width/2, cto_values, width, label='CTO', color=self.colors['cto'])
        
        # Configuration
        self.ax_comp.set_xlabel("Métriques")
        self.ax_comp.set_ylabel("Valeur")
        self.ax_comp.set_title("Comparaison PEA vs CTO")
        self.ax_comp.set_xticks(x)
        self.ax_comp.set_xticklabels(categories)
        self.ax_comp.legend()
        self.ax_comp.grid(True, alpha=0.3, axis='y')
        
        # Ajouter les valeurs sur les barres
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                if bar.get_x() < 3:  # Pour les valeurs monétaires
                    self.ax_comp.text(bar.get_x() + bar.get_width()/2., height,
                                    f'{height:,.0f}', ha='center', va='bottom')
                else:  # Pour le CAGR
                    self.ax_comp.text(bar.get_x() + bar.get_width()/2., height,
                                    f'{height:.1f}%', ha='center', va='bottom')
        
        self.fig_comp.tight_layout()
        self.canvas_comp.draw()
    
    def update_distribution_chart(self):
        """Met à jour le graphique de distribution"""
        if not self.monte_carlo_results:
            return
        
        self.ax_dist.clear()
        
        pea_results = self.monte_carlo_results['pea_results']
        
        # Histogramme
        n_bins = min(50, len(pea_results) // 10)
        self.ax_dist.hist(pea_results, bins=n_bins, alpha=0.7, 
                         color=self.colors['chart_1'], edgecolor='black')
        
        # Lignes pour les indicateurs
        mean_val = np.mean(pea_results)
        median_val = np.median(pea_results)
        
        self.ax_dist.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Moyenne: {mean_val:,.0f} €')
        self.ax_dist.axvline(median_val, color='green', linestyle='--', linewidth=2, label=f'Médiane: {median_val:,.0f} €')
        
        # Configuration
        self.ax_dist.set_xlabel("Valeur finale nette (€)")
        self.ax_dist.set_ylabel("Fréquence")
        self.ax_dist.set_title("Distribution des résultats - PEA")
        self.ax_dist.legend()
        self.ax_dist.grid(True, alpha=0.3)
        
        self.fig_dist.tight_layout()
        self.canvas_dist.draw()
    
    def update_results_display(self):
        """Met à jour l'affichage des résultats"""
        if not self.simulation_results or 'PEA' not in self.simulation_results:
            return
        
        result = self.simulation_results['PEA']
        
        # Mise à jour des widgets
        self.results_widgets['final_value'].config(text=f"{result['final_value_net']:,.0f}")
        self.results_widgets['total_gain'].config(text=f"{result['total_gain_net']:,.0f}")
        self.results_widgets['cagr'].config(text=f"{result['cagr']:.2f}")
        
        # Couleurs conditionnelles
        for key in ['final_value', 'total_gain', 'cagr']:
            widget = self.results_widgets[key]
            value = float(widget.cget('text').replace(',', '').replace('%', ''))
            
            if 'cagr' in key:
                if value > 10:
                    widget.config(foreground='green')
                elif value > 5:
                    widget.config(foreground='orange')
                else:
                    widget.config(foreground='red')
            else:
                if value > 0:
                    widget.config(foreground='green')
                else:
                    widget.config(foreground='red')
    
    def update_monte_carlo_results(self):
        """Met à jour les résultats Monte Carlo"""
        if not self.monte_carlo_results:
            return
        
        pea_results = self.monte_carlo_results['pea_results']
        
        # Calcul des statistiques
        mean_val = np.mean(pea_results)
        std_val = np.std(pea_results)
        
        # Sharpe ratio (simplifié)
        risk_free_rate = 2.0  # Taux sans risque estimé
        excess_return = (mean_val / self.investment_var.get()) ** (1/self.years_var.get()) - 1 - risk_free_rate/100
        sharpe_ratio = excess_return / (std_val / mean_val) if std_val > 0 else 0
        
        # VaR 95%
        var_95 = np.percentile(pea_results, 5)
        
        # Probabilité de perte
        initial_investment = self.investment_var.get()
        loss_prob = np.sum(pea_results < initial_investment) / len(pea_results) * 100
        
        # Mise à jour des widgets
        self.results_widgets['sharpe'].config(text=f"{sharpe_ratio:.2f}")
        self.results_widgets['var_95'].config(text=f"{var_95:,.0f}")
        self.results_widgets['loss_prob'].config(text=f"{loss_prob:.1f}")
        
        # Couleurs
        if sharpe_ratio > 1:
            self.results_widgets['sharpe'].config(foreground='green')
        elif sharpe_ratio > 0.5:
            self.results_widgets['sharpe'].config(foreground='orange')
        else:
            self.results_widgets['sharpe'].config(foreground='red')
    
    def generate_report(self):
        """Génère un rapport complet"""
        if not self.simulation_results:
            messagebox.showwarning("Avertissement", "Veuillez d'abord exécuter une simulation")
            return
        
        try:
            # Créer une fenêtre de rapport
            report_window = tk.Toplevel(self.root)
            report_window.title("Rapport de Simulation")
            report_window.geometry("800x600")
            
            # Zone de texte pour le rapport
            text_widget = tk.Text(report_window, font=('Arial', 10), wrap=tk.WORD)
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Générer le contenu du rapport
            report_content = self.create_report_content()
            text_widget.insert(1.0, report_content)
            
            # Boutons d'export
            button_frame = ttk.Frame(report_window)
            button_frame.pack(fill=tk.X, padx=10, pady=5)
            
            ttk.Button(button_frame, text="Exporter en PDF", 
                      command=lambda: self.export_pdf(report_content)).pack(side=tk.LEFT, padx=5)
            
            ttk.Button(button_frame, text="Copier", 
                      command=lambda: self.copy_to_clipboard(report_content)).pack(side=tk.LEFT, padx=5)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la génération du rapport:\n{str(e)}")
    
    def create_report_content(self):
        """Crée le contenu du rapport"""
        if not self.simulation_results:
            return "Aucune donnée disponible."
        
        pea_result = self.simulation_results.get('PEA', {})
        cto_result = self.simulation_results.get('CTO', {})
        
        content = f"""
{'='*70}
RAPPORT DE SIMULATION D'INVESTISSEMENT
{'='*70}

Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Action: {self.ticker_var.get()}
Durée: {self.years_var.get()} ans

{'='*70}
PARAMÈTRES DE SIMULATION
{'='*70}

• Prix initial: {self.initial_price_var.get():.2f} €
• Investissement initial: {self.investment_var.get():,.2f} €
• Investissement mensuel: {self.monthly_investment_var.get():,.2f} €
• Rendement annuel estimé: {self.annual_return_var.get():.1f}%
• Volatilité: {self.volatility_var.get():.1f}%
• Rendement dividende: {self.dividend_yield_var.get():.1f}%
• Scénario fiscal: {self.tax_scenario_var.get()}

{'='*70}
RÉSULTATS DÉTAILLÉS
{'='*70}

[PEA - Plan d'Épargne en Actions]
{'─'*40}
• Valeur finale brute: {pea_result.get('final_value', 0):,.2f} €
• Valeur finale nette: {pea_result.get('final_value_net', 0):,.2f} €
• Gain total brut: {pea_result.get('total_gain', 0):,.2f} €
• Gain total net: {pea_result.get('total_gain_net', 0):,.2f} €
• Impôts payés: {pea_result.get('tax_paid', 0):,.2f} €
• Taux d'imposition: {pea_result.get('tax_rate', 0)*100:.1f}%
• Rendement annualisé (CAGR): {pea_result.get('cagr', 0):.2f}%
• Investissement total: {pea_result.get('total_invested', 0):,.2f} €

[CTO - Compte Titres Ordinaire]
{'─'*40}
• Valeur finale brute: {cto_result.get('final_value', 0):,.2f} €
• Valeur finale nette: {cto_result.get('final_value_net', 0):,.2f} €
• Gain total brut: {cto_result.get('total_gain', 0):,.2f} €
• Gain total net: {cto_result.get('total_gain_net', 0):,.2f} €
• Impôts payés: {cto_result.get('tax_paid', 0):,.2f} €
• Taux d'imposition: {cto_result.get('tax_rate', 0)*100:.1f}%
• Rendement annualisé (CAGR): {cto_result.get('cagr', 0):.2f}%

{'='*70}
ANALYSE COMPARATIVE
{'='*70}

• Avantage PEA vs CTO: {pea_result.get('final_value_net', 0) - cto_result.get('final_value_net', 0):,.2f} €
• Économie fiscale PEA: {cto_result.get('tax_paid', 0) - pea_result.get('tax_paid', 0):,.2f} €
• Différence de rendement: {pea_result.get('cagr', 0) - cto_result.get('cagr', 0):.2f}%

{'='*70}
RECOMMANDATIONS
{'='*70}

"""
        
        # Ajouter des recommandations basées sur les résultats
        pea_cagr = pea_result.get('cagr', 0)
        advantage = pea_result.get('final_value_net', 0) - cto_result.get('final_value_net', 0)
        
        if advantage > 0:
            content += "✅ Le PEA est plus avantageux que le CTO pour cet investissement.\n"
        else:
            content += "⚠️ Le CTO pourrait être plus avantageux dans ce scénario.\n"
        
        if pea_cagr > 10:
            content += "📈 Performance excellente (>10% annuel)\n"
        elif pea_cagr > 5:
            content += "📊 Performance correcte (5-10% annuel)\n"
        else:
            content += "⚠️ Performance modérée (<5% annuel)\n"
        
        if self.years_var.get() >= 5:
            content += "🏦 Durée suffisante pour bénéficier de l'avantage fiscal PEA\n"
        else:
            content += "⏳ Durée insuffisante pour l'avantage fiscal PEA\n"
        
        content += f"\n{'='*70}\n"
        content += "NOTE: Ces résultats sont basés sur des simulations et des hypothèses.\n"
        content += "Les performances passées ne préjugent pas des performances futures.\n"
        content += "Consultez un conseiller financier pour des recommandations personnalisées.\n"
        content += f"{'='*70}\n"
        
        return content
    
    def export_data(self):
        """Exporte les données de simulation"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[
                    ("Fichiers Excel", "*.xlsx"),
                    ("Fichiers CSV", "*.csv"),
                    ("Tous les fichiers", "*.*")
                ],
                initialfile=f"simulation_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )
            
            if filename:
                if filename.endswith('.xlsx'):
                    self.export_to_excel(filename)
                elif filename.endswith('.csv'):
                    self.export_to_csv(filename)
                
                messagebox.showinfo("Succès", f"Données exportées dans:\n{filename}")
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'export:\n{str(e)}")
    
    def export_to_excel(self, filename):
        """Exporte les données vers Excel"""
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Paramètres
            params_df = pd.DataFrame([
                ["Ticker", self.ticker_var.get()],
                ["Prix initial", self.initial_price_var.get()],
                ["Investissement initial", self.investment_var.get()],
                ["Investissement mensuel", self.monthly_investment_var.get()],
                ["Durée", self.years_var.get()],
                ["Rendement annuel", self.annual_return_var.get()],
                ["Volatilité", self.volatility_var.get()],
                ["Dividende", self.dividend_yield_var.get()],
                ["Scénario fiscal", self.tax_scenario_var.get()]
            ], columns=["Paramètre", "Valeur"])
            
            params_df.to_excel(writer, sheet_name='Paramètres', index=False)
            
            # Résultats
            if self.simulation_results:
                results_data = []
                for account, result in self.simulation_results.items():
                    results_data.append({
                        "Compte": account,
                        "Valeur finale nette": result.get('final_value_net', 0),
                        "Gain net": result.get('total_gain_net', 0),
                        "Impôts payés": result.get('tax_paid', 0),
                        "CAGR": result.get('cagr', 0),
                        "Investissement total": result.get('total_invested', 0)
                    })
                
                results_df = pd.DataFrame(results_data)
                results_df.to_excel(writer, sheet_name='Résultats', index=False)
    
    def export_to_csv(self, filename):
        """Exporte les données vers CSV"""
        if self.simulation_results:
            data = []
            for account, result in self.simulation_results.items():
                data.append({
                    "compte": account,
                    "valeur_finale": result.get('final_value_net', 0),
                    "gain_net": result.get('total_gain_net', 0),
                    "impots": result.get('tax_paid', 0),
                    "cagr": result.get('cagr', 0)
                })
            
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False, sep=';')
    
    def export_pdf(self, content):
        """Exporte le rapport en PDF (version simplifiée)"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")],
                initialfile=f"rapport_{datetime.now().strftime('%Y%m%d')}.txt"
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("Succès", f"Rapport exporté dans:\n{filename}")
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'export PDF:\n{str(e)}")
    
    def copy_to_clipboard(self, content):
        """Copie le contenu dans le presse-papier"""
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        messagebox.showinfo("Succès", "Rapport copié dans le presse-papier!")
    
    def reset_all(self):
        """Réinitialise toutes les simulations"""
        self.simulation_results = {}
        self.monte_carlo_results = None
        
        # Réinitialiser les graphiques
        for ax in [self.ax_simple, self.ax_monte, self.ax_comp, self.ax_dist]:
            ax.clear()
            ax.text(0.5, 0.5, "Aucune donnée disponible\n\nExécutez une simulation", 
                   ha='center', va='center', transform=ax.transAxes, fontsize=12, color='gray')
            ax.set_title("")
            ax.set_xticks([])
            ax.set_yticks([])
        
        # Redessiner les canvas
        self.canvas_simple.draw()
        self.canvas_monte.draw()
        self.canvas_comp.draw()
        self.canvas_dist.draw()
        
        # Réinitialiser les résultats
        for widget in self.results_widgets.values():
            widget.config(text="-", foreground='black')
        
        messagebox.showinfo("Réinitialisation", "Toutes les simulations ont été réinitialisées.")
    
    def show_progress(self, title, max_value):
        """Affiche une fenêtre de progression"""
        progress_window = tk.Toplevel(self.root)
        progress_window.title(title)
        progress_window.geometry("300x100")
        progress_window.transient(self.root)
        progress_window.grab_set()
        
        ttk.Label(progress_window, text=title, font=('Arial', 10)).pack(pady=10)
        
        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(progress_window, variable=progress_var, maximum=max_value)
        progress_bar.pack(padx=20, pady=10, fill=tk.X)
        
        progress_window.update_progress = lambda val: progress_var.set(val)
        progress_window.update()
        
        return progress_window

def main():
    """Fonction principale"""
    root = tk.Tk()
    
    # Configuration de la fenêtre
    root.title("Simulateur d'Actions Avancé")
    root.geometry("1400x900")
    
    # Centrer la fenêtre
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 1400
    window_height = 900
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # Créer l'application
    app = AdvancedStockSimulator(root)
    
    # Lancer la boucle principale
    root.mainloop()

if __name__ == "__main__":
    main()