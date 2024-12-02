# Browser Performance Project

## Description
This project automates performance testing of web browsers in the context of different web pages. The following are measured:
- Page load time.
- CPU usage.
- RAM usage.

## Requirements
- Python 3.7+
- Google Chrome, Firefox, Microsoft Edge
- Installed browsers and their WebDriver (e.g. chromedriver, geckodriver)

## Instalation
1. Clone the repository or download the files.
2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the tests:
   ```bash
   python main.py
   ```
4. Webdocker instalation:
- For Chrome: https://googlechromelabs.github.io/chrome-for-testing/#stable
- For Firefox: https://github.com/mozilla/geckodriver/releases
- For Edge: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/?form=MA13LH#downloads
5. If doesn't work
- Delete folder venv and install, by terminal in visual
   ```bash
   python -m venv venv
   ```
## Results
The test results are saved in the `results.csv` file and visualized in the form of graphs.
