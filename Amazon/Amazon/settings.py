# -*- coding: utf-8 -*-

BOT_NAME = 'Amazon'

SPIDER_MODULES = ['Amazon.spiders']
NEWSPIDER_MODULE = 'Amazon.spiders'

USER_AGENT = "Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
              '*/*;q=0.8',
    'Accept-Language': 'en',
    'User-Agent': USER_AGENT,
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'Amazon.middlewares.AmazonSpiderMiddleware': 543,
#    'Amazon.middlewares.RandomUserAgentMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'Amazon.middlewares.RandomUserAgent': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'Amazon.pipelines.AmazonGoodsPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

COOKIES = {'session-id-time': '2082787201l', 'i18n-prefs': 'USD',
           'session-id': '142-9723185-7096359', 'csm-hit': 'tb:s-TBNBSGGG2DTDACWFT2JG|1572104186431&t:1572104193942&adb:adblk_yes', 'sp-cdn': '"L5Z9:CN"', 'session-token': 'NtXSk4TNeLL1ywfKV+TvuhmxatgSa0yrUMVDxOzt0g6CAMeI6LkpgnQrcoU1asoE+pKF7ldrZnErq1dycNPGtszkRh03Wmo07Omhxs4OsROir2zQn4T5AtJAkn+RqVL8XB6izSJHsI0OWrp6to8bsr9AAw/4tLCFpEsnIh7nzYE0aDnZRQdyKCRbZbIxQTZg42jrFYHQH21c0ePPk9d0oC3feWEYOqh5KmCr5RWv8+xnCTX7kqpCELI9Qbsz1VKR', 'ubid-main': '135-5055030-7258235', 'x-wl-uid': '1iBt/JjYEoFYF+hGe2aCjWjyE0SGZ8B4QyX2KaTJl47LFamTRWYPbh4mcm/D2kLypor/oEsLBxqI', 'lc-main': 'zh_CN'}
