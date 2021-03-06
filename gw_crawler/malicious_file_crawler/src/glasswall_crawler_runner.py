""" Main class for initializing and running crawlers. """
import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from scrapy.exceptions import CloseSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from src.utils.read_config import ConfigReader

logging.basicConfig(filename="testdata_scrapper.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger()


class GlassWallRunner(object):
    """ Initialize crawler with project settings """

    def __init__(self, *spidercfg):
        settings_file_path = "malicious_file_crawler.src.settings"
        os.environ.setdefault("SCRAPY_SETTINGS_MODULE", settings_file_path)
        settings = get_project_settings()  # Scrapy settings
        # settings['JOBDIR'] = settings.get('JOB_DIR')
        # self.extra_settings = {'JOBDIR': settings.get('JOB_DIR')}
        self.process = CrawlerProcess(settings=settings)
        self.spidercfg = spidercfg

    """ Get all the sites to crawl from config file """

    def get_sites_to_run(self, scrape_site=None):
        if scrape_site is None:
            section = "SCRAPE_SITE"
            section = os.environ['SCRAPE_SITES']
            try:
                # config_obj = ConfigReader(section).read_config()
                sites_arr = section.split(',')
                print(sites_arr)
            except KeyError as ke:
                logger.error(ke)
                raise CloseSpider(reason="Error while getting site list from config.")

        else:
            sites_arr = scrape_site.split(",")
        site_cfg = {}

        # construct site_cfg dictionary: {site_name: site_cfg}
        for site in sites_arr:
            try:
                cfg = ConfigReader(site.upper()).read_config()
                site_cfg[site] = cfg
            except KeyError as ke:
                logger.error(ke)
                raise CloseSpider
        return site_cfg

    """ Instantiate crawler for every site with respective configuration, start crawler engine """

    def run_spiders(self, cfg, data=None):
        logger.info(f"GlassWallRunner:run_spiders:: Spider is {cfg.get('name')}")
        spider = cfg.get('name')
        self.process.crawl(spider, config=cfg, data=data)

    def main(self, site_arr):
        for site, cfg in site_arr.items():
            """ run crawler for every site and get response list """
            self.run_spiders(cfg)

        # the script will block here until crawling is finished
        self.process.start()


if __name__ == '__main__':

    scraper = GlassWallRunner()

    """ get site list and corresponding config into a dictionary """
    if len(sys.argv) == 2:
        scrape_site = sys.argv[1]
        site_list = scraper.get_sites_to_run(scrape_site=scrape_site)

    else:
        site_list = scraper.get_sites_to_run()

    scraper.main(site_list)
