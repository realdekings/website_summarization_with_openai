import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
from openai import OpenAI

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    print('No API key was found - please check if you are accessing the key')
elif api_key[:8]!= 'sk-proj-':
    print('An API key was found, it did not start with sk-proj-; please check that you are suing the right api key')
elif api_key.strip() != api_key:
    print('An API KEY was found, but it might contain spaces, tab at th start or the end')
else:
    print('API KEY found and looks good')


openai = OpenAI()

class Website:
    """
    This is a utility class representing a website and will be used to scrape the content of any 
    website it is given
    """
    url: str
    title: str
    text: str


    def __init__(self, url):
        """
        Create this website object from the given url using beautifulSoup library
        """
        self.url = url
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else 'No title found'
        for irrelevant in soup.body(['script', 'style', 'img', 'input']):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator='\n', strip=True)


# Define system prompt 

system_prompt = "You are an assistant that analyzes the content of a website \
and provide a short summary, ignoring text that might be navigation related. \
Respond in markdown"

# A function that write a User prompt that asks for summaries of websites

def user_prompt(website):
    prompt = f"You are looking at a website titled {website.title}"
    prompt += "\nThe content of this website is as follows: \
    please provide a short summary of this website in markdown. \
    Please also explain in your summary who their primary target are and their competitor"
    prompt += website.text
    return prompt


def message_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt(website)}
    ]




# Call OPENAI API

def summarize(url):
    website = Website(url)
    response = openai.chat.completions.create(
        model = "gpt-4o-mini",
        messages = message_for(website)
    )
    return response.choices[0].message.content


def display_summary(url):
    summary = summarize(url)
    print(f"Summary for {url}:\n")
    print(summary)
    # display(Markdown(summary))


if __name__ == "__main__":
    url = "https://dataforest.ai/"
    display_summary(url)
