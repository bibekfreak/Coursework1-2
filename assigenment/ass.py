import unittest
from unittest.mock import patch, Mock
import requests
from bs4 import BeautifulSoup
from assignment import WebCrawler  

class TestWebCrawler(unittest.TestCase):
    
    @patch('requests.get')
    def test_fetch_links_success(self, mock_get):
       
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '<html><body><a href="http://example.com">Example</a></body></html>'
        mock_get.return_value = mock_response
        
        crawler = WebCrawler("http://test.com")
        links = crawler.fetch_links()
        self.assertEqual(links, ['http://example.com'])
    
    @patch('requests.get')
    def test_fetch_links_failure(self, mock_get):
        
        mock_get.side_effect = requests.exceptions.RequestException("Error")
        
        crawler = WebCrawler("http://test.com")
        links = crawler.fetch_links()
        self.assertEqual(links, "Error")

if __name__ == '__main__':
    unittest.main()
