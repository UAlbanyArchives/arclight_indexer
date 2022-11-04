import json
import copy
import pysolr
from description_indexer.models.arclight import SolrCollection, SolrComponent

class Arclight():


    def __init__(self, solr_url):
        """
        Connects to an accessible Solr instance with pysolr.

        Parameters:
            solr_url(str): The url for a solr instance, such as http://solr.me.edu:8983/solr/my_core
        """

        self.solr = pysolr.Solr(solr_url, always_commit=True)
        self.solr.ping()
        

    def convert(self, record):

        has_online_content = set()

        print(f"converting to {record.id} to Solr documents...")
        solrDocument, has_online_content = self.convertCollection(record, has_online_content)
        
        if len(has_online_content) > 0:
            if solrDocument.id in has_online_content:
                solrDocument.has_online_content_ssim = ["true"]
            solrDocument = self.mark_online_content(solrDocument, has_online_content)

        return solrDocument

    def mark_online_content(self, solrComponent, has_online_content):
        
        for component in solrComponent.components:
            if component.ref_ssi in has_online_content:
                component.has_online_content_ssim = ["true"]
            childComponent = self.mark_online_content(component, has_online_content)

        return solrComponent


    def convertDigitalObjects(self, record, solrDocument):

        solrDocument.content_tesim = record.digital_objects[0].content
        solrDocument.content_teim = record.digital_objects[0].content
        solrDocument.thumbnail_href_ssm = record.digital_objects[0].thumbnail_href
        solrDocument.label_ssi = record.digital_objects[0].label
        solrDocument.dao_identifier_ssi = record.digital_objects[0].identifier
        solrDocument.is_representative_ssm = record.digital_objects[0].is_representative
        solrDocument.rights_statement_ssi = record.digital_objects[0].rights_statement
        solrDocument.access_subjects_ssim.extend(record.digital_objects[0].subjects)
        for field in record.digital_objects[0].metadata.keys():
            setattr(solrDocument, field + "_ssm", record.digital_objects[0].metadata[field])
        if hasattr(record.digital_objects[0], "iiif_manifest") and len(record.digital_objects[0].iiif_manifest) > 0:
            solrDocument.iiif_manifest_ssi = record.digital_objects[0].iiif_manifest
        else:
            fv_mappings = {
                "href": "hrefs_ssm",
                "mime_type": "mime_types_ssm",
                "filename": "filenames_ssm",
                "label": "file_labels_ssm",
                "is_access": "file_access_ssm",
                "is_original": "file_originals_ssm",
            }
            for file_version in record.digital_objects[0].file_versions:
                for desc_attr in fv_mappings.keys():
                    if getattr(file_version, desc_attr) is None:
                        getattr(solrDocument, fv_mappings[desc_attr]).append("")
                    else:
                        getattr(solrDocument, fv_mappings[desc_attr]).append(getattr(file_version, desc_attr))

        return solrDocument


    def convertCollection(self, record, has_online_content, recursive_level=0, parents=[], parent_titles=[], parent_levels=[], inherited_data={}):
        """
        A recursive function to convert collection and component objects to Arclight-friendly solr docs.
        It takes a component object and converts it and any child objects to an Arclight-friendly
        array of Solr docs.

        Parameters:
            record (Component): a hierarchical component object containing all public-facing description for a collection
            has_online_content (set):
            recursive_level (int): The level of recursion. Start at 0
            parents (list): A list of parent IDs as strings
            parent_titles (list): A list of parent names as strings
            parent_levels (list): A list of parent levels as strings
            inherited_data(dict): data inherited from upper-level ASpace API objects
                collection_name (list): The resource title
                child_component_count (int): The number of child components
                collection_creator (list): The collection-level creator as a list of strings
                parent_access_restrict (list): A list of access restriction paragraphs from the most immediate parent
                parent_access_terms (list): A list of use restriction paragraphs from the most immediate parent

        Returns:
            solrDocument (SolrCollection): a solr collection document containing nested solr component docs
        """

        if record.level == "collection":
            solrDocument = SolrCollection()
        else:
            solrDocument = SolrComponent()

        solrDocument.ead_ssi = [record.collection_id]
        solrDocument.collection_unitid_ssm = [record.collection_id]
        solrDocument.collection_unitid_teim = [record.collection_id]

        dates = []
        normalized_dates = []
        date_range = []
        for date in record.dates:
            if hasattr(date, "date_type") and date.date_type == "bulk":
                normalized_date = "bulk "
            else:
                normalized_date = ""
            if hasattr(date, "expression") and date.expression != None:
                dates.append(date.expression)
                normalized_date += date.expression
            elif hasattr(date, "end") and date.end != None:
                dates.append(f"{date.begin}-{date.end}")
                normalized_date = f"{normalized_date}{date.begin}-{date.end}"
            else:
                dates.append(date.begin)
                normalized_date += date.begin
            date_range.append(int(date.begin.split("-")[0]))
            if hasattr(date, "end") and date.end != None:
                date_range.append(int(date.end.split("-")[0]))
            normalized_dates.append(normalized_date)
        solrDocument.date_range_sim = date_range
        solrDocument.unitdate_ssm = dates
        solrDocument.normalized_date_ssm = [", ".join(normalized_dates)]

        solrDocument.title_ssm = [record.title]

        solrDocument.normalized_title_ssm = [f"{record.title}, {solrDocument.normalized_date_ssm[0]}"]
        solrDocument.collection_title_tesim = solrDocument.normalized_title_ssm
        if record.level == "collection":
            solrDocument.id = record.id.replace(".", "-")
            solrDocument.unitid_ssm = [record.collection_id]
            solrDocument.unitid_teim = [record.collection_id]
            solrDocument.collection_ssm = solrDocument.normalized_title_ssm
            solrDocument.collection_sim = solrDocument.normalized_title_ssm
            solrDocument.collection_ssi = solrDocument.normalized_title_ssm
            inherited_data['collection_name'] = solrDocument.normalized_title_ssm
            col_creators = []
            for col_creator in record.creators:
                col_creators.append(col_creator.name)
            inherited_data['collection_creator'] = col_creators

            new_parents = [record.collection_id.replace(".", "-")]
            new_parent_titles = solrDocument.normalized_title_ssm
            new_parent_levels = solrDocument.level_ssm
        else:
            record.component_level_isim = [recursive_level]

            #Arclight expects the collection id to be prepended to component ids but not to ref_ssm
            solrDocument.id = record.collection_id.replace(".", "-") + record.id.replace(".", "-")
            solrDocument.ref_ssi = record.id.replace(".", "-")
            # dunno why this is duplicated, but it seems to be like this in the default indexer
            solrDocument.ref_ssm = [record.id.replace(".", "-"), record.id.replace(".", "-")]
            solrDocument.collection_ssm = inherited_data['collection_name']
            solrDocument.collection_sim = inherited_data['collection_name']
            solrDocument.collection_ssi = inherited_data['collection_name']
            if "collection_creator" in inherited_data.keys():
                solrDocument.collection_creator_ssm = inherited_data['collection_creator']

            solrDocument.parent_ssim = parents
            #solrDocument.parent_ssm = parents
            # parent_ssi appears to be only the immediate parent
            if len(parents) > 0:
                solrDocument.parent_ssi = [parents[-1]]

            solrDocument.parent_unittitles_ssm = parent_titles
            solrDocument.parent_unittitles_teim = parent_titles
            solrDocument.parent_levels_ssm = parent_levels
            solrDocument.component_level_isim = [recursive_level]
            solrDocument.child_component_count_isim = [inherited_data["child_component_count"]]
            if "parent_access_restrict" in inherited_data.keys():
                solrDocument.parent_access_restrict_ssm = inherited_data["parent_access_restrict"]
            if "parent_access_terms" in inherited_data.keys():
                solrDocument.parent_access_terms_ssm = inherited_data["parent_access_terms"]

            new_parents = copy.deepcopy(parents)
            new_parents.append(record.id.replace(".", "-"))
            new_parent_titles = copy.deepcopy(parent_titles)
            new_parent_titles.append(solrDocument.normalized_title_ssm[0])
            new_parent_levels = copy.deepcopy(parent_levels)
            new_parent_levels.append(record.level)

        solrDocument.repository_ssm = [record.repository] #this is wrong locally
        solrDocument.repository_sim = [record.repository]

        solrDocument.level_ssm = [record.level.title()]
        solrDocument.level_sim = [record.level.title()]

        extents = []
        for extent in record.extents:
            extents.append(f"{extent.number} {extent.unit}")
        solrDocument.extent_ssm = extents

        if hasattr(record, "languages") and len(record.languages) > 0:
            solrDocument.language_ssm = [", ".join(record.languages)]

        # I think the ASpace Agent updates added many more of these that Arclight doesn't handle atm
        agent_translations = {
            "corporate_entity": "corpname_ssm",
            "family": "famname_ssm",
            "person": "persname_ssm"
        }
        # Agents are wonky in the default indexer which this recreates, but it should probably be thought out better. I don't have great data to do it right
        creators = []
        names = []
        for creator in record.creators:
            creators.append(creator.name)
            if creator.agent_type in agent_translations.keys():
                setattr(solrDocument, agent_translations[creator.agent_type], [creator.name])
                setattr(solrDocument, "creator_" + agent_translations[creator.agent_type], [creator.name])
                setattr(solrDocument, "creator_" + agent_translations[creator.agent_type].rsplit("_", 1)[0] + "_ssim", [creator.name])
            else:
                names.append(creator.name)
        solrDocument.creator_ssm = creators
        solrDocument.creator_ssim = creators
        solrDocument.creators_ssim = creators
        for name in record.names:
            names.append(name.name)
            if name.agent_type in agent_translations.keys():
                setattr(solrDocument, agent_translations[name.agent_type], [name.name])
        solrDocument.names_ssim = names
        # I stopped implementing this until agents are reworked, as its not used by the UI
        #solrDocument.names_coll_ssim

        # Seems imprecise, but this is how what the exiting indexer does.
        solrDocument.access_subjects_ssm = record.subjects
        solrDocument.access_subjects_ssim = record.subjects
        solrDocument.geogname_ssm = record.places
        solrDocument.geogname_sim = record.places
        solrDocument.places_sim = record.places
        solrDocument.places_ssm = record.places
        solrDocument.places_ssim = record.places

        # Notes
        note_translations = {
            "abstract": "abstract_ssm",
            "physloc": "physloc_ssm",
            "processinfo": "processinfo_ssm",
            "bioghist": "bioghist_ssm",
            "scopecontent": "scopecontent_ssm",
            "arrangement": "arrangement_ssm",
            "acqinfo": "acqinfo_ssim",
            "accessrestrict": "accessrestrict_ssm",
            "userestrict": "userestrict_ssm",
            "prefercite": "prefercite_ssm",
            "odd": "odd_ssm",
            "originalsloc": "originalsloc_ssm",
            "altformavail": "altformavail_ssm",
            "separatedmaterial": "separatedmaterial_ssm",
            "relatedmaterial": "relatedmaterial_ssm",
            "custodhist": "custodhist_ssm",
            "phystech": "phystech_ssm",
            "otherfindaid": "otherfindaid_ssm",
            "accruals": "accruals_ssm",
            "appraisal": "appraisal_ssm",
            "fileplan": "fileplan_ssm",
            "materialspec": "materialspec_ssm",
            "bibliography": "bibliography_ssm",
            "dimensions": "dimensions_ssm",
            "note ": "note_ssm"
        }
        for note in dir(record):
            if note in note_translations.keys():
                note_text = getattr(record, note)
                setattr(solrDocument, note_translations[note], note_text)
                if note == "accessrestrict":
                    inherited_data["parent_access_restrict"] = []
                    inherited_data["parent_access_restrict"].extend(note_text)
                if note == "userestrict":
                    inherited_data["parent_access_terms"] = []
                    inherited_data["parent_access_terms"].extend(note_text)

        # Containers
        # This is a bit nuts, but it was just as much code as a function so I left it explicit
        containers_ssim = []
        for container in record.containers:
            container_string = []
            if hasattr(container, "top_container") and container.top_container != None:
                container_string.append(container.top_container)
            if hasattr(container, "top_container_indicator") and container.top_container_indicator != None:
                container_string.append(container.top_container_indicator)
            if len(container_string) > 0:
                containers_ssim.append(" ".join(container_string))
            sub_container_string = []
            if hasattr(container, "sub_container") and container.sub_container != None:
                sub_container_string.append(container.sub_container)
            if hasattr(container, "sub_container_indicator") and container.sub_container_indicator != None:
                sub_container_string.append(container.sub_container_indicator)
            if len(sub_container_string) > 0:
                containers_ssim.append(" ".join(sub_container_string))
            sub_sub_container_string = []
            if hasattr(container, "sub_sub_container") and container.sub_sub_container != None:
                sub_sub_container_string.append(container.sub_sub_container)
            if hasattr(container, "sub_sub_container_indicator") and container.sub_sub_container_indicator != None:
                sub_sub_container_string.append(container.sub_sub_container_indicator)
            if len(sub_sub_container_string) > 0:
                containers_ssim.append(" ".join(sub_sub_container_string))
        solrDocument.containers_ssim = containers_ssim

        
        if len(record.digital_objects) < 1:
            has_dao = False
        elif len(record.digital_objects) == 1 and record.digital_objects[0].is_representative == "true":
            has_dao = True
            solrDocument = self.convertDigitalObjects(record, solrDocument)
        else:
            has_dao = True
            do_count = 0
            solrDocument.child_component_count_isim = [solrDocument.child_component_count_isim[0] + len(record.digital_objects)]
            for digital_object in record.digital_objects:
                dao_component = SolrComponent()
                dao_component.id = solrDocument.id + "-" + str(do_count)
                dao_component.component_level_isim = [solrDocument.component_level_isim[0] + 1]
                dao_component.ead_ssi = solrDocument.ead_ssi
                dao_component.level_ssm = ["Digital Object"]
                dao_component.repository_ssm = solrDocument.repository_ssm

                parent_ssims = solrDocument.parent_ssim
                parent_unittitles_ssm = solrDocument.parent_ssim
                ref_ssm = solrDocument.ref_ssm
                dao_component.parent_ssim = parent_ssims.append(solrDocument.id)
                dao_component.parent_unittitles_ssm = parent_unittitles_ssm.append(solrDocument.normalized_title)
                dao_component.ref_ssm = ref_ssm.append(solrDocument.id)

                # for now
                dao_component.normalized_date = solrDocument.normalized_date
                dao_component.normalized_title = solrDocument.normalized_title
                dao_component.title_ssm = solrDocument.title_ssm

                dao_component = self.convertDigitalObjects(record, dao_component)
                solrDocument.components.append(dao_component)
                do_count += 1
        
        if has_dao:
            has_online_content.add(record.id.replace(".", "-"))
            has_online_content.update(parents)

        # bump recursion level
        recursive_level += 1

        for component in record.components:
            inherited_data["child_component_count"] = len(component.components)
            subcomponent, has_online_content = self.convertCollection(component, has_online_content, recursive_level, new_parents, new_parent_titles, new_parent_levels, inherited_data)
            solrDocument.components.append(subcomponent)

        return solrDocument, has_online_content

    def post(self, collection):

        print ("POSTing data to Solr...")
        self.solr.add([collection.to_struct()])
        #print (json.dumps(collection.to_struct(), indent=4))