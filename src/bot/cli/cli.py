# Author: Andrei Biswas (@codeabiswas)
# This is a Python command-line tool which requests user to input a Spotify or Apple Music link, and it gets converted to the corresponding streaming service's link.

import requests
from bs4 import BeautifulSoup
import json

def bot_link_conversion(url):
    pass

def link_conversion(url):
    """
        Converts the Apple Music or Spotify link to its corresponding streaming service's link.
        Return: Tuple if successful at producing results/no corresponding link since track is unique to the streaming service, String if no link was found or there was some error.
    """

    # song.link URL
    static_song_link_url = "https://song.link/"

    try:
        # Access the page and Beautiful Soupify TM it
        page = requests.get(static_song_link_url + url)
        soup = BeautifulSoup(page.text, "html.parser")
        elements = soup.find_all("script")[-1]

        # JSON-ify the data for easier parsing
        data = json.loads(elements.text)

        # Acquire list of links
        stream_links = data['props']['pageProps']['pageData']['sections'][1]['links']
        # This is the song.link URL. Share this with the user in case they want links to other streaming platforms as well.
        global_song_link_url = data['props']['pageProps']['pageData']['pageUrl']

        
        for stream_obj in stream_links:
            if "apple" in url.lower():
                print("Finding Spotify link...")
                # Try to get the Spotify URL. If unsuccessful, it likely means that there is no corresponding Spotify URL, like in the case of an Apple Music DJ Mix.
                if stream_obj['displayName'] == 'Spotify':
                    try:
                        return stream_obj['url'], global_song_link_url
                    except Exception as err:
                        return "Sorry, a corresponding link was not found", global_song_link_url
            # If a Spotify URL was shared, convert to Apple Music link
            elif "spotify" in url.lower():
                print("Finding Apple Music link...")
                # Try to get the Apple Music URL. If unsuccessful, it likely means that there is no corresponding Apple Music URL, like in the case of a Spotify single.
                if stream_obj['displayName'] == 'Apple Music':
                    try:
                        return stream_obj['url'], global_song_link_url
                    except Exception as err:
                        return "Sorry, a corresponding link was not found", global_song_link_url

        # No results found
        return "Sorry, a corresponding link was not found."
    
    except Exception as err:
        return "Sorry, there was a problem: {some_error}".format(some_error=err)

def main():
    """
        Main function
    """

    # Get user input
    user_url = input("Share URL: ")

    # Convert the link and show to end user
    return_val = link_conversion(url=user_url)
    if type(return_val) == tuple:
        print("\n\nLink: {stream_link}\nPowered By: {song_link}".format(stream_link=return_val[0], song_link=return_val[1]))
    # Otherwise, inform user about no results.
    else:
        print(return_val)

if __name__ == "__main__":
    main()
