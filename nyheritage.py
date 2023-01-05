import pysolr
from description_indexer.configurator import Config
from description_indexer.models.arclight import SolrCollection, SolrComponent

config = Config()

solr_url = config.solr_url
solr = pysolr.Solr(solr_url + "/" + config.solr_core, always_commit=True)
solr.ping()

collection1 = SolrCollection()

collection1.id = "p16694coll45"
collection1.title_ssm = ["Wayne Tucker Postcard Collection"]
collection1.repository_ssm = ["Schenectady County Historical Society"]
collection1.repository_sim = ["Schenectady County Historical Society"]
collection1.scopecontent_ssm = ["This collection contains postcards, trade cards, and other ephemera relating to Schenectady County and other nearby areas. The collection was willed to the Schenectady County Historical Society by former Glenville resident Wayne Tucker. Mr. Tucker was an avid collector of postcards and his collection was quite comprehensive with postcards of showing the same area from various viewpoints and years. Most of the postcards date from the early twentieth century and are either colorized views of an area, or real photo postcards."]
collection1.bioghist_ssm = ["Schenectady is a city located near Albany, New York. The city developed at a rapid pace in the nineteenth century because of its location to the Erie Canal and Mohawk River, making it a transportation corridor. The city also grew into a manufacturing territory, with the cotton mill being a major source for product and trade."]
collection1.extent_ssm = ["184"]
collection1.unitdate_ssm = ["c. 1900 - 1940"]
collection1.date_range_sim = [1900, 1940]
collection1.level_ssm = ["collection"]
collection1.level_sim = ["collection"]
collection1.creator_ssm = ["Unknown", "C.W. Hughes and Company, Mechanicville, NY", "Albany News Company", "Novitas Post Card Company, New York City", "Bush Smith Company, Schenectady, NY"]
collection1.creator_ssim = ["Unknown", "C.W. Hughes and Company, Mechanicville, NY", "Albany News Company", "Novitas Post Card Company, New York City", "Bush Smith Company, Schenectady, NY"]
collection1.creators_ssim = ["Unknown", "C.W. Hughes and Company, Mechanicville, NY", "Albany News Company", "Novitas Post Card Company, New York City", "Bush Smith Company, Schenectady, NY"]
collection1.creator_corpname_ssm = ["Unknown", "C.W. Hughes and Company, Mechanicville, NY", "Albany News Company", "Novitas Post Card Company, New York City", "Bush Smith Company, Schenectady, NY"]
collection1.access_subjects_ssim = ["Postcards", "Parks", "Amusement parks", "Fountains", "Amusement rides"]
collection1.access_subjects_ssm = ["Postcards", "Parks", "Amusement parks", "Fountains", "Amusement rides"]
collection1.normalized_title_ssm = ["Wayne Tucker Postcard Collection, c. 1900-1940"]
collection1.collection_title_tesim = ["Wayne Tucker Postcard Collection, c. 1900-1940"]
collection1.has_online_content_ssim = ["Contains online items"]


item1 = SolrComponent()

item1.id = "p16694coll45:229"
item1.title_ssm = ["Scotia Gate and Toll Bridge, Schenectady, NY"]
item1.unitdate_ssm = ["1918"]
item1.date_range_sim = [1918]
item1.level_ssm = ["item"]
item1.level_sim = ["item"]
item1.repository_ssm = ["Schenectady County Historical Society"]
item1.repository_sim = ["Schenectady County Historical Society"]
item1.description_ssim = ["View of the Scotia Bridge, toll gate and electric trolley stop in Schenectady, NY."]
item1.creator_ssm = ["Charles W. Hughes, Schenectady, NY"]
item1.creator_ssim = ["Charles W. Hughes, Schenectady, NY"]
item1.creators_ssim = ["Charles W. Hughes, Schenectady, NY"]
item1.creator_corpname_ssm = ["Charles W. Hughes, Schenectady, NY"]
item1.access_subjects_ssim = ["Postcards", "Bridges"]
item1.access_subjects_ssm = ["Postcards", "Bridges"]
item1.corpname_ssm = ["Scotia Bridge"]
item1.physloc_ssm = ["Wayne Tucker Postcard Collection at Grems-Doolittle Library"]
item1.type_ssim = ["Still image"]
item1.language_ssm = ["eng"]
item1.mime_types_ssm = ["image/jpeg"]
item1.legacy_identifier_ssim = ["NYSHS003060"]
item1.rights_statement_ssi = "http://rightsstatements.org/vocab/UND/1.0/"
item1.prefercite_ssm = ["Please cite this image as the Grems-Doolittle Library Photograph Collection."]
item1.processing_activity_ssim = ["JPEG made from archival TIFF - Scanned using Epson Expression 10000 XL at 600dpi"]
item1.date_digitized_ssim = "2019-08-20"
item1.original_format_ssim = ["Postcards"]
item1.physical_dimensions_ssim = ["Postcard; col.; 3.5 x 5.5 in. (8.9 x 14 cm.)"]

item1.filenames_ssm = ["index.cpd", "NYSHS_WTPC_060.jpg"]
item1.iiif_manifest_ssi = "https://nyheritage.contentdm.oclc.org/iiif/2/p16694coll45:229/manifest.json"
item1.is_representative_ssm = "true"
item1.hrefs_ssm = ["https://nyheritage.contentdm.oclc.org/digital/collection/p16694coll45/id/229/rec/36"]
item1.thumbnail_href_ssm = "https://nyheritage.contentdm.oclc.org/digital/api/singleitem/collection/p16694coll45/id/227/thumbnail"
item1.has_online_content_ssim = ["Online access"]

collection1.components.append(item1)

print ("POSTing data to Solr...")

solr.add([collection1.to_struct()])
