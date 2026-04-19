import os
import subprocess
import shutil

def try_clone_repo():
    repo_url = "https://github.com/malin-radek/project_zero.git"
    try:
        print("Próba pobrania plików z repozytorium...")
        subprocess.run(["git", "clone", repo_url, "_tmp_project_zero"], check=True)
        print("Repozytorium pobrane.")
        return True
    except Exception as e:
        print(f"Nie udało się pobrać repozytorium: {e}")
        return False

def ask_yes_no(question):
    try:
        return input(question + " [t/n]: ").strip().lower() == 't'
    except Exception:
        return False

def main():
    project_name = os.path.basename(os.getcwd())
    print(f"Tworzenie struktury projektu: {project_name}")

    if try_clone_repo():
        print("Kopiowanie plików z repozytorium...")
        # Sprawdź czy repozytorium jest puste
                # Sprawdź czy repozytorium zawiera pliki inne niż .git
        entries = [e.name for e in os.scandir('_tmp_project_zero') if e.name != '.git']
        if not entries:
            print("Repozytorium jest puste. Tworzę lokalną strukturę jako fallback...")
            shutil.rmtree("_tmp_project_zero", ignore_errors=True)
        else:
            # Fallback dla brakujących plików
            fallback_files = {
                "README.md": f"# {project_name}\n\nProjekt oparty o Python (Flask), frontend (nginx), TinyDB.\n",
                os.path.join(".github", "copilot-instructions.md"): "Instrukcje dla Copilota dotyczące tego projektu.\n\nKażda odpowiedź powinna kończyć się cytatem Homera Simpsona.\n\nZawsze twórz dodatkowy plik z instrukcjami (np. .github/copilot-learned.md). Dodawaj tam automatycznie wszystkie rzeczy, których uczysz się podczas pracy nad projektem. Jeśli jakaś komenda lub rozwiązanie nie działa (np. użycie 'heredoc' w PowerShell), wpisz w tym pliku ostrzeżenie, np. 'nie używaj heredoc'. Dany błąd może być popełniony tylko raz.\n",
                os.path.join(".github", "copilot-learned.md"): "# Plik automatycznie uzupełniany przez Copilota\n\n- Nie używaj heredoc w PowerShell – nie działa.\n",
                os.path.join("src", "app.py"): "",
                os.path.join("src", "db.py"): "",
                os.path.join("frontend", "nginx.conf"): "",
                os.path.join("tests", "test_app.py"): ""
            }
            for file, content in fallback_files.items():
                if not os.path.exists(file):
                    dir_path = os.path.dirname(file)
                    if dir_path and not os.path.exists(dir_path):
                        os.makedirs(dir_path, exist_ok=True)
                    with open(file, "w", encoding="utf-8") as f:
                        f.write(content)
            print("Uzupełniono brakujące pliki lokalnymi szablonami.")
            shutil.rmtree("_tmp_project_zero", ignore_errors=True)

    # Inicjalizacja gita
    did_git = False
    did_remote = False

    # ... (cała logika tworzenia plików i katalogów powyżej)

    # Inicjalizacja gita na końcu
    if ask_yes_no("Czy zainicjować repozytorium git w tym projekcie?"):
        subprocess.run(["git", "init"], check=False)
        did_git = True
        if ask_yes_no("Czy powiązać z remote na GitHub?"):
            remote_input = input("Podaj pełny adres repozytorium (https://github.com/uzytkownik/repo.git) lub nazwę (uzytkownik/repo): ").strip()
            if remote_input:
                if remote_input.startswith("http"):
                    remote_url = remote_input
                elif "/" in remote_input:
                    remote_url = f"https://github.com/{remote_input}.git"
                else:
                    print("Nieprawidłowy format. Podaj pełny adres lub nazwę w formacie uzytkownik/repo.")
                    return
                # Sprawdzenie czy repo istnieje
                import urllib.request
                try:
                    with urllib.request.urlopen(remote_url.replace('.git','')) as resp:
                        if resp.status != 200:
                            raise Exception()
                    subprocess.run(["git", "remote", "add", "origin", remote_url], check=False)
                    print(f"Dodano remote origin: {remote_url}")
                    did_remote = True
                except Exception:
                    print(f"Repozytorium {remote_url} nie istnieje.")
                    print("Utwórz repozytorium na GitHub, np. przez stronę: https://github.com/new")
    # Automatyczny commit i push
    if did_git:
        subprocess.run(["git", "add", "."], check=False)
        subprocess.run(["git", "commit", "-m", "Initial commit"], check=False)
        if did_remote:
            subprocess.run(["git", "push", "-u", "origin", "master"], check=False)


    folders = [
        "src",
        "frontend",
        "tests",
        ".github"
    ]
    files = [
        "README.md",
        os.path.join(".github", "copilot-instructions.md"),
        os.path.join("src", "app.py"),
        os.path.join("src", "db.py"),
        os.path.join("frontend", "nginx.conf"),
        os.path.join("tests", "test_app.py")
    ]

    for folder in folders:
        os.makedirs(folder, exist_ok=True)

    for file in files:
        dir_path = os.path.dirname(file)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        with open(file, "w", encoding="utf-8") as f:
            pass

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(f"# {project_name}\n\nProjekt oparty o Python (Flask), frontend (nginx), TinyDB.\n")

    with open(os.path.join(".github", "copilot-instructions.md"), "w", encoding="utf-8") as f:
        f.write("Instrukcje dla Copilota dotyczące tego projektu.\n\nKażda odpowiedź powinna kończyć się cytatem Homera Simpsona.\n\nZawsze twórz dodatkowy plik z instrukcjami (np. .github/copilot-learned.md). Dodawaj tam automatycznie wszystkie rzeczy, których uczysz się podczas pracy nad projektem. Jeśli jakaś komenda lub rozwiązanie nie działa (np. użycie 'heredoc' w PowerShell), wpisz w tym pliku ostrzeżenie, np. 'nie używaj heredoc'. Dany błąd może być popełniony tylko raz.\n")
    with open(os.path.join(".github", "copilot-learned.md"), "w", encoding="utf-8") as f:
        f.write("# Plik automatycznie uzupełniany przez Copilota\n\n- Nie używaj heredoc w PowerShell – nie działa.\n")

if __name__ == "__main__":
    main()
