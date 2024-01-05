# SReality.cz Web Scraper

This is a web scraper specifically designed for extracting information from the real estate website [SReality.cz](https://www.sreality.cz/). The scraper is programmed to retrieve 500 offers from the website and store them in a PostgreSQL database. It captures their titles and links to associated images.

## How to Run the Scraper

To execute the scraper, follow these steps:

1. Ensure you have Docker installed on your machine.
2. Clone this repository.
3. Navigate to the root directory of the repository.
4. Use the command `docker-compose up` to run the scraper.

Upon successful execution, you can view the results by accessing `127.0.0.1:8080` in your web browser.

## Example Result Preview

An example representation of the scraped data should look like this:

![Sample Scraper Result](assets/example.png)