import requests
import random
from piece import Piece
import pyeuropeana.utils as utils
import pyeuropeana.apis as apis
import pandas as pd

class Europeana:
    # TO DO: bulk download and save data 
    def __init__(self, url, query):
        self.url = url
        self.query = query
        self.df = utils.search2df(self.make_request())

    def make_request(self):
        response = requests.get(self.url)
        return response.json()

    def bulk_requests(self):
        query_terms = [
            'art nouveau',
            'cubism',
            'surrealism',
            'expressionism' #,
            'impressionism',
            'rococo',
            'baroque',
            'pop art',
            'art deco',
            'dadaism',
            'de stijl',
            'symbolism',
            'romanticism',
            'digital art',
            'sculpture',
            'impressionism',
            'academic',
            'ancient',
            'classical',
            'contemporary',
            'expressionism',
            'fauvism',
            'gothic',
            'caravaggio',
            'michelangelo',
            'botticelli',
            'davinci',
            'raphael',
            'titian',
            'velázquez',
            'rembrandt',
            'vermeer',
            'monet',
            'degas',
            'gauguin',
            'matisse',
            'picasso',
            'kandinsky',
            'matisse',
            'klimt',
            'klee',
            'modern'
        ]
        df_list = []
        for query in query_terms:
            response = apis.search(
                query=query
            )
            self.df = pd.concat([self.df, utils.search2df(response)])
            cols = self.df.columns
            for col in cols:
                print(col)
                print(self.df[col].unique())
            
            print(self.df['type'])
        return self.df
        
    # def write_to_csv(self):
    #     self.df.to_csv('europeana_data.csv', index=False)

def main():
    key = "etendinfi"
    qf='''(DATA_PROVIDER:"Östasiatiska museet" NOT TYPE:TEXT) OR 
            (DATA_PROVIDER:"Medelhavsmuseet") OR (DATA_PROVIDER:"Rijksmuseum") 
            OR (europeana_collectionName: "91631_Ag_SE_SwedishNationalHeritage_shm_art") 
            OR (DATA_PROVIDER:"Bibliothèque municipale de Lyon") 
            OR (DATA_PROVIDER:"Museu Nacional d'Art de Catalunya") 
            OR (DATA_PROVIDER:"Victoria and Albert Museum") 
            OR (DATA_PROVIDER:"Slovak national gallery")
            OR (DATA_PROVIDER:"Thyssen-Bornemisza Museum") 
            OR (DATA_PROVIDER:"Museo Nacional del Prado") 
            OR (DATA_PROVIDER:"Statens Museum for Kunst") 
            OR (DATA_PROVIDER:"Hungarian University of Fine Arts, Budapest") 
            OR (DATA_PROVIDER:"Hungarian National Museum") 
            OR (DATA_PROVIDER:"Museum of Applied Arts, Budapest") 
            OR (DATA_PROVIDER:"Szépművészeti Múzeum") 
            OR (DATA_PROVIDER:"Museum of Fine Arts - Hungarian National Gallery, Budapest") 
            OR (DATA_PROVIDER:"Schola Graphidis Art Collection. Hungarian University of Fine Arts - High School of Visual Arts, Budapest") 
            OR (PROVIDER:"Ville de Bourg-en-Bresse") OR (DATA_PROVIDER:"Universitätsbibliothek Heidelberg")
            OR ((what:("fine art" OR "beaux arts" OR "bellas artes" OR "belle arti" OR "schone kunsten" OR konst OR "bildende kunst" OR "Opere d'arte visiva" OR "decorative arts" OR konsthantverk OR "arts décoratifs" OR paintings OR schilderij OR pintura OR peinture OR dipinto OR malerei OR måleri OR målning OR sculpture OR skulptur OR sculptuur OR beeldhouwwerk OR drawing OR poster OR tapestry OR gobelin OR jewellery OR miniature OR prints OR träsnitt OR holzschnitt OR woodcut OR lithography OR chiaroscuro OR "old master print" OR estampe OR porcelain OR mannerism OR rococo OR impressionism OR expressionism OR romanticism OR "Neo-Classicism" OR "Pre-Raphaelite" OR Symbolism OR Surrealism OR Cubism OR "Art Deco" OR "Art Déco" OR Dadaism OR "De Stijl" OR "Pop Art" OR "art nouveau" OR "art history" OR "http://vocab.getty.edu/aat/300041273" OR "histoire de l'art" OR kunstgeschichte OR "estudio de la historia del arte" OR Kunstgeschiedenis OR "illuminated manuscript" OR buchmalerei OR enluminure OR "manuscrito illustrado" OR "manoscritto miniato" OR boekverluchting OR kalligrafi OR calligraphy OR exlibris)) AND (provider_aggregation_edm_isShownBy:*)) NOT (what: "printed serial" OR what:"printedbook" OR "printing paper" OR "printed music" OR DATA_PROVIDER:"NALIS Foundation" OR DATA_PROVIDER:"Ministère de la culture et de la communication, Musées de France" OR DATA_PROVIDER:"CER.ES: Red Digital de Colecciones de museos de España" OR PROVIDER:"OpenUp!" OR PROVIDER:"BHL Europe" OR PROVIDER:"EFG - The European Film Gateway" OR DATA_PROVIDER: "Malta Aviation Museum Foundation" OR DATA_PROVIDER:"National Széchényi Library - Digital Archive of Pictures" OR PROVIDER:"Swiss National Library")'''
    url = f"https://api.europeana.eu/api/v2/search.json?query={qf}&wskey=etendinfi"
    europeana = Europeana(url, qf)
    europeana.bulk_requests()


if __name__ == "__main__":
    main()


