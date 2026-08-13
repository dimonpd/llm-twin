import re

from llm_engineering.application.crawlers import (
    CrawlerDispatcher,
    GithubCrawler,
    LinkedInCrawler,
    MediumCrawler,
)
from llm_engineering.application.crawlers.custom_article import CustomArticleCrawler

URLS = {
    "https://medium.com/@user/article-1": MediumCrawler,
    "https://www.linkedin.com/posts/paul/123": LinkedInCrawler,
    "https://github.com/decodingml/llm-twin": GithubCrawler,
    "https://slova.org.ru/mayakovskiy/": CustomArticleCrawler,
    "https://substack.com/@user/post": CustomArticleCrawler,
}


def test_registration_patterns_match_expected_domains():
    dispatcher = (
        CrawlerDispatcher.build()
        .register_medium()
        .register_linkedin()
        .register_github()
        .register_slova_org()
    )

    patterns = dispatcher._crawlers
    assert len(patterns) == 4, f"expected 4 crawlers, got {len(patterns)}: {list(patterns)}"

    for url, expected_cls in URLS.items():
        matched = [cls for pattern, cls in patterns.items() if re.match(pattern, url)]
        if expected_cls is CustomArticleCrawler and "slova.org.ru" not in url:
            assert not matched, f"{url} matched {matched}, expected fallback"
        else:
            assert matched == [expected_cls], f"{url} matched {matched}, expected {expected_cls}"
