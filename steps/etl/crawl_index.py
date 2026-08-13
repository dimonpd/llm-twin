from loguru import logger
from zenml import step

from llm_engineering.application.crawlers.dispatcher import CrawlerDispatcher
from llm_engineering.domain.documents import UserDocument


@step
def crawl_index(user: UserDocument, index_url: str) -> None:
    crawler = (
        CrawlerDispatcher.build()
        .register_slova_org()
        .get_crawler(index_url)
    )
    logger.info(f"Crawling index: {index_url}")
    crawler.extract_from_index(index_url, user=user)
