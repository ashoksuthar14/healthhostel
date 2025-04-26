#!/usr/bin/env python3
import os
import sys
import pandas as pd
from datetime import datetime
from colorama import init, Fore, Style
import json

# Initialize colorama for cross-platform colored output
init()

class HealthBot:
    def __init__(self):
        self.health_log_file = "health_log.csv"
        self.symptoms_db_file = "symptoms_db.json"
        self.initialize_files()
        self.load_symptoms_database()

    def initialize_files(self):
        # Initialize health log if it doesn't exist
        if not os.path.exists(self.health_log_file):
            df = pd.DataFrame(columns=['date', 'symptoms', 'severity', 'remedies_suggested'])
            df.to_csv(self.health_log_file, index=False)

        # Initialize symptoms database if it doesn't exist
        if not os.path.exists(self.symptoms_db_file):
            symptoms_db = {
                "fever": {
                    "remedies": ["Rest well", "Stay hydrated", "Take paracetamol if temperature is high"],
                    "severity": "medium",
                    "seek_medical_attention": "If temperature exceeds 102°F or persists for more than 3 days"
                },
                "headache": {
                    "remedies": ["Rest in a quiet, dark room", "Stay hydrated", "Try mild pain relievers"],
                    "severity": "low",
                    "seek_medical_attention": "If severe and persistent for more than 24 hours"
                },
                "cold": {
                    "remedies": ["Rest", "Drink warm fluids", "Steam inhalation"],
                    "severity": "low",
                    "seek_medical_attention": "If symptoms worsen after 7 days"
                },
                "stomach_ache": {
                    "remedies": ["Avoid heavy foods", "Try ginger tea", "Stay hydrated"],
                    "severity": "medium",
                    "seek_medical_attention": "If severe pain or accompanied by vomiting"
                }
            }
            with open(self.symptoms_db_file, 'w') as f:
                json.dump(symptoms_db, f, indent=4)

    def load_symptoms_database(self):
        with open(self.symptoms_db_file, 'r') as f:
            self.symptoms_db = json.load(f)

    def display_menu(self):
        print(f"\n{Fore.CYAN}=== Health Alert Bot ==={Style.RESET_ALL}")
        print("1. Log New Symptoms")
        print("2. View Health History")
        print("3. Get Health Insights")
        print("4. Learn About Seasonal Illnesses")
        print("5. Exit")
        return input("\nChoose an option (1-5): ")

    def log_symptoms(self):
        print(f"\n{Fore.YELLOW}Available Symptoms:{Style.RESET_ALL}")
        for i, symptom in enumerate(self.symptoms_db.keys(), 1):
            print(f"{i}. {symptom}")
        
        try:
            choice = int(input("\nEnter symptom number: "))
            symptom = list(self.symptoms_db.keys())[choice-1]
        except (ValueError, IndexError):
            print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
            return

        severity = input("Rate severity (1-5, where 5 is most severe): ")
        
        # Get remedies for the symptom
        remedies = self.symptoms_db[symptom]["remedies"]
        medical_attention = self.symptoms_db[symptom]["seek_medical_attention"]

        # Log the symptom
        df = pd.read_csv(self.health_log_file)
        new_entry = {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'symptoms': symptom,
            'severity': severity,
            'remedies_suggested': '; '.join(remedies)
        }
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(self.health_log_file, index=False)

        # Display advice
        print(f"\n{Fore.GREEN}Suggested Remedies:{Style.RESET_ALL}")
        for remedy in remedies:
            print(f"- {remedy}")
        
        if int(severity) >= 4:
            print(f"\n{Fore.RED}⚠️ MEDICAL ATTENTION ADVISED:{Style.RESET_ALL}")
            print(medical_attention)

    def view_history(self):
        if not os.path.exists(self.health_log_file):
            print(f"{Fore.RED}No health history found.{Style.RESET_ALL}")
            return

        df = pd.read_csv(self.health_log_file)
        if df.empty:
            print(f"{Fore.YELLOW}No entries in health log yet.{Style.RESET_ALL}")
            return

        print(f"\n{Fore.CYAN}Your Health History:{Style.RESET_ALL}")
        print(df.to_string(index=False))

    def get_insights(self):
        if not os.path.exists(self.health_log_file):
            print(f"{Fore.RED}No data available for insights.{Style.RESET_ALL}")
            return

        df = pd.read_csv(self.health_log_file)
        if df.empty:
            print(f"{Fore.YELLOW}No entries to analyze yet.{Style.RESET_ALL}")
            return

        print(f"\n{Fore.CYAN}Health Insights:{Style.RESET_ALL}")
        
        # Most common symptoms
        common_symptoms = df['symptoms'].value_counts()
        print("\nMost Common Symptoms:")
        for symptom, count in common_symptoms.items():
            print(f"- {symptom}: {count} times")

        # Average severity by symptom
        avg_severity = df.groupby('symptoms')['severity'].mean()
        print("\nAverage Severity by Symptom:")
        for symptom, severity in avg_severity.items():
            print(f"- {symptom}: {severity:.1f}/5")

    def seasonal_illnesses(self):
        print(f"\n{Fore.CYAN}Common Seasonal Illnesses:{Style.RESET_ALL}")
        seasonal_info = {
            "Winter": ["Common Cold", "Flu", "Sore Throat"],
            "Summer": ["Heat Exhaustion", "Food Poisoning", "Dehydration"],
            "Monsoon": ["Viral Fever", "Dengue", "Respiratory Infections"]
        }

        for season, illnesses in seasonal_info.items():
            print(f"\n{Fore.YELLOW}{season}:{Style.RESET_ALL}")
            for illness in illnesses:
                print(f"- {illness}")

    def run(self):
        while True:
            choice = self.display_menu()
            
            if choice == '1':
                self.log_symptoms()
            elif choice == '2':
                self.view_history()
            elif choice == '3':
                self.get_insights()
            elif choice == '4':
                self.seasonal_illnesses()
            elif choice == '5':
                print(f"\n{Fore.GREEN}Take care! Goodbye!{Style.RESET_ALL}")
                sys.exit(0)
            else:
                print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")

            input("\nPress Enter to continue...")

if __name__ == "__main__":
    bot = HealthBot()
    bot.run() 