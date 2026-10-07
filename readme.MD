# Books to Scrape — Web Data Acquisition

## Project Description

A practical web data acquisition project built around Books to Scrape. The project demonstrates how to design a reliable scraper incrementally, starting with simple server-rendered HTML and progressively introducing concepts used in production web data acquisition systems.

The focus is not simply on extracting data, but on understanding the architecture and engineering decisions involved in acquiring data reliably from the web.

## Objective

Build a system that:

- Acquires the available book catalog from the website.
- Extracts structured book information from HTML.
- Handles pagination dynamically.
- Stores the acquired data in JSON for downstream use.
- Handles common HTTP and pagination failures safely.
- Provides a foundation that can be extended as more complex web-rendering mechanisms are introduced.
- Current Scope

For each book, the scraper currently extracts:

- title
- price
- rating
- availability
- image
- link

The scraper follows the website's next pagination link rather than relying on a hardcoded number of pages.

## Architecture

1. Website
   ↓
2. HTTP Session
   ↓
3. Request / Response Handling
   ↓
4. HTML Validation
   ↓
5. BeautifulSoup
   ↓
6. Page Extraction
   ↓
7. Pagination
   ↓
8. Collected Records
   ↓
9. JSON

The scraper separates HTTP acquisition, HTML parsing, data extraction, pagination, and persistence into distinct responsibilities.

## Reliability Features

The HTTP layer currently includes:

- Persistent requests.Session
- Request timeout
- User-Agent headers
- HTTP status handling
- Retryable vs. non-retryable status codes
- Handling of 429 Too Many Requests
- Retry-After support
- Basic retry/backoff strategy
- Network exception handling
- Proactive request pacing

## Status

### Level 0 — Server-rendered HTML acquisition: Complete

The scraper successfully acquires the available book catalog, follows pagination dynamically, handles common request failures, prevents pagination loops, and persists the resulting records as JSON.

The next stages will build on this foundation rather than replacing it.