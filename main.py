import pandas as pd
from selenium import webdriver
import psutil
import time
import matplotlib.pyplot as plt
import seaborn as sns

# Funkcja monitorująca zasoby
def monitor_resources(pid):
    process = psutil.Process(pid)
    return {
        "cpu": process.cpu_percent(interval=1),
        "memory": process.memory_info().rss / (1024 * 1024)  # Memory in MB
    }

# Funkcja testująca przeglądarkę
def test_browser(url, browser_name):
    if browser_name == "Chrome":
        driver = webdriver.Chrome()
    elif browser_name == "Firefox":
        driver = webdriver.Firefox()
    elif browser_name == "Edge":
        driver = webdriver.Edge()
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
    urls = ['https://www.example.com', 'https://www.google.com']
    browsers = ['Chrome', 'Firefox', 'Edge']
    results = []

    for browser in browsers:
        for url in urls:
            print(f"Testing {url} on {browser}...")
            result = test_browser(url, browser)
            results.append(result)

    return pd.DataFrame(results)

# Generowanie wykresów
def generate_plots(df):
    metrics = ['Load Time (s)', 'CPU Usage (%)', 'Memory Usage (MB)']
    
    for metric in metrics:
        # Filtruj dane dla aktualnej metryki
        df_metric = df[['URL', 'Browser', metric]].copy()
        df_metric = df_metric.rename(columns={metric: 'Value'})
        
        # Tworzenie wykresu dla każdej metryki
        plt.figure(figsize=(10, 6))
        sns.barplot(x='URL', y='Value', hue='Browser', data=df_metric, ci=None)
        plt.title(f'Browser Performance Comparison: {metric}')
        plt.ylabel(metric)
        plt.xlabel('Website')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    results_df = run_tests()
    print(results_df)
    results_df.to_csv('results.csv', index=False)
    generate_plots(results_df)
