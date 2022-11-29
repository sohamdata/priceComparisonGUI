

from tkinter import *
from bs4 import BeautifulSoup
from matplotlib.pyplot import plot
import requests
from difflib import get_close_matches
import webbrowser
from collections import defaultdict
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# import random

root = Tk()
root.geometry("320x150")


class Price_compare:

    def __init__(self, master):

        self.var = StringVar()
        # self.var_ebay = StringVar()
        self.var_flipkart = StringVar()
        self.var_amazon = StringVar()

        label = Label(master, text='Enter the product:')
        label.grid(row=0, column=0, padx=(30, 10), pady=30)

        entry = Entry(master, textvariable=self.var)
        entry.grid(row=0, column=1)

        button_find = Button(master, text='Find', bd=4, command=self.find)
        button_find.grid(row=1, column=1, sticky=W, pady=8)

    def find(self):
        self.product = self.var.get()
        self.product_arr = self.product.split()
        self.n = 1
        self.key = ""
        self.title_flipkart = StringVar()
        self.title_amazon_var = StringVar()
        self.variable_amazon = StringVar()
        self.variable_flipkart = StringVar()

        for word in self.product_arr:
            if self.n == 1:
                self.key = self.key + str(word)
                self.n += 1

            else:
                self.key = self.key + '+' + str(word)

        self.window = Toplevel(root)
        self.window.title('Price Comparison Engine')
        flipkart_title = Label(self.window, text='Flipkart')
        flipkart_title.grid(row=0, column=0, sticky=W)

        flipkart_price = Label(self.window, text='Flipkart price: Rs')
        flipkart_price.grid(row=1, column=0, sticky=W)

        entry_flipkart = Entry(self.window, textvariable=self.var_flipkart)
        entry_flipkart.grid(row=1, column=1, sticky=W)

        amazon_title = Label(self.window, text='Amazon')
        amazon_title.grid(row=3, column=0, sticky=W)

        amazon_price = Label(self.window, text='Amazon price: Rs')
        amazon_price.grid(row=4, column=0, sticky=W)

        entry_amazon = Entry(self.window, textvariable=self.var_amazon)
        entry_amazon.grid(row=4, column=1, sticky=W)

        button_search = Button(self.window, text='Search',
                               command=self.search, bd=4)
        button_search.grid(row=5, column=1, sticky=W, pady=10)

        self.price_flipkart(self.key)
        self.price_amazon(self.key)

        try:
            self.variable_amazon.set(self.matches_amazon[0])
        except:
            self.variable_amazon.set('Product not available')
        try:
            self.variable_flipkart.set(self.matches_flip[0])
        except:
            self.variable_flipkart.set('Product not available')

        option_amzn = OptionMenu(
            self.window, self.variable_amazon, *self.matches_amazon)
        option_amzn.grid(row=3, column=1, sticky=W)

        lab_amz = Label(
            self.window, text='<-Click the dropdown to try other variants')
        lab_amz.grid(row=3, column=2, padx=4)

        option_flip = OptionMenu(
            self.window, self.variable_flipkart, *self.matches_flip)
        option_flip.grid(row=0, column=1, sticky=W)

        lab_flip = Label(
            self.window, text='<-Click the dropdown to try other variants')
        lab_flip.grid(row=0, column=2, padx=4)

        button_amzn_visit = Button(
            self.window, text='Link', command=self.visit_amzn, bd=4)
        button_amzn_visit.grid(row=4, column=2, sticky=W)

        button_flip_visit = Button(
            self.window, text='Link', command=self.visit_flip, bd=4)
        button_flip_visit.grid(row=1, column=2, sticky=W)

    def price_flipkart(self, key):
        url_flipkart = 'https://www.flipkart.com/search?q=' + str(
            key) + '&marketplace=FLIPKART&otracker=start&as-show=on&as=off'
        map = defaultdict(list)

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        source_code = requests.get(url_flipkart, headers=self.headers)
        soup = BeautifulSoup(source_code.text, "html.parser")
        self.opt_title_flip = StringVar()
        home = 'https://www.flipkart.com'
        for block in soup.find_all('div', {'class': '_2kHMtA'}):
            title, price, link = None, 'Currently Unavailable', None
            for heading in block.find_all('div', {'class': '_4rR01T'}):
                title = heading.text
            for p in block.find_all('div', {'class': '_30jeq3 _1_WHN1'}):
                price = p.text[1:]
            for l in block.find_all('a', {'class': '_1fQZEK'}):
                link = home + l.get('href')
            map[title] = [price, link]

        user_input = self.var.get().title()
        self.matches_flip = get_close_matches(user_input, map.keys(), 20, 0.1)
        self.looktable_flip = {}
        for title in self.matches_flip:
            self.looktable_flip[title] = map[title]

        try:
            self.opt_title_flip.set(self.matches_flip[0])
            self.var_flipkart.set(
                self.looktable_flip[self.matches_flip[0]][0] + '.00')
            self.link_flip = self.looktable_flip[self.matches_flip[0]][1]
        except IndexError:
            self.opt_title_flip.set('Product not found')

    def price_amazon(self, key):
        url_amazon = 'https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=' + \
            str(key)

        # Faking the visit from a browser
        headers = {
            'authority': 'www.amazon.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        map = defaultdict(list)
        home = 'https://www.amazon.in'
        # proxies_list = ["128.199.109.241:8080", "113.53.230.195:3128", "125.141.200.53:80", "125.141.200.14:80",
        #                 "128.199.200.112:138", "149.56.123.99:3128", "128.199.200.112:80", "125.141.200.39:80",
        #                 "134.213.29.202:4444"]
        # proxies = {'https': random.choice(proxies_list)}
        source_code = requests.get(url_amazon, headers=headers)
        plain_text = source_code.text
        self.opt_title = StringVar()
        self.soup = BeautifulSoup(plain_text, "html.parser")
        # print(self.soup)
        # print(self.soup.find_all('div', {'class': 'sg-col-inner'}))
        for html in self.soup.find_all('div', {'class': 'sg-col-inner'}):
            title, link, price = None, None, None
            for heading in html.find_all('span', {'class': 'a-size-medium a-color-base a-text-normal'}):
                title = heading.text
            for p in html.find_all('span', {'class': 'a-price-whole'}):
                price = p.text
            for l in html.find_all('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}):
                link = home + l.get('href')
            if title and link:
                map[title] = [price, link]
        user_input = self.var.get().title()
        self.matches_amazon = get_close_matches(
            user_input, list(map.keys()), 20, 0.01)
        self.looktable = {}
        for title in self.matches_amazon:
            self.looktable[title] = map[title]
        self.opt_title.set(self.matches_amazon[0])
        self.var_amazon.set(self.looktable[self.matches_amazon[0]][0] + '.00')
        self.product_link = self.looktable[self.matches_amazon[0]][1]

    def search(self):
        amazon_get = self.variable_amazon.get()
        self.opt_title.set(amazon_get)
        product = self.opt_title.get()
        price, self.product_link = self.looktable[product][0], self.looktable[product][1]
        self.var_amazon.set(price + '.00')
        flip_get = self.variable_flipkart.get()
        flip_price, self.link_flip = self.looktable_flip[flip_get][0], self.looktable_flip[flip_get][1]
        self.var_flipkart.set(flip_price + '.00')

    def visit_amzn(self):
        webbrowser.open(self.product_link)

    def visit_flip(self):
        webbrowser.open(self.link_flip)

    def plot():
        # the figure that will contain the plot
        fig = Figure(figsize=(5, 5),
                     dpi=100)
        # list of squares
        y = [i**2 for i in range(101)]
        # adding the subplot
        plot1 = fig.add_subplot(111)
        # plotting the graph
        plot1.plot(y)
        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack()
        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas, window)
        toolbar.update()
        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().pack()
        # the main Tkinter window
        window = Tk()
        # setting the title
        window.title('Plotting in Tkinter')
        # dimensions of the main window
        window.geometry("500x500")
        # button that displays the plot
        plot_button = Button(master=window,
                             command=plot,
                             height=2,
                             width=10,
                             text="Plot")
        # place the button
        # in main window
        plot_button.pack()


if __name__ == "__main__":
    c = Price_compare(root)
    root.title('Price Comparison Engine')
    root.mainloop()
