

class fybse (fyb):


    def describe(self):
        return self.deep_extend(super.describe(), {
            'id': 'fybse',
            'name': 'FYB-SE',
            'countries': 'SE',  # Sweden
            'hasCORS': False,
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27766512-31019772-5edb-11e7-8241-2e675e6797f1.jpg',
                'api': 'https://www.fybse.se/api/SEK',
                'www': 'https://www.fybse.se',
                'doc': 'http://docs.fyb.apiary.io',
            },
            'markets': {
                'BTC/SEK': {'id': 'SEK', 'symbol': 'BTC/SEK', 'base': 'BTC', 'quote': 'SEK'},
        })
