import requests
from bs4 import BeautifulSoup


OLLAMA_API = "http://localhost:11434/api/chat/"
HEADERS = {"Content-Type": "application/json"}
MODEL = "llama3.2"

# messages = [
#     {"role": "user", "content": "Describe some of the business applications of Gen AI"}
# ]



# response = requests.post(OLLAMA_API, headers=HEADERS, json=payload)
# print(response.json()['message']['content'])



# response = ollama.chat(model=MODEL, messages=messages)
# print(response['message']['content'])


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
    print(website)
    prompt += website
    return prompt


messages = [
        {"role": "user", "content": user_prompt("https://dataforest.ai/")}
]



payload = {
"model": MODEL,
"messages": messages,
"stream": False
}
response = requests.post(OLLAMA_API, headers=HEADERS, json=payload)
print(response.json()['message']['content'])

# def display_summary(url):
#     summary = summarize(url)
#     print(f"Summary for {url}:\n")
#     print(summary)
#     # display(Markdown(summary))


# if __name__ == "__main__":
#     url = "https://primlytics.com/"
#     display_summary(url)