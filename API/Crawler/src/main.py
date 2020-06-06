# Instantiates and runs the Crawler

from Classes import scraper as scp

def run_crawler():
    """ Instantiate crawler and test connection """
    crawler = scp.Crawler()
    # crawler.testConnection()
    crawler.requestOnPage(22)
    crawler.organiseFiles()

def main():
    run_crawler()

if __name__ == "__main__":
    main()