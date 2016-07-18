
VERSION_NO = '1.2013.06.02.1'


def any(s):
    for v in s:
        if v:
            return True
    return False


def Start():
    HTTP.CacheTime = 0


class EXCAgent(Agent.Movies):
    name = 'InterracialBlowbang'
    languages = [Locale.Language.English]
    accepts_from = ['com.plexapp.agents.localmedia']
    primary_provider = True

    def search(self, results, media, lang):
        title = media.name
        if media.primary_metadata is not None:
            title = media.primary_metadata.title

        results.Append(MetadataSearchResult(
            id="_".join([part.lower() for part in title.split(" ")]),
            name=title, score=100, lang=lang
        ))
        results.Sort('score', descending=True)

    def update(self, metadata, media, lang):

        metadata.studio = 'Interracial Blowbang'
        details = HTML.ElementFromURL(
            "http://www.interracialblowbang.com/tour/"
            "interracial-gangbang/%s/" % metadata.id
        )
        print metadata.id

        # Posters
        i = 1
        for poster_path in [
            '//*[@id="mod_thumb1"]', '//*[@id="mod_thumb2"]',
            '//*[@id="mod_thumb3"]'
        ]:
            poster = details.xpath(poster_path)[0].get('src')
            metadata.posters[poster] = Proxy.Preview(
                HTTP.Request(
                    poster, headers={'Referer': 'http://www.google.com'}
                ).content,
                sort_order=i
            )
            i += 1
