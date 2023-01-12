# description_indexer
A tool for working with archival description for public access. description_indexer reads archival description into a [minimalist data model for public-facing archival description](https://github.com/UAlbanyArchives/description_indexer/blob/main/description_indexer/models/description.py) and then converts it to the [Arclight data model](https://github.com/UAlbanyArchives/description_indexer/blob/main/description_indexer/models/arclight.py) and POSTs it into an Arclight Solr index using [PySolr](https://github.com/django-haystack/pysolr).

description_indexer is designed to be extensible and harvest archival description from a number of [sources](https://github.com/UAlbanyArchives/description_indexer/tree/main/description_indexer/inputs). Currently the only available source harvests data from the [ArchivesSpace](https://github.com/archivesspace/archivesspace) [API](https://archivesspace.github.io/archivesspace/api/#introduction) using [ArchivesSnake](https://github.com/archivesspace-labs/ArchivesSnake). It is possible in the future to add modules for EAD2002 and other sources. Its also possible to add additional [output modules](https://github.com/UAlbanyArchives/description_indexer/tree/main/description_indexer/outputs) to serialize description to EAD or other formats in addition to or in replace of sending description to an Arclight Solr instance. This potential opens up new possibilities of managing description using low-barrier formats and tools.

The [main branch](https://github.com/UAlbanyArchives/description_indexer) is designed to be a drop-in replacement for the Arclight Traject indexer, while the [dao-indexing branch](https://github.com/UAlbanyArchives/description_indexer/tree/dao-indexing) tries to fully index digital objects from digital repositories and other sources, including item-level metadata fields, embedded text, OCR text, and transcriptions. 

This is still a bit drafty, as its only tested on ASpace v2.8.0 and needs better error handling. Validation is also very minimal, but there is potential to add detailed validation with `jsonschema `.

### Installation

```python
pip install description_indexer
```

First, you need to configure ArchivesSnake by creating a `~/.archivessnake.yml`file with your API credentials as detailed by the [ArchivesSnake configuration docs](https://github.com/archivesspace-labs/ArchivesSnake#configuration).

Next, you also need a `~/.description_indexer.yml` file that lists your Solr URL and the core you want to index to. These can also be overridden with args.

```yml
solr_url: http://127.0.0.1:8983/solr
solr_core: blacklight-core
last_query: 0
```

### Indexing from ArchivesSpace API to Arclight

Once description_indexer is set up, you can index from the ASpace API to Arclight using the `to-arclight` command.

#### Index by id_0

You can provide one or more IDs to index using a resource's id_0` field

`to-arclight --id ua807`

`to-arclight --id mss123 apap106`

#### Index by URI

You can also use integers from ASpace URIs for resource, such as 263 for `https://my.aspace.edu/resources/263`

`to-arclight --uri 435`

`to-arclight --uri 1 755`

#### Indexing by modified time

Index collections modified in the past hour: `to-arclight --hour`

Index collections modified in the past day: `to-arclight --today`

Index collections modified since las run: `to-arclight --new`

#### Deleting collections

You can delete one or more collections using the `--delete` argument in addition to`--id`. This uses the Solr document ID, such as `apap106` for `https://my.arclight.edu/catalog/apap106`.

`to-arclight --id apap101 apap301 --delete`



### Indexing Digital Objects

The [dao-indexing branch](https://github.com/UAlbanyArchives/description_indexer/tree/dao-indexing) can index full text content such as transcriptions and OCR output from digital objects. To do this, your Arclight Solr core must be created with the [provided configset](https://github.com/UAlbanyArchives/description_indexer/tree/dao-indexing/solr/conf) which extends the [Arclight configset](https://github.com/projectblacklight/arclight/tree/main/solr/conf).

Since archival repositories manage digital objects using a variety of tools and repositories, description_indexer is designed to incorporate local logic as plugins to map digital object data from different sources to a [common data model](https://github.com/UAlbanyArchives/description_indexer/blob/dao-indexing/description_indexer/models/description.py). To harvest digital object data from your local system, copy the [example plugin](https://github.com/UAlbanyArchives/description_indexer/blob/dao-indexing/description_indexer/dao_plugins/example.py) to `~/.description_indexer/dao_plugins/my_plugin.py`or another location and set the path to a `$DESCRIPTION_INDEXER_PLUGIN_DIR` environment variable. `.py` files in these locations that follow the [example plugin](https://github.com/UAlbanyArchives/description_indexer/blob/dao-indexing/description_indexer/dao_plugins/example.py) will be able to modify digital object data using a local system. The [UAlbany-hyrax](https://github.com/UAlbanyArchives/description_indexer/blob/dao-indexing/description_indexer/dao_plugins/UAlbany-hyrax.py) plugin is available as a built-in example that reads data from UAlbany's [Hyrax](https://hyrax.samvera.org/) instance at [https://archives.albany.edu/catalog](https://archives.albany.edu/catalog).

description_indexer also comes equipped with a number of [extractors](https://github.com/UAlbanyArchives/description_indexer/tree/dao-indexing/description_indexer/extractors) for extracting content from digital objects. The [text extractor](https://github.com/UAlbanyArchives/description_indexer/blob/dao-indexing/description_indexer/extractors/text.py) is simplest, as it just reads from plain text files or CSVs. The Tika extractor uses [Apache Tika](https://github.com/UAlbanyArchives/description_indexer/blob/dao-indexing/description_indexer/models/description.py) as a [command line utility](https://tika.apache.org/2.6.0/gettingstarted.html#Using_Tika_as_a_command_line_utility) to extract text from PDFs, images, or office documents. This requires [Java](https://openjdk.org/), the `tika-app.jar` file, and a `$TIKA_PATH` environment variable that points to the location of `tika-app.jar`. The Tika extractor can also perform OCR on digital objects. This requires [tesseract](https://tesseract-ocr.github.io/) to be installed and a `tika-config.xml` file in `$TIKA_PATH` that tells Tika to [extract text with OCR](https://stackoverflow.com/questions/51655510/how-do-you-enable-the-tesseractocrparser-using-tikaconfig-and-the-tika-command-l#answer-60404894).

Extracting text and performing OCR during harvesting is not great practice, as its much slower than harvesting description and can take a very long time for a collection with many digital objects, so this functionality is offered just as a proof-of-concept. To limit re-running Tika during reindexing, description_indexer stores extracted texts to the files system at `~/.description_indexer/[id].txt`or `C:\Users\[username]\.description_indexer\[id].txt` and uses these files for future harvests if they are present. Ideally, extracted text would be made available by whatever tool is managing your digital objects using a common specification.