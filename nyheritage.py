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
collection1.collection_sim = ["Wayne Tucker Postcard Collection"]
collection1.collection_ssi = ["Wayne Tucker Postcard Collection"]
collection1.repository_ssm = ["Schenectady County Historical Society"]
collection1.repository_sim = ["Schenectady County Historical Society"]
collection1.scopecontent_ssm = ["This collection contains postcards, trade cards, and other ephemera relating to Schenectady County and other nearby areas. The collection was willed to the Schenectady County Historical Society by former Glenville resident Wayne Tucker. Mr. Tucker was an avid collector of postcards and his collection was quite comprehensive with postcards of showing the same area from various viewpoints and years. Most of the postcards date from the early twentieth century and are either colorized views of an area, or real photo postcards."]
collection1.bioghist_ssm = ["Schenectady is a city located near Albany, New York. The city developed at a rapid pace in the nineteenth century because of its location to the Erie Canal and Mohawk River, making it a transportation corridor. The city also grew into a manufacturing territory, with the cotton mill being a major source for product and trade."]
collection1.extent_ssm = ["184"]
collection1.unitdate_ssm = ["c. 1900 - 1940"]
collection1.date_range_sim = [1900, 1940]
collection1.level_ssm = ["Collection"]
collection1.level_sim = ["Collection"]
collection1.creator_ssm = ["Unknown", "C.W. Hughes and Company, Mechanicville, NY", "Albany News Company", "Novitas Post Card Company, New York City", "Bush Smith Company, Schenectady, NY"]
collection1.creator_ssim = ["Unknown", "C.W. Hughes and Company, Mechanicville, NY", "Albany News Company", "Novitas Post Card Company, New York City", "Bush Smith Company, Schenectady, NY"]
collection1.creators_ssim = ["Unknown", "C.W. Hughes and Company, Mechanicville, NY", "Albany News Company", "Novitas Post Card Company, New York City", "Bush Smith Company, Schenectady, NY"]
collection1.creator_corpname_ssm = ["Unknown", "C.W. Hughes and Company, Mechanicville, NY", "Albany News Company", "Novitas Post Card Company, New York City", "Bush Smith Company, Schenectady, NY"]
collection1.access_subjects_ssim = ["Postcards", "Parks", "Amusement parks", "Fountains", "Amusement rides"]
collection1.access_subjects_ssm = ["Postcards", "Parks", "Amusement parks", "Fountains", "Amusement rides"]
collection1.normalized_title_ssm = ["Wayne Tucker Postcard Collection, c. 1900-1940"]
collection1.collection_title_tesim = ["Wayne Tucker Postcard Collection, c. 1900-1940"]
collection1.has_online_content_ssim = ["Contains online items"]
collection1.ead_ssi = ["nyh-p16694coll45"]

collection2 = SolrCollection()

collection2.id = "schmuse"
collection2.title_ssm = ["Steinmetz Digital Collection of Schenectady"]
collection2.collection_sim = ["Steinmetz Digital Collection of Schenectady"]
collection2.collection_ssi = ["Steinmetz Digital Collection of Schenectady"]
collection2.repository_ssm = ["Steinmetz Digital Collection of Schenectady"]
collection2.repository_sim = ["Steinmetz Digital Collection of Schenectady"]
collection2.scopecontent_ssm = ["The Steinmetz Collection of Schenectady tells the story of Dr. Charles Steinmetz, General Electric's Chief Engineer in the 1890s and early 1900s, through photographs and documents."]
collection2.bioghist_ssm = ["Charles Proteus Steinmetz (1865 - 1923) was the Chief Engineer for General Electric during the 1890s and early 1900s. His birth name was Karl August Rudolph Steinmetz but changed it when he came to the United States to have a more American sounding name. Steinmetz cultivated the development of alternating current which led to the growth of the electric power industry and made innovative discoveries that led future engineers into designing higher quality electromagnetic apparatus equipment. The additional areas Steinmetz is known for in the electrical engineering field involve alternating current systems theory’s three major fields--transients, hysteresis, and steady-state analysis."]
collection2.extent_ssm = ["267"]
collection2.unitdate_ssm = ["c. 1860 - 1950"]
collection2.date_range_sim = [1860, 1950]
collection2.level_ssm = ["Collection"]
collection2.level_sim = ["Collection"]
collection2.creator_ssm = ["Steinmetz, Charles Proteus, 1865-1923", "General Electric Company Publicity Department", "unknown", "General Electric Company", "Hayden, Joseph, b. 1906"]
collection2.creator_ssim = ["Steinmetz, Charles Proteus, 1865-1923", "General Electric Company Publicity Department", "unknown", "General Electric Company", "Hayden, Joseph, b. 1906"]
collection2.creators_ssim = ["Steinmetz, Charles Proteus, 1865-1923", "General Electric Company Publicity Department", "unknown", "General Electric Company", "Hayden, Joseph, b. 1906"]
collection2.creator_corpname_ssm = ["unknown", "General Electric Company Publicity Department", "General Electric Company"]
collection2.creator_persname_ssm = ["Steinmetz, Charles Proteus, 1865-1923", "Hayden, Joseph, b. 1906"]
collection2.access_subjects_ssim = ["Engineers", "Rivers", "Canoes", "Bridges", "Play (Recreation)"]
collection2.access_subjects_ssm = ["Engineers", "Rivers", "Canoes", "Bridges", "Play (Recreation)"]
collection2.normalized_title_ssm = ["Steinmetz Digital Collection of Schenectady, c. 1860-1950"]
collection2.collection_title_tesim = ["Steinmetz Digital Collection of Schenectady, c. 1860-1950"]
collection2.has_online_content_ssim = ["Contains online items"]
collection2.ead_ssi = ["nyh-schmuse"]

item1 = SolrComponent()

item1.id = collection1.id + "-229"
item1.ead_ssi = ["p16694coll45"]
item1.title_ssm = ["Scotia Gate and Toll Bridge, Schenectady, NY"]
item1.collection_sim = ["Wayne Tucker Postcard Collection"]
item1.collection_ssi = ["Wayne Tucker Postcard Collection"]
item1.unitdate_ssm = ["1918"]
item1.date_range_sim = [1918]
item1.normalized_title_ssm = ["Scotia Gate and Toll Bridge, Schenectady, NY, 1918"]
item1.level_ssm = ["Item"]
item1.level_sim = ["Item"]
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

item1.parent_ssim = ["p16694coll45"]
item1.parent_ssi = ["p16694coll45"]
item1.parent_levels_ssm = ["collection"]
item1.parent_unittitles_ssm = ["Wayne Tucker Postcard Collection, c. 1900-1940"]
item1.parent_unittitles_teim = ["Wayne Tucker Postcard Collection, c. 1900-1940"]
item1.component_level_isim = [1]
item1.collection_creator_ssm = ["Unknown", "C.W. Hughes and Company, Mechanicville, NY", "Albany News Company", "Novitas Post Card Company, New York City", "Bush Smith Company, Schenectady, NY"]
item1.child_component_count_isim = [0]
#item1.parent_access_restrict_ssm = fields.ListField(str)
#item1.parent_access_terms_ssm = fields.ListField(str)
item1.title_filing_si = "Scotia Gate and Toll Bridge, Schenectady, NY, 1918"
item1.ref_ssm = ["p16694coll45-229"]
item1.ref_ssi = "p16694coll45-229"

item2 = SolrComponent()

item2.id = collection1.id + "-310"
item2.ead_ssi = ["p16694coll45"]
item2.title_ssm = ["The Mohawk River & Scotia Bridge, Schenectady, NY"]
item2.collection_sim = ["Wayne Tucker Postcard Collection"]
item2.collection_ssi = ["Wayne Tucker Postcard Collection"]
item2.unitdate_ssm = ["Unknown"]
item2.date_range_sim = []
item2.normalized_title_ssm = ["The Mohawk River & Scotia Bridge, Schenectady, NY"]
item2.level_ssm = ["Item"]
item2.level_sim = ["Item"]
item2.repository_ssm = ["Schenectady County Historical Society"]
item2.repository_sim = ["Schenectady County Historical Society"]
item2.description_ssim = ["View of boats in the Mohawk River going under the Scotia Bridge. The Scotia Bridge connected the Stockade of Schenectady with Scotia, NY."]
item2.creator_ssm = ["Charles W. Hughes, Schenectady, NY"]
item2.creator_ssim = ["Charles W. Hughes, Schenectady, NY"]
item2.creators_ssim = ["Charles W. Hughes, Schenectady, NY"]
item2.creator_corpname_ssm = ["Charles W. Hughes, Schenectady, NY"]
item2.access_subjects_ssim = ["Postcards", "Bridges", "Rivers"]
item2.access_subjects_ssm = ["Postcards", "Bridges", "Rivers"]
item2.corpname_ssm = ["Scotia Bridge"]
item2.physloc_ssm = ["Wayne Tucker Postcard Collection at Grems-Doolittle Library"]
item2.type_ssim = ["Still image"]
item2.language_ssm = ["eng"]
item2.mime_types_ssm = ["image/jpeg"]
item2.legacy_identifier_ssim = ["NYSHS003061"]
item2.rights_statement_ssi = "http://rightsstatements.org/vocab/UND/1.0/"
item2.prefercite_ssm = ["Please cite this image as the Grems-Doolittle Library Photograph Collection."]
item2.processing_activity_ssim = ["JPEG made from archival TIFF - Scanned using Epson Expression 10000 XL at 600dpi"]
item2.date_digitized_ssim = "2019-08-22"
item2.original_format_ssim = ["Postcards"]
item2.physical_dimensions_ssim = ["Postcard; col.; 3.5 x 5.5 in. (8.9 x 14 cm.)"]

item2.filenames_ssm = ["index.cpd", "NYSHS_WTPC_061.jpg"]
item2.iiif_manifest_ssi = "https://nyheritage.contentdm.oclc.org/iiif/2/p16694coll45:310/manifest.json"
item2.is_representative_ssm = "true"
item2.hrefs_ssm = ["https://nyheritage.contentdm.oclc.org/digital/collection/p16694coll45/id/310/rec/17"]
item2.thumbnail_href_ssm = "https://nyheritage.contentdm.oclc.org/digital/api/singleitem/collection/p16694coll45/id/310/thumbnail"
item2.has_online_content_ssim = ["Online access"]

item2.parent_ssim = ["p16694coll45"]
item2.parent_ssi = ["p16694coll45"]
item2.parent_levels_ssm = ["collection"]
item2.parent_unittitles_ssm = ["Wayne Tucker Postcard Collection, c. 1900-1940"]
item2.parent_unittitles_teim = ["Wayne Tucker Postcard Collection, c. 1900-1940"]
item2.component_level_isim = [1]
item2.collection_creator_ssm = ["Unknown", "C.W. Hughes and Company, Mechanicville, NY", "Albany News Company", "Novitas Post Card Company, New York City", "Bush Smith Company, Schenectady, NY"]
item2.child_component_count_isim = [0]
#item2.parent_access_restrict_ssm = fields.ListField(str)
#item2.parent_access_terms_ssm = fields.ListField(str)
item2.title_filing_si = "The Mohawk River & Scotia Bridge, Schenectady, NY"
item2.ref_ssm = ["p16694coll45-310"]
item2.ref_ssi = "p16694coll45-310"

item3 = SolrComponent()

item3.id = collection1.id + "-330"
item3.ead_ssi = ["p16694coll45"]
item3.title_ssm = ["Old Scotia Bridge, Schenectady, NY"]
item3.collection_sim = ["Wayne Tucker Postcard Collection"]
item3.collection_ssi = ["Wayne Tucker Postcard Collection"]
item3.unitdate_ssm = ["1906"]
item3.date_range_sim = [1906]
item3.normalized_title_ssm = ["Old Scotia Bridge, Schenectady, NY, 1906"]
item3.level_ssm = ["Item"]
item3.level_sim = ["Item"]
item3.repository_ssm = ["Schenectady County Historical Society"]
item3.repository_sim = ["Schenectady County Historical Society"]
item3.description_ssim = ["	View of the Old Scotia Bridge on the Mohawk River in Schenectady, NY from the NY Central Railroad track."]
item3.creator_ssm = ["Charles W. Hughes, Schenectady, NY"]
item3.creator_ssim = ["Charles W. Hughes, Schenectady, NY"]
item3.creators_ssim = ["Charles W. Hughes, Schenectady, NY"]
item3.creator_corpname_ssm = ["Charles W. Hughes, Schenectady, NY"]
item3.access_subjects_ssim = ["Postcards", "Bridges", "Rivers"]
item3.access_subjects_ssm = ["Postcards", "Bridges", "Rivers"]
item3.corpname_ssm = ["Scotia Bridge"]
item3.physloc_ssm = ["Wayne Tucker Postcard Collection at Grems-Doolittle Library"]
item3.type_ssim = ["Still image"]
item3.language_ssm = ["eng"]
item3.mime_types_ssm = ["image/jpeg"]
item3.legacy_identifier_ssim = ["NYSHS003066"]
item3.rights_statement_ssi = "http://rightsstatements.org/vocab/NoC-US/1.0/"
item3.prefercite_ssm = ["Please cite this image as the Grems-Doolittle Library Photograph Collection."]
item3.processing_activity_ssim = ["JPEG made from archival TIFF - Scanned using Epson Expression 10000 XL at 600dpi"]
item3.date_digitized_ssim = "2019-08-22"
item3.original_format_ssim = ["Postcards"]
item3.physical_dimensions_ssim = ["Postcard; col.; 3.5 x 5.5 in. (8.9 x 14 cm.)"]

item3.filenames_ssm = ["index.cpd", "NYSHS_WTPC_066.jpg"]
item3.iiif_manifest_ssi = "https://nyheritage.contentdm.oclc.org/iiif/2/p16694coll45:330/manifest.json"
item3.is_representative_ssm = "true"
item3.hrefs_ssm = ["https://nyheritage.contentdm.oclc.org/digital/collection/p16694coll45/id/330/rec/3"]
item3.thumbnail_href_ssm = "https://nyheritage.contentdm.oclc.org/digital/api/singleitem/collection/p16694coll45/id/328/thumbnail"
item3.has_online_content_ssim = ["Online access"]

item3.parent_ssim = ["p16694coll45"]
item3.parent_ssi = ["p16694coll45"]
item3.parent_levels_ssm = ["collection"]
item3.parent_unittitles_ssm = ["Wayne Tucker Postcard Collection, c. 1900-1940"]
item3.parent_unittitles_teim = ["Wayne Tucker Postcard Collection, c. 1900-1940"]
item3.component_level_isim = [1]
item3.collection_creator_ssm = ["Unknown", "C.W. Hughes and Company, Mechanicville, NY", "Albany News Company", "Novitas Post Card Company, New York City", "Bush Smith Company, Schenectady, NY"]
item3.child_component_count_isim = [0]
#item3.parent_access_restrict_ssm = fields.ListField(str)
#item3.parent_access_terms_ssm = fields.ListField(str)
item3.title_filing_si = "Old Scotia Bridge, Schenectady, NY"
item3.ref_ssm = ["p16694coll45-330"]
item3.ref_ssi = "p16694coll45-330"

item4 = SolrComponent()

item4.id = collection2.id + "-54"
item4.ead_ssi = ["schmuse"]
item4.title_ssm = ["Flood, Scotia Shore"]
item4.collection_sim = ["Steinmetz Digital Collection of Schenectady"]
item4.collection_ssi = ["Steinmetz Digital Collection of Schenectady"]
item4.unitdate_ssm = ["1895-04-10"]
item4.date_range_sim = [1895]
item4.normalized_title_ssm = ["Flood, Scotia Shore, 1895-04-10"]
item4.level_ssm = ["Item"]
item4.level_sim = ["Item"]
item4.repository_ssm = ["Steinmetz Digital Collection of Schenectady"]
item4.repository_sim = ["Steinmetz Digital Collection of Schenectady"]
item4.description_ssim = ["The Mohawk River rises as a result of melting snow and ice in the early spring, along with the spring rain season.  The flood is shown here in Schotia.  Scotia is a village located in Schenectady County on the north bank of the Mohawk River"]
item4.creator_ssm = ["Steinmetz, Charles Proteus, 1865-1923"]
item4.creator_ssim = ["Steinmetz, Charles Proteus, 1865-1923"]
item4.creators_ssim = ["Steinmetz, Charles Proteus, 1865-1923"]
item4.creator_persname_ssm = ["Steinmetz, Charles Proteus, 1865-1923"]
item4.access_subjects_ssim = ["Floods", "Spring", "Cities & towns"]
item4.access_subjects_ssm = ["Floods", "Spring", "Cities & towns"]
item4.persname_ssm = ["Steinmetz, Charles Proteus, 1865-1923"]
item4.physloc_ssm = ["Charles Steinmetz Photograph Collection"]
item4.type_ssim = ["Still image"]
item4.language_ssm = ["eng"]
item4.mime_types_ssm = ["image/jpeg"]
item4.legacy_identifier_ssim = ["CPS264"]
item4.rights_statement_ssi = "http://rightsstatements.org/vocab/NoC-US/1.0/"
item4.processing_activity_ssim = ["From Archival TIFF - Epson Expression 1680; 600 dpi; 21.4 MB; Grayscale; 5318 x 4305 pixels; no compression"]
item4.date_digitized_ssim = "2009-05-04"
item4.original_format_ssim = ["Black-and-white photographs"]
item4.physical_dimensions_ssim = ["photograph; b&w; 8 x 10 in. (20 x 24 cm.)"]

item4.iiif_manifest_ssi = "https://nyheritage.contentdm.oclc.org/iiif/2/schmuse:54/manifest.json"
item4.is_representative_ssm = "true"
item4.hrefs_ssm = ["https://nyheritage.contentdm.oclc.org/digital/collection/schmuse/id/54/rec/46"]
item4.thumbnail_href_ssm = "https://nyheritage.contentdm.oclc.org/digital/api/singleitem/collection/schmuse/id/54/thumbnail"
item4.has_online_content_ssim = ["Online access"]

item4.parent_ssim = ["schmuse"]
item4.parent_ssi = ["schmuse"]
item4.parent_levels_ssm = ["collection"]
item4.parent_unittitles_ssm = ["Steinmetz Digital Collection of Schenectady, c. 1860-1950"]
item4.parent_unittitles_teim = ["Steinmetz Digital Collection of Schenectady, c. 1860-1950"]
item4.component_level_isim = [1]
item4.collection_creator_ssm = ["Steinmetz, Charles Proteus, 1865-1923", "General Electric Company Publicity Department", "unknown", "General Electric Company", "Hayden, Joseph, b. 1906"]
item4.child_component_count_isim = [0]
#item4.parent_access_restrict_ssm = fields.ListField(str)
#item4.parent_access_terms_ssm = fields.ListField(str)
item4.title_filing_si = "Flood, Scotia Shore"
item4.ref_ssm = ["schmuse-54"]
item4.ref_ssi = "schmuse-54"

item5 = SolrComponent()

item5.id = collection2.id + "-219"
item5.ead_ssi = ["schmuse"]
item5.title_ssm = ["Scotia Bridge"]
item5.collection_sim = ["Steinmetz Digital Collection of Schenectady"]
item5.collection_ssi = ["Steinmetz Digital Collection of Schenectady"]
item5.unitdate_ssm = ["1897-070"]
item5.date_range_sim = [1897]
item5.normalized_title_ssm = ["Scotia Bridge, 1897-07"]
item5.level_ssm = ["Item"]
item5.level_sim = ["Item"]
item5.repository_ssm = ["Steinmetz Digital Collection of Schenectady"]
item5.repository_sim = ["Steinmetz Digital Collection of Schenectady"]
item5.description_ssim = ["This bridge connected the village of Scotia with the city of Schenectady, and crossing the Mohawk River at the foot of Washington Avenue in Schenectady.  On the original glass slide envelope, Steinmetz titled this photograph: From Yates' Veranda, Scotia Bridge."]
item5.creator_ssm = ["Steinmetz, Charles Proteus, 1865-1923"]
item5.creator_ssim = ["Steinmetz, Charles Proteus, 1865-1923"]
item5.creators_ssim = ["Steinmetz, Charles Proteus, 1865-1923"]
item5.creator_persname_ssm = ["Steinmetz, Charles Proteus, 1865-1923"]
item5.access_subjects_ssim = ["Bridges", "Rivers"]
item5.access_subjects_ssm = ["Bridges", "Rivers"]
item5.persname_ssm = ["Steinmetz, Charles Proteus, 1865-1923"]
item5.physloc_ssm = ["Charles Steinmetz Photograph Collection"]
item5.type_ssim = ["Still image"]
item5.language_ssm = ["eng"]
item5.mime_types_ssm = ["image/jpeg"]
item5.legacy_identifier_ssim = ["CPS755A"]
item5.rights_statement_ssi = "http://rightsstatements.org/vocab/NoC-US/1.0/"
item5.processing_activity_ssim = ["From Archival TIFF - Epson Expression 1680; 300 dpi; 353 KB; Grayscale; 2676 x 2179 pixels; no compression"]
item5.date_digitized_ssim = "2009-11-16"
item5.original_format_ssim = ["Black-and-white photographs"]
item5.physical_dimensions_ssim = ["photograph; b&w; 8 x 10 in. (20 x 24 cm.)"]

item5.iiif_manifest_ssi = "https://nyheritage.contentdm.oclc.org/iiif/2/schmuse:219/manifest.json"
item5.is_representative_ssm = "true"
item5.hrefs_ssm = ["https://nyheritage.contentdm.oclc.org/digital/collection/schmuse/id/219/rec/34"]
item5.thumbnail_href_ssm = "https://nyheritage.contentdm.oclc.org/digital/api/singleitem/collection/schmuse/id/219/thumbnail"
item5.has_online_content_ssim = ["Online access"]

item5.parent_ssim = ["schmuse"]
item5.parent_ssi = ["schmuse"]
item5.parent_levels_ssm = ["collection"]
item5.parent_unittitles_ssm = ["Steinmetz Digital Collection of Schenectady, c. 1860-1950"]
item5.parent_unittitles_teim = ["Steinmetz Digital Collection of Schenectady, c. 1860-1950"]
item5.component_level_isim = [1]
item5.collection_creator_ssm = ["Steinmetz, Charles Proteus, 1865-1923", "General Electric Company Publicity Department", "unknown", "General Electric Company", "Hayden, Joseph, b. 1906"]
item5.child_component_count_isim = [0]
#item5.parent_access_restrict_ssm = fields.ListField(str)
#item5.parent_access_terms_ssm = fields.ListField(str)
item5.title_filing_si = "Scotia Bridge"
item5.ref_ssm = ["schmuse-219"]
item5.ref_ssi = "schmuse-219"

collection1.components.append(item1)
collection1.components.append(item2)
collection1.components.append(item3)

collection2.components.append(item4)
collection2.components.append(item5)

print ("POSTing data to Solr...")
#print(collection1.to_struct())

solr.add([collection1.to_struct()])
solr.add([collection2.to_struct()])
