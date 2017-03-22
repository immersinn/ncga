

from bs4 import BeautifulSoup as bs
import pandas

import utils


donation_docs = {'2014' : 'NC Campaign Document Search By Type-2014.html',
				 '2015' : 'NC Campaign Document Search By Type-2015.html',
				 '2016' : 'NC Campaign Document Search By Type-2016.html',
				}


def load_campdoc_html(year):

	try:
		fn = donation_docs[year]
		data_dir = utils.get_data_dir(which='Dropbox')
		with open(os.path.join(data_dir, 'PACDocs', fn), 'r') as f:
			html = f.read()
		return(html)

	except KeyError:
		err_msg = "Invalid Report Year specified.  Select on of: " + '; '.join(donation_docs.keys())
		raise KeyError(err_msg)


def process_table(table, limit=-1):
    
    def process_row(row):
        data = {}
        for cn, col in zip(col_names, row.find_all('td')):
            a = col.find('a')
            if a:
                try:
                    data[cn] = a['href']
                except KeyError:
                    data[cn] = ''
            else:
                data[cn] = col.text.strip()
        return(data)

    rows = table.find_all('tr')
    col_names = [h.text for h in rows[0].find_all('td')]
    
	if limit==-1:
		limit = len(rows)-1

    data = [process_row(row) for row in rows[1:limit]]
    df = pandas.DataFrame(data)
    df = df[col_names]
    
    return(df)


def extract_nccd(year='2014'):

	html = load_compdoc_html(year)
	soup = bs(html, 'html.parser')
	table = soup.find('table')
	data = process_table(table)
	
	return(data)
