import requests
from collections import Counter
import tkinter as tk
from tkinter import messagebox

# Configurações
CLIENT_ID = 'sua_client_id'
CLIENT_SECRET = 'seu_client_secret'
REDIRECT_URI = 'sua_redirect_uri'

def get_access_token(authorization_code):
    url = 'https://www.linkedin.com/oauth/v2/accessToken'
    payload = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(url, data=payload)
    return response.json().get('access_token')

def get_profile_data(access_token):
    url = 'https://api.linkedin.com/v2/me'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    return response.json()

def get_job_descriptions():
    return [
        'Desenvolvedor Python, com experiência em Django e Flask.',
        'Desenvolvedor Java com conhecimento em Spring.',
        'Engenheiro de Software com habilidades em machine learning.'
    ]

def extract_keywords(job_descriptions):
    words = []
    for description in job_descriptions:
        words.extend(description.split())
    word_counts = Counter(words)
    return word_counts.most_common(10)

def suggest_optimizations(profile, keywords):
    suggestions = []
    summary = profile.get('headline', '')
    
    for keyword in keywords:
        if keyword[0].lower() not in summary.lower():
            suggestions.append(f"Adicione a palavra-chave '{keyword[0]}' ao seu título.")
    
    return suggestions

class LinkedInOptimizerApp:
    def __init__(self, master):
        self.master = master
        master.title("LinkedIn Profile Optimizer")

        self.label = tk.Label(master, text="Insira seu código de autorização:")
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.optimize_button = tk.Button(master, text="Otimizar Perfil", command=self.optimize_profile)
        self.optimize_button.pack()

        self.results_label = tk.Label(master, text="")
        self.results_label.pack()

    def optimize_profile(self):
        authorization_code = self.entry.get()
        access_token = get_access_token(authorization_code)

        if not access_token:
            messagebox.showerror("Erro", "Falha ao obter token de acesso.")
            return

        profile_data = get_profile_data(access_token)
        job_descriptions = get_job_descriptions()
        keywords = extract_keywords(job_descriptions)
        suggestions = suggest_optimizations(profile_data, keywords)

        if suggestions:
            self.results_label.config(text="\n".join(suggestions))
        else:
            self.results_label.config(text="Seu perfil está otimizado!")

if __name__ == "__main__":
    root = tk.Tk()
    app = LinkedInOptimizerApp(root)
    root.mainloop()
