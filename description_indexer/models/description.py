from jsonmodels import models, fields, errors, validators

"""
This is designed to be an as-simple-as-possible data model
for public-facing archival description that is neccessary
for an access and discovery system
"""

class Date(models.Base):
    expression = fields.StringField(required=True)
    begin = fields.StringField(required=True)
    end = fields.StringField()
    date_type = fields.StringField()

class Extent(models.Base):
    number = fields.StringField(required=True)
    unit = fields.StringField(required=True)

class Agent(models.Base):
    # Should be built out more but I don't have access to good agent data
    name = fields.StringField(required=True)
    agent_type = fields.StringField(required=True)

class Container(models.Base):
    top_container = fields.StringField()
    top_container_indicator = fields.StringField()
    sub_container = fields.StringField()
    sub_container_indicator = fields.StringField()
    sub_sub_container = fields.StringField()
    sub_sub_container_indicator = fields.StringField()

class FileVersion(models.Base):
    href = fields.StringField(required=True)
    label = fields.StringField()
    filename = fields.StringField()
    is_access = fields.StringField()
    is_original = fields.StringField()
    mime_type = fields.StringField()

class File(models.Base):
    # This is also a pcdm:File
    identifier = fields.StringField(required=True)
    label = fields.StringField()
    thumbnail_href = fields.StringField()
    # Searchable text or transcription content
    content = fields.StringField()
    versions = fields.ListField(FileVersion)

class DigitalObject(models.Base):
    # This is also a pcdm:Object
    # In EAD and ASpace
    uri = fields.StringField()
    label = fields.StringField(required=True)
    identifier = fields.StringField(required=True)
    # In ASpace, not EAD
    # As in "Is this representative of the entire component?"
    is_representative = fields.StringField(required=True)

    # Not typically managed with description
    #fulfillment stuff
    thumbnail_href = fields.StringField()
    rights_statement = fields.StringField()
    #digital object-level metadata
    metadata = fields.DictField()
    subjects = fields.ListField(str)

    files = fields.ListField(File)
    

class Component(models.Base):
    id = fields.StringField(required=True)
    collection_id = fields.StringField(required=True)
    title = fields.StringField(required=True)
    title_filing_si = fields.StringField()
    repository = fields.StringField(required=True)
    level = fields.StringField(required=True)
    collection_name = fields.StringField(required=True)
    dates = fields.ListField(Date)
    extents = fields.ListField(Extent)
    languages = fields.ListField(str)
    creators = fields.ListField(Agent)
    names = fields.ListField(Agent)
    subjects = fields.ListField(str)
    places = fields.ListField(str)
    abstract = fields.ListField(str)
    accessrestrict = fields.ListField(str)
    scopecontent = fields.ListField(str)
    acqinfo = fields.ListField(str)
    accruals = fields.ListField(str)
    altformavail = fields.ListField(str)
    appraisal = fields.ListField(str)
    arrangement = fields.ListField(str)
    bibliography = fields.ListField(str)
    bioghist = fields.ListField(str)
    custodhist = fields.ListField(str)
    fileplan = fields.ListField(str)
    note = fields.ListField(str)
    odd = fields.ListField(str)
    originalsloc = fields.ListField(str)
    otherfindaid = fields.ListField(str)
    phystech = fields.ListField(str)
    prefercite = fields.ListField(str)
    processinfo = fields.ListField(str)
    relatedmaterial = fields.ListField(str)
    separatedmaterial = fields.ListField(str)
    userestrict = fields.ListField(str)
    materialspec = fields.ListField(str)
    physloc = fields.ListField(str)

    containers = fields.ListField(Container)
    digital_objects = fields.ListField(DigitalObject)
    components = fields.ListField()
    # this should actually be a component attribute since its an aggregate
    iiif_manifest = fields.StringField()
