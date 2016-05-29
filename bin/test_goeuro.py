#!/usr/bin/env python

import time
import sys
import unittest

class TrainResults(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_search(self):
        print "opening browser"
        self.driver.get('http://www.goeuro.com/')
        print "browse opened"
        
        print "inserting from/to destination"
        from_input = self.driver.find_element_by_id('from_filter')
        from_input.send_keys('Berlin, Germany')
        to_input = self.driver.find_element_by_id('to_filter')
        to_input.send_keys('Prague, Czech Republic')
        
        print "click on search button"
        search_btn = self.driver.find_element_by_id('search-form__submit-btn')
        # TODO: these two lines below are workaround, for some reason sometimes click() doesn't work, need to investigate 
        search_btn.send_keys('')
        time.sleep(1)
        
        search_btn.click()
        
        # wait until results are ready, detection is done using <div id='results-train'> .This element should have class='active'
        # max time to wait is 10seconds
        print "wait until results are returned...."
        results_ready = False
        iteration = 0 
        while not results_ready and iteration < 5:
            try:
                #to_input = self.driver.find_element_by_class_name("tabs-content")
                results_train = self.driver.find_element_by_id('results-train')
                class_attribute = results_train.get_attribute("class")
                print "results are %s" %class_attribute
                if class_attribute == 'active':
                    print "results are loaded"
                    results_ready = True
                    break
            except Exception as e:
                time.sleep(2)
                iteration+=1
            
                
        print "extracting prices from the page..."
        prices_elems = self.driver.find_elements_by_xpath("//div[@id='results-train']//div[contains(@class, 'price-cell-content')]")
        prices = []
        for price_elem in prices_elems:
            total_text = price_elem.text
            price = self._get_price(total_text)
            if price:
                prices.append(price)
        print "prices are extracted"
        
        if prices:
            is_sorted = all(prices[i] <= prices[i+1] for i in xrange(len(prices)-1))
            self.assertEqual(is_sorted, True, "Prices are not sorted, prices are: %s" %",".join(map(lambda x : str(x), prices)))
            print "Test passed, Prices are sorted, prices are: %s" %",".join(map(lambda x : str(x), prices))
        else:
            print "no prices were extracted"
            self.fail("No prices were extracted from HTML page")
        
    def tearDown(self):
        print "close browser"
        self.driver.quit()
        
    def _get_price(self, text):
        #helper method, which takes entire text and extract only the price
        price = None
        try:
            splitted = text.split(' ')
            price = splitted[4]
            return float(price)
        except Exception as e:
            print e
        return price

if __name__ == '__main__':
    
    try:
        from selenium import webdriver
    except ImportError:
        print('selenium not installed, please install with pip install selenium')
        sys.exit(-1)
    
    unittest.main()