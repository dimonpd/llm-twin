from zenml import pipeline

from steps.etl import crawl_index, get_or_create_user


@pipeline
def mayakovsky_etl(user_full_name: str, index_url: str) -> None:
    user = get_or_create_user(user_full_name)
    crawl_index(user=user, index_url=index_url)
