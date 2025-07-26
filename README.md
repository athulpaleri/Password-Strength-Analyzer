Password Strength Analyzer with Custom Wordlist Generator

🔐 A Python-based command-line tool that:
- Analyzes password strength using `zxcvbn-python`
- Generates custom wordlists from user inputs (name, year, etc.)
- Supports leetspeak and year combinations
- Exports the wordlist to `.txt` for use in tools like Hydra or John the Ripper

👨‍💻 Author: Athul P
🏢 Internship: Cybersecurity Research Intern at Elevate Labs (July 2025)

---

🛠️ Tools Used:
- Python 3
- Libraries:
  - zxcvbn-python – For password strength estimation
  - argparse, itertools, datetime, string – For CLI and logic

---

🚀 How to Use:

📦 Install Requirements:
pip install zxcvbn-python

🔍 Analyze a Password:
python password_tool.py analyze -p "MySup3rP@ss!"

🧠 Generate a Wordlist:
python password_tool.py generate -w "athul,2001,shadow" -o wordlist.txt

---

🖼️ Screenshots:

1. Password Strength Analysis – CLI showing score and crack time
2. Wordlist in Notepad – Contents of wordlist.txt
3. Command-Line Wordlist Generator – CLI usage with generate command

(Insert these screenshots in a folder called screenshots/ if uploading to GitHub.)

---

📄 Report:
Password_Analyzer_Report_Athul.pdf

---

✅ Project Status:
✔️ Completed
