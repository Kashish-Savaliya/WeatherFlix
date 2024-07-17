from newsapi import NewsApiClient
import requests

newsapi = NewsApiClient(api_key='2205442c75e0447d81857465256695a0')

def get_sources_and_domains():
    # Get all sources
    all_sources = newsapi.get_sources()['sources']

    # Extract sources and domains
    sources = []
    domains = []

    for source in all_sources:
        id = source['id']
        domain = source['url'].replace("http://", "").replace("https://", "").replace("www.", "")
        slash = domain.find('/')
        if slash != -1:
            domain = domain[:slash]
        sources.append(id)
        domains.append(domain)

    # Convert lists to comma-separated strings
    sources_str = ", ".join(sources)
    domains_str = ", ".join(domains)

    return sources_str, domains_str


