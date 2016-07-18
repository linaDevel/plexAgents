import urllib2 as urllib

VERSION_NO = '1.2013.06.02.1'


def any(s):
    for v in s:
        if v:
            return True
    return False


def Start():
    HTTP.CacheTime = 0


class EXCAgent(Agent.Movies):
    name = 'DigitalPlayground'
    languages = [Locale.Language.English]
    accepts_from = ['com.plexapp.agents.localmedia']
    primary_provider = True

    def search(self, results, media, lang):
        title = media.name
        if media.primary_metadata is not None:
            title = media.primary_metadata.title

        year = media.year
        if media.primary_metadata is not None:
            year = media.primary_metadata.year

        encodedTitle = urllib.quote(title)

        searchResults = HTML.ElementFromURL(
            'http://www.digitalplayground.com/search/?q=' + encodedTitle
        )
        for searchResult in searchResults.xpath(
            '//*[@id="container"]/div/section'
            '[contains(@class,"dvd")]/div/article'
        ):
            titleNoFormatting = searchResult.xpath(
                './div/div/div/h4/span/a'
            )[0].text
            curID = searchResult.xpath(
                './div/div/div/h4/span/a'
            )[0].get('href').replace('/', '_')
            score = 100 - Util.LevenshteinDistance(
                title.lower(), titleNoFormatting.lower()
            )
            results.Append(MetadataSearchResult(
                id=curID, name=titleNoFormatting,
                score=score, lang=lang
            ))

        results.Sort('score', descending=True)

    def update(self, metadata, media, lang):

        metadata.studio = 'Digital Playground'
        temp = str(metadata.id).replace('_', '/')
        details = HTML.ElementFromURL(
            "http://www.digitalplayground.com" + temp
        )

        # Summary
        metadata.title = details.xpath(
            '//*[@id="container"]/section[1]/div/header/h1'
        )[0].text

        # Posters
        poster = details.xpath('//*[@id="front-cover"]')[0].get('src')
        metadata.posters[poster] = Proxy.Preview(
            HTTP.Request(
                poster, headers={'Referer': 'http://www.google.com'}
            ).content,
            sort_order=1
        )
