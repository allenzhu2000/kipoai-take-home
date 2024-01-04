README.md

# Backend Take-Home Question 

## Task description

This repo contains just the front-end portion of a very simple web app in which a user can search for parts. Your task is to build the backend required for this web app to function. 

The key tasks are:
1. Build a database by scraping 1,000 datasheets from Mouser. 
2. Extract basic information from the datasheets so that the user can search for a datasheet. Keep it simple. Index the datasheets appropriately. 
3. Design a search tool that uses an LLM to select a part from the database. 

You can use any existing libraries to accomplish this task. Feel free to use any external tools or resources (ChatGPT, StackOverflow, etc.). Please ping Arjun with any questions if you get stuck. You should aim to spend about 4 hours on this task. 

## 1. Scraping

Scrape up to 1,000 datasheets from [Mouser's circular connectors](https://www.mouser.com/c/connectors/circular-connectors/circular-mil-spec-connectors/). You can use any tools or libraries you want, but we recommend [Playwright](https://playwright.dev/) to get around Mouser's anti-scraping measures.

You don't have to design around this consideration, but if this were used in production, how would you design it? What if we had to scrape 1M datasheets on a regular basis? Write your thoughts here:

- Dedicate multiple machines to scraping. Have each of these machines run parallel processes
- Orchestration system to generate continuous scraping tasks and allocate each task to a process
- Database to keep track of the sites that we have scraped and alerts if a particular site has not been scraped in the past X amount of time
- Service to rotate proxies and headless browsers to avoid anti-scraping measures


## 2. Indexing

Retrieve enough information about the datasheet, and the metadata retrieved from scraping, to allow users to search for the part. Choose an appropriate database to store this data. Design it as you see fit, and keep it basic. 

## 3. Search

Build a backend with whatever tools and frameworks you are comfortable in (Python frameworks preferred if all else is equal). The user interface is defined in `substitute.html` and already includes a search bar and a way to display a table of parts, but feel free to edit this code if you'd like. Your backend should take the user's query, use it to retrieve some datasheets/parts, and show some of the relevant data in the table. 

Use an LLM to assist with searching the database for matching parts. There are unlimited ways to do this - we're not looking for a specific solution. Consider how this might help a user find a part as naturally and quickly as possible, and feel free to get creative. You can use the OpenAI API for this - you will be limited to $10 of API calls, which should be sufficient for this task. 

## Submitting, logistics, and evaluation

- To use the OpenAI API, use the organization key "org-pG18N9kBRPkp3ogbR6AYphvb". The API key will be provided to you via email. See [here](https://platform.openai.com/docs/api-reference/authentication) for more details on authentication.
- Please reach out to Arjun with any questions you might have. I would be surprised if you had no questions - so don't hesitate to ask! 
- You can use any existing tools or libraries you want. How well you can build on existing tools is a relevant part of our evaluation.

When you're done, share your code via email arjun@kipo.ai, a link to a private Github repo, or another method.
- Please include a short description of the relevant features of your approach. 
- Please include a requirements.txt file with the libraries you used, or any special instructions for running your code.
- Make sure that your solution works and can be demonstrated on a live video call via screenshare. 

Evaluation: In descending order of importance, we will evaluate (a) the functionality and breadth of your solution; (b) the reasoning behind the design choices you make around scraping, databases, indexing, and search; (c) how adeptly you use existing tools and libraries; (d) the quality of your code and its documentation. 

### Bonus

Don't bother with this unless you have time to spare - but if you do, write a simple unit test for one of the functions you wrote. Don't worry about coverage - we are looking to see how you would approach writing a test.