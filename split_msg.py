import click
import sys
import re
from bs4 import BeautifulSoup 


@click.command()
@click.option('--max-len', default=1, help='Maximum length.')
@click.argument('source', type=click.Path(exists=True))
def get_data(source, max_len):
    """Splits the original message (`source`) into array"""
    with open(source, "r", encoding='utf-8') as f: 
        text = f.read()
    for part in split_message(text, max_len):
        sys.stdout.write(f"{part[0]}\n")
        sys.stdout.write(part[1])

def split_message(text, max_len):
    """Splits the original message (`source`) into fragments of 
    the specified length (`max_len`)."""
    array = text.split("\n") 
    html = []
    fragment = 1
    tags = []
    for index, item in enumerate(array):
        old_close_tags = ''.join([f'</{tag}>' for tag in tags]) # getting tags to close from previous line
        html.append(item)
        open_tags = [tag.strip('<') for tag in re.findall("<\w+", item)] # finding opening tags in line as array with only name
        close_tags = [tag.strip('</') for tag in re.findall("</\w+", item)] # finding closing tags in line as array with only name
        tags.extend(open_tags) # adding openings tags into tags to close
        for tag in close_tags: 
            tags.remove(tag)   # removing tags which are closed
        new_close_tags = ''.join([f'</{tag}>' for tag in tags]) # getting tags to close from current line
        html.append(new_close_tags)
        soup = BeautifulSoup(''.join(html), 'html.parser') 
        if not len(soup.prettify()) <= max_len:
            del html[-2:]                       # removing line and tags to close from current line
            html.append(old_close_tags)         # adding tags to close from previous line
            soup = BeautifulSoup(''.join(html), 'html.parser')
            if len(soup.prettify()) <= max_len and len(soup) > 0:
                yield [f'-- fragment #{fragment}: {len(soup.prettify())} chars --', soup.prettify()]
            else:
                yield ["Error:", "Max_len is less than one tag block"] # catching error
                break  # stoping script
            fragment += 1
            new_open_tags = ''.join([f'<{tag}>' for tag in tags]) # getting tags to open from current line
            html.clear()  
            html.append(new_open_tags)
            html.append(item)
        else:
            del html[-1]   # removing tags to close from current line
        if index == len(array) - 1:  # catching last element of list
            html.append(new_close_tags) #  adding tags to close
            soup = BeautifulSoup(''.join(html), 'html.parser')
            if len(soup) > 0 and len(soup.prettify()) <= max_len: # checking if current fragment is not empty and catching error
                yield [f'-- fragment #{fragment}: {len(soup.prettify())} chars --', soup.prettify()]
            elif len(soup.prettify()) >= max_len:
                yield ["Error:", "Max_len is less than one tag block"]           

if __name__ == '__main__':
    get_data()
