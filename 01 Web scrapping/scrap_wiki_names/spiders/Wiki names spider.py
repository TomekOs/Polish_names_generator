import scrapy

class WikiNamesSpider(scrapy.Spider):
    
    # name of the Spider
    name = "wiki_names"
    
    # Return Request object which will be parsed by function indiciated in callback argument
    def start_requests(self):
        start_url = "https://pl.wikipedia.org/wiki/Kategoria:Alfabetyczna_lista_imion"
        return [scrapy.Request(url=start_url, callback = self.parse_start_page)]
    
    # Follow links on initial Wikipedia site (page with letters of alphabet)
    def parse_start_page(self, response):
        for link in response.css("div.mw-category-group ul li a::attr(href)").extract():
            yield response.follow(link, callback = self.parse_letter_name_list)
        
    # Follow links on Wikipedia page with containing alhabetical list of names
    def parse_letter_name_list(self, response):
        for link in response.css("div.mw-parser-output ul li a::attr(href)").extract():
            yield response.follow(link, callback = self.parse_name_page)
        
    # Parse web pages conatining description of each first name and return first name and content of first paragraph of text description of the name
    def parse_name_page(self, response):
        yield {
                "name": response.css("h1.firstHeading::text").extract(),
                "name_description": response.xpath("string(//div[@class=\"mw-parser-output\"]/p[1])").extract()
        }