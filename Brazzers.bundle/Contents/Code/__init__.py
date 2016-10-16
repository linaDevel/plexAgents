import urllib2 as urllib

VERSION_NO = '1.2013.06.02.1'


def any(s):
    for v in s:
        if v:
            return True
    return False


def Start():
    HTTP.CacheTime = CACHE_1DAY


class EXCAgent(Agent.Movies):
    name = 'Brazzers'
    languages = [Locale.Language.English]
    accepts_from = ['com.plexapp.agents.localmedia']
    primary_provider = True

    def search(self, results, media, lang):
        title = media.name
        if media.primary_metadata is not None:
            title = media.primary_metadata.title

        encodedTitle = urllib.quote(title)

        searchResults = HTML.ElementFromURL(
            'https://bazze.lina-infra.ru/search?title=' + encodedTitle
        )

        for searchResult in searchResults.xpath('//results/result'):
            titleNoFormatting = searchResult.get('title')
            curID = searchResult.get('link').replace('/', '_')
            score = 100 - Util.LevenshteinDistance(
                title.lower(), titleNoFormatting.lower()
            )
            results.Append(MetadataSearchResult(
                id=curID, name=titleNoFormatting, score=score, lang=lang
            ))

        results.Sort('score', descending=True)

    def update(self, metadata, media, lang):
        metadata.studio = 'Brazzers'
        temp = str(metadata.id).replace('_', '/')
        url = 'https://bazze.lina-infra.ru/get/' + temp
        details = HTML.ElementFromURL(url)

        # Summary
        metadata.summary = details.xpath("//video")[0].get('description')
        metadata.tagline = details.xpath("//video")[0].get('category')
        metadata.title = details.xpath("//video")[0].get('title')
        metadata.year = int(details.xpath("//video")[0].get('year'))

        # Genres
        metadata.genres.clear()
        for genre in details.xpath('//video/tags/tag'):
            metadata.genres.add(genre.get('name'))

        metadata.roles.clear()
        metadata.collections.clear()

        # Actors
        for member in details.xpath('//video/models/model'):
            role = metadata.roles.new()

            role.name = member.get('name')
            metadata.collections.add(member.get('name'))
            role.photo = member.get('image')

        # Posters
        i = 1
        for poster in details.xpath('//video/images/image'):
            if float(poster.get('aspect')) < 1:
                # Item is a poster
                metadata.posters[poster.get('link')] = Proxy.Preview(
                    HTTP.Request(
                        poster.get('link'),
                        headers={
                            'Referer': 'http://www.google.com'
                        }).content,
                    sort_order=i
                )
            else:
                # Item is an art item
                metadata.art[poster.get('link')] = Proxy.Preview(
                    HTTP.Request(
                        poster.get('link'),
                        headers={
                            'Referer': 'http://www.google.com'
                        }).content,
                    sort_order=i
                )
            i += 1

        # Add actor posters
        for member in details.xpath('//video/models/model'):
            metadata.posters[member.get('image')] = Proxy.Preview(
                HTTP.Request(
                    member.get('image'),
                    headers={'Referer': 'http://www.google.com'}).content,
                sort_order=i
            )
            i += 1
