BOT_NAME = 'scrapy_sreality'

SPIDER_MODULES = ['scrapy_sreality.spiders']
NEWSPIDER_MODULE = 'scrapy_sreality.spiders'

ROBOTSTXT_OBEY = False

PLAYWRIGHT_LAUNCH_OPTIONS = {"headless": True}

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 100000

ITEM_PIPELINES = {
    'scrapy_sreality.pipelines.ScrapySrealityPipeline': 10,
}

CLOSESPIDER_ITEMCOUNT = 500
