# About 

This tool will scrape the netgear cable modem "Cable Connection" page and will return the data in the "Downstream Bonded Channels" section as a json file. 

I used it to monitor my channels since I had a pretty bad cable connection.

Since the "Cable Connection" page is rendered using javascript, it's using QT4 WebKit to render the page and does the scraping.

QT4 libraries requires X11 (XOrg). If you want to run this on console you have to install something like: xvfb-run 

From xvfb-run man page:
>       xvfb-run is a wrapper for the Xvfb(1x)  command  which  simplifies  the
>       task of running commands (typically an X client, or a script containing
>       a list of clients to be run) within a virtual X server environment. 

# Installation

TBW

I will add more doc soon.

