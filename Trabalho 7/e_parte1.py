import io
from pyquery import PyQuery
import urllib.request as urllib
import urllib.error as urlib_error


def writeInFile(out):
    with io.open('movies_db.out', 'w', encoding='utf8') as file:
        file.write(out)
    file.close()


def main():
    movie_number = 0
    count = 0
    out = ''
    css_selector = '#content-start > article > div.card.card-movie.card-movie-overview.row.row-col-padded-10.cf > div > div > div:nth-child'

    while count < 50:
        movie_number += 1
        target = "http://www.adorocinema.com/filmes/filme-"
        try:
            html = urllib.urlopen(target + str(movie_number)).read()
        except urlib_error.HTTPError:
            continue

        count += 1
        pyQuery = PyQuery(html)
        movie = pyQuery('#content-layout > div > div.row.row-col-padded > div > div > div').text() + ';'  # movie_name
        pq = pyQuery(css_selector+'(1)').text()
        if 'Data de lançamento ' in pq:
            for i in range(2, 6):
                movie += pyQuery(css_selector + '(' + str(i) + ')').text() + ';'
        else:
            for i in range(1, 5):
                movie += pyQuery(css_selector + '(' + str(i) + ')').text() + ';'

        out += movie.replace('Nacionalidade ', '')\
                   .replace('Direção: ', '')\
                   .replace('Elenco: ', '')\
                   .replace(' mais', '')\
                   .replace('Gênero ', '')\
                   .replace('Gêneros ', '').replace(' , ', ', ') + str('\n')
        print(movie_number)
    writeInFile(out)


if __name__ == '__main__':
    main()