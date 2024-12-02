import pandas as pd
pd.options.display.float_format = '{:.4f}'.format  
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
import psutil
import time
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# Ścieżki do WebDriver
CHROME_DRIVER_PATH = "E:\WebDrivers\chromedriver.exe"
FIREFOX_DRIVER_PATH = "E:\WebDrivers\geckodriver.exe"
EDGE_DRIVER_PATH = "E:\WebDrivers\msedgedriver.exe "

# Funkcja monitorująca zasoby
def monitor_resources(pid):
    process = psutil.Process(pid)
    return {
        "cpu": round(process.cpu_percent(interval=1), 4),
        "memory": process.memory_info().rss / (1024 * 1024)  # Memory in MB
    }

# Funkcja testująca przeglądarkę
def test_browser(url, browser_name):
    if browser_name == "Chrome":
        driver = webdriver.Chrome(service=ChromeService(CHROME_DRIVER_PATH))
    elif browser_name == "Firefox":
        driver = webdriver.Firefox(service=FirefoxService(FIREFOX_DRIVER_PATH))
    elif browser_name == "Edge":
        driver = webdriver.Edge(service=EdgeService(EDGE_DRIVER_PATH))
    else:
        raise ValueError("Unsupported browser")
    
    start_time = time.time()
    driver.get(url)
    load_time = time.time() - start_time

    resources = monitor_resources(driver.service.process.pid)
    driver.quit()

    return {
        "URL": url,
        "Browser": browser_name,
        "Load Time (s)": load_time,
        "CPU Usage (%)": resources["cpu"],
        "Memory Usage (MB)": resources["memory"]
    }

# Główna funkcja do przeprowadzania testów
def run_tests():
    # Strony do testowania
    urls = {
        'Wikipedia': 'https://www.wikipedia.org',
        'Google Maps': 'https://www.google.com/maps',
        'YouTube': 'https://www.youtube.com',
        'Facebook': 'https://www.facebook.com'
    }
    browsers = ['Chrome', 'Firefox', 'Edge']
    results = []

    for browser in browsers:
        for site_name, url in urls.items():
            print(f"Testing {site_name} ({url}) on {browser}...")
            try:
                result = test_browser(url, browser)
                results.append(result)
            except Exception as e:
                print(f"Error testing {site_name} on {browser}: {e}")

    return pd.DataFrame(results)

# Generowanie wykresów
def generate_plots(df):
    metrics = ['Load Time (s)', 'CPU Usage (%)', 'Memory Usage (MB)']
    
    for metric in metrics:
        # Filtruj dane dla aktualnej metryki
        df_metric = df[['URL', 'Browser', metric]].copy()
        df_metric = df_metric.rename(columns={metric: 'Value'})
        
        # Tworzenie wykresu dla każdej metryki
        ax = sns.barplot(x='URL', y='Value', hue='Browser', data=df_metric, errorbar=None)
        ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.4f'))
        plt.figure(figsize=(10, 6))
        sns.barplot(x='URL', y='Value', hue='Browser', data=df_metric, errorbar=None)
        plt.title(f'Browser Performance Comparison: {metric}')
        plt.ylabel(metric)
        plt.xlabel('Website')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    results_df = run_tests()
    results_df = results_df.round(4)  
    print(results_df)
    results_df.to_csv('results.csv', index=False, float_format='%.4f') 
    generate_plots(results_df)
