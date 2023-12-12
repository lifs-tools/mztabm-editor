from collections import OrderedDict
from editor.ols_lookup import OLSLookup
from natsort import natsorted
import pandas as pd
from pandas import isnull
from pygoslin.parser.Parser import LipidParser
from numpy import mean, std
# mztabm class for mzTab-M files
# supports creation of the metadata and summary table sections

# create a python class for mzTab-M files
class MzTabM:

    staticCvTerms = {}
    ontologies = {}

    """Class to create mzTab-M files from a config.json file and additional csv tables for mztab-head.csv, contacts.csv, databases.csv, instruments.csv, publications.csv, softwares.csv and id_and_quant.csv."""
    def __init__(self, config, mztab_head, contacts, databases, instruments, publications, softwares, id_and_quant):
        self.config = config
        self.mztab_head = mztab_head
        self.contacts = contacts
        self.databases = databases
        self.instruments = instruments
        self.publications = publications
        self.softwares = softwares
        self.id_and_quant = id_and_quant
        self.ols_lookup = OLSLookup(self.config["ontologies"], self.config["static_cv_terms"])

    def write_mztabm(self, input_file, input_file_sheet, firstLipidColumnIndex, output_file):
        print("Writing mzTab file to", output_file, "from", input_file, "sheet", input_file_sheet, "...")

        df = pd.read_excel(input_file, input_file_sheet, index_col = "Sample")
        df = df.reindex(index=natsorted(df.index))
        df.insert(0, 'Sample', df.index)

        studyVariables = df["StudyVariable"].unique()
        samples = df["Sample"]
        sampleSpecies = {}
        if "Species" in df.columns:
            sampleSpecies = df["Species"].map(lambda x: x.split("|"))

        sampleTissues = {}  
        if "Tissue" in df.columns:
            sampleTissues = df["Tissue"].map(lambda x: x.split("|"))

        sampleDiseases = {}
        if "Disease" in df.columns:
            sampleDiseases = df["Disease"].map(lambda x: x.split("|"))

        sampleCellTypes = {}
        if "CellType" in df.columns:
            sampleCellTypes = df["CellType"].map(lambda x: x.split("|"))

        sampleGender = {}
        if "Gender" in df.columns:
            sampleGender = df["Gender"].map(lambda x: x.split("|"))

        sample_to_sample_pos = {}
        assay_to_msrun_pos = {}
        sample_to_assay_pos = {}    
        mztabHead = pd.read_csv(self.mztab_head, sep=",")
        mtdHead = self.create_mtd_head(mztabHead)
        self.create_id_and_quant(mtdHead)
        self.create_publications(mtdHead)
        self.create_contacts(mtdHead)
        self.create_ontologies(mtdHead)
        self.create_samples(samples, sampleSpecies, sampleTissues, sampleDiseases, sampleCellTypes, sampleGender, mtdHead, sample_to_sample_pos)
        self.create_ms_runs(samples, mtdHead, assay_to_msrun_pos)
        self.create_assays(samples, mtdHead, assay_to_msrun_pos, sample_to_assay_pos)
        self.create_study_variables(df, studyVariables, mtdHead, sample_to_assay_pos)
        self.create_instruments(mtdHead)
        self.create_softwares(mtdHead)
        self.create_databases(mtdHead)

        lipids = [col for i, col in enumerate(df) if i >= firstLipidColumnIndex]
        lipid_parser = LipidParser()

        with open(output_file, "wt") as mz:
            mz.writelines(f'{s}\n' for s in mtdHead)
            smlColums = [
                "SMH",
                "SML_ID",
                "SMF_ID_REFS",
                "chemical_name",
                "database_identifier",
                "chemical_formula",
                "smiles",
                "inchi",
                "uri",
                "theoretical_neutral_mass",
                "adduct_ions",
                "reliability",
                "best_id_confidence_measure",
                "best_id_confidence_value"
            ]
            smlColums.extend(["abundance_assay[%i]" % i for i in range(1, len(samples) + 1)])
            for j, studyVariableValue in enumerate(studyVariables):
                    j += 1
                    smlColums.extend(["abundance_study_variable[%i]" % j, "abundance_variation_study_variable[%i]" % j])

            mz.write("\t".join(smlColums)+"\n")
            
            for i, lipid_name in enumerate(lipids):
                i += 1
                goslin_lipid_name = lipid_name
                normalized_lipid_name = lipid_name
                theoretical_neutral_mass = "null"
                concentrations = "\t".join([str(val) for val in df[lipid_name]])
                concentrations = concentrations.replace("nan", "null")
                # print(lipid_name, concentrations)
                sv_assay_values = []
                for j, studyVariableValue in enumerate(studyVariables):
                    j += 1
                    sampleIds = df[df["StudyVariable"]==studyVariableValue]["Sample"]
                    sv_mean = str(mean(df.loc[sampleIds, lipid_name])).replace("nan", "null")
                    sv_std = str(std(df.loc[sampleIds, lipid_name])).replace("nan", "null")
                    sv_assay_values.extend([sv_mean, sv_std])
                
                sv_assay_values_str = "\t".join(sv_assay_values)
                try:
                    lipid = lipid_parser.parse(lipid_name)
                    normalized_lipid_name = lipid.get_lipid_string()
                    goslin_lipid_name = f"goslin:{normalized_lipid_name}"
                    theoretical_neutral_mass = f"{round(lipid.get_mass(),4):.4f}"
                except:
                    pass
                
                mz.write("SML	%i	null	%s	%s	null	null	null	null	%s	null	3	[MS,MS:1002890,fragmentation score,]	1.0	%s	%s\n" % (i, normalized_lipid_name, goslin_lipid_name, theoretical_neutral_mass, concentrations, sv_assay_values_str))

    def create_databases(self, mtdHead):
        databases = pd.read_csv(self.databases, sep=",", index_col="id")

        databaseRows = []
        for i, database in databases.iterrows():
            item = f"database[{i}]"
            value = ""
            if "cv_term" in database and not isnull(database["cv_term"]):
                dbTerm = self.ols_lookup.resolve_term(database['cv_term'], value)
                if dbTerm != None:
                    databaseRows.append(f"MTD\t{item}\t{dbTerm}")
                else:
                    databaseRows.append(f"MTD\t{item}\t{database['cv_term']}")
            elif "name" in database and not isnull(database["name"]):
                databaseRows.append(f"MTD\t{item}\t[,,{self.ols_lookup.quote_term_name(database['name'])},{value}]")
            else:
                databaseRows.append(f"MTD\t{item}\t[,,\"no database\",null]")
            
            if "prefix" in database and not isnull(database["prefix"]):
                databaseRows.append(f"MTD\t{item}-prefix\t{database['prefix']}")
            if "version" in database and not isnull(database["version"]):
                databaseRows.append(f"MTD\t{item}-version\t{database['version']}")
            else:
                databaseRows.append(f"MTD\t{item}-version\tUnknown")
            if "uri" in database and not isnull(database["uri"]):
                databaseRows.append(f"MTD\t{item}-uri\t{database['uri']}")
            else:
                databaseRows.append(f"MTD\t{item}-uri\tnull")

        mtdHead.extend(databaseRows)

    def create_softwares(self, mtdHead):
        softwares = pd.read_csv(self.softwares, sep=",", index_col="id")
        softwareRows = []
        for i, software in softwares.iterrows():
            item = f"software[{i}]"
            value = ""
            if "value" in software and not isnull(software["value"]):
                value = software["value"]
            if "cv_term" in software and not isnull(software["cv_term"]):
                softwareRows.append(f"MTD\t{item}\t{self.ols_lookup.resolve_term(software['cv_term'], value)}")
            elif "name" in software and not isnull(software["name"]):
                softwareRows.append(f"MTD\t{item}\t[,,{self.ols_lookup.quote_term_name(software['name'])},{value}]")
            
            if "setting" in software and not isnull(software["setting"]):
                for setting in software["setting"].split("|"):
                    softwareRows.append(f"MTD\t{item}-setting\t{setting}")

        mtdHead.extend(softwareRows)

    def create_instruments(self, mtdHead):
        instrumentRows = []
        instruments = pd.read_csv(self.instruments, sep=",", index_col="id")

        instrumentRows = []
        for i, instrument in instruments.iterrows():
            item = f"instrument[{i}]"
            value = ""
            if "name" in instrument and not isnull(instrument["name"]):
                instrumentRows.append(f"MTD\t{item}-name\t{self.ols_lookup.resolve_term(instrument['name'])}")
            if "source" in instrument and not isnull(instrument["source"]):
                instrumentRows.append(f"MTD\t{item}-source\t{self.ols_lookup.resolve_term(instrument['source'])}")
            if "analyzer" in instrument and not isnull(instrument["analyzer"]):
                instrumentRows.append(f"MTD\t{item}-analyzer\t{self.ols_lookup.resolve_term(instrument['analyzer'])}")
            if "detector" in instrument and not isnull(instrument["detector"]):
                instrumentRows.append(f"MTD\t{item}-detector\t{self.ols_lookup.resolve_term(instrument['detector'])}")

        mtdHead.extend(instrumentRows)

    def create_study_variables(self, df, studyVariables, mtdHead, sample_to_assay_pos):
        studyVariableRows = []
        for i, studyVariableValue in enumerate(studyVariables):
            i += 1
            sampleIds = df[df["StudyVariable"]==studyVariableValue]["Sample"].astype(str).tolist()
            assayIds = "|".join(["assay["+str(sample_to_assay_pos[x])+"]" for x in sampleIds])
            studyVariableRows.append(f"MTD\tstudy_variable[{i}]\t{studyVariableValue}")
            studyVariableRows.append(f"MTD\tstudy_variable[{i}]-description\t{studyVariableValue}")
            studyVariableRows.append(f"MTD\tstudy_variable[{i}]-assay_refs\t{assayIds}")

        mtdHead.extend(studyVariableRows)

    def create_assays(self, samples, mtdHead, assay_to_msrun_pos, sample_to_assay_pos):
        assayRows = []
        for i, sample in enumerate(samples):
            i += 1
            sample_to_assay_pos[sample] = i
            assayRows.append(f"MTD\tassay[{i}]\tAssay for Sample no {sample}")
            assayRows.append(f"MTD\tassay[{i}]-sample_ref\tsample[{i}]")
            assayRows.append(f"MTD\tassay[{i}]-ms_run_ref\tms_run[{assay_to_msrun_pos[sample]}]")

        mtdHead.extend(assayRows)

    def create_ms_runs(self, samples, mtdHead, assay_to_msrun_pos):
        msRunRows = []
        for i, sample in enumerate(samples):
            i += 1
            assay_to_msrun_pos[sample] = i
            msRunRows.append(f"MTD\tms_run[{i}]-location\tfile://Sample_no_{sample}.mzML")
            msRunRows.append(f"MTD\tms_run[{i}]-scan_polarity[1]\t[MS, MS:1000130, positive scan, ]")
            
        mtdHead.extend(msRunRows)

    def create_samples(self, samples, sampleSpecies, sampleTissues, sampleDiseases, sampleCellTypes, sampleGender, mtdHead, sample_to_sample_pos):
        sampleRows = []

        for i, sample in enumerate(samples):
            i += 1
            sample_to_sample_pos[sample] = i
            sampleRows.append(f"MTD\tsample[{i}]\tSample no. {sample}")
            if len(sampleSpecies) > 0:
                for j, species in enumerate(sampleSpecies[sample]):
                    j += 1
                    sampleRows.append(f"MTD\tsample[{i}]-species[{j}]\t{self.ols_lookup.resolve_term(species)}")
            if len(sampleTissues) > 0:
                for j, tissue in enumerate(sampleTissues[sample]):
                    j += 1
                    sampleRows.append(f"MTD\tsample[{i}]-tissue[{j}]\t{self.ols_lookup.resolve_term(tissue)}")
            if len(sampleDiseases) > 0:
                for j, disease in enumerate(sampleDiseases[sample]):
                    j += 1
                    sampleRows.append(f"MTD\tsample[{i}]-disease[{j}]\t{self.ols_lookup.resolve_term(disease)}")
            if len(sampleCellTypes) > 0:
                for j, cellType in enumerate(sampleCellTypes[sample]):
                    j += 1
                    sampleRows.append(f"MTD\tsample[{i}]-cell_type[{j}]\t{self.ols_lookup.resolve_term(cellType)}")
            if len(sampleGender) > 0:
                for j, gender in enumerate(sampleGender[sample]):
                    j += 1
                    sampleRows.append(f"MTD\tsample[{i}]-custom[{j}]\t[NCIT, NCIT:C17357, Gender, {self.ols_lookup.resolve_term_name(gender)}]")

        mtdHead.extend(sampleRows)

    def create_ontologies(self, mtdHead):
        ontologyRows = []
        for i, ontology in enumerate(self.ontologies):
            i += 1
            ontologyRows.append(f"MTD\tcv[{i}]-label\t{ontology}")
            ontologyRows.append(f"MTD\tcv[{i}]-uri\t{self.ontologies[ontology].config.id}")
            if self.ontologies[ontology].config.version == None:
                ontUpdDate = self.ontologies[ontology].updated.split("T")[0]
                ontologyRows.append(f"MTD\tcv[{i}]-version\t{ontUpdDate}")
            else:
                ontologyRows.append(f"MTD\tcv[{i}]-version\t{self.ontologies[ontology].config.version}")
            ontologyRows.append(f"MTD\tcv[{i}]-full_name\t{self.ontologies[ontology].title}")

        mtdHead.extend(ontologyRows)

    def create_contacts(self, mtdHead):
        contacts = pd.read_csv(self.contacts, sep=",", index_col="id")

        contactRows = []
        for i, contact in contacts.iterrows():
            item = f"contact[{i}]"
            if "name" in contact and not isnull(contact["name"]):
                contactRows.append(f"MTD\t{item}-name\t{contact['name']}")
            if "affiliation" in contact and not isnull(contact["affiliation"]):
                contactRows.append(f"MTD\t{item}-affiliation\t{contact['affiliation']}")
            if "email" in contact and not isnull(contact["email"]):
                contactRows.append(f"MTD\t{item}-email\t{contact['email']}")
            if "orcid" in contact and not isnull(contact["orcid"]):
                contactRows.append(f"MTD\t{item}-orcid\t{contact['orcid']}")

        mtdHead.extend(contactRows)

    def create_publications(self, mtdHead):
        publications = pd.read_csv(self.publications, sep=",", index_col="id")
        publications

        publicationRows = []
        for i, publication in publications.iterrows():
            item = f"publication[{i}]"
            if "identifier" in publication:
                publicationRows.append(f"MTD\t{item}\t{publication['identifier']}")

        mtdHead.extend(publicationRows)

    def create_id_and_quant(self, mtdHead):
        quantifications = pd.read_csv(self.id_and_quant, sep=",")

        quantificationRows = []
        for i, quantification in quantifications.iterrows():
            for column in quantification.keys():
                print(quantification[column])
                quantificationRows.append(f"MTD\t{column}\t{self.ols_lookup.resolve_term(quantification[column])}")

        mtdHead.extend(quantificationRows)

    def create_mtd_head(self, mztabHead):
        mtdHead = []
        mtdHead.append(f"MTD\tmzTab-version\t{mztabHead['mztabversion'][0]}")
        mtdHead.append(f"MTD\tmzTab-ID\t{mztabHead['mztabid'][0]}")
        mtdHead.append(f"MTD\ttitle\t{mztabHead['title'][0]}")
        mtdHead.append(f"MTD\tdescription\t{mztabHead['description'][0]}")
        return mtdHead
