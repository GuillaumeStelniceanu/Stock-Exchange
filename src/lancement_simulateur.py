#!/usr/bin/env python3
"""
Script de lancement du simulateur d'actions
"""

import subprocess
import sys
import os

def check_requirements():
    """Vérifie et installe les dépendances"""
    requirements = [
        "numpy",
        "pandas", 
        "matplotlib",
        "yfinance"
    ]
    
    print("🔍 Vérification des dépendances...")
    
    for package in requirements:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package} est installé")
        except ImportError:
            print(f"⚠️  {package} n'est pas installé")
            install = input(f"Installer {package}? (o/n): ")
            if install.lower() == 'o':
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ {package} installé avec succès")
    
    print("\n✅ Toutes les dépendances sont vérifiées!")

def main():
    """Fonction principale"""
    print("=" * 50)
    print("SIMULATEUR D'INVESTISSEMENT ACTIONS")
    print("=" * 50)
    print("\nChoisissez le simulateur à lancer:")
    print("1. Simulateur Simple (recommandé)")
    print("2. Simulateur Avancé (Monte Carlo)")
    print("3. Quitter")
    
    choice = input("\nVotre choix (1-3): ")
    
    if choice == "1":
        print("\n🚀 Lancement du simulateur simple...")
        from simulateur_actions import main as run_simple
        run_simple()
    elif choice == "2":
        print("\n🚀 Lancement du simulateur avancé...")
        from simulateur_actions_avance import main as run_advanced
        run_advanced()
    elif choice == "3":
        print("\n👋 Au revoir!")
        sys.exit(0)
    else:
        print("\n❌ Choix invalide!")
        main()

if __name__ == "__main__":
    # Vérifier les dépendances au premier lancement
    if not os.path.exists(".deps_checked"):
        check_requirements()
        open(".deps_checked", "w").close()
    
    main()