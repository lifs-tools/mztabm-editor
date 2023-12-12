#from ebi.ols.api.client import OlsClient
import json
from typing import List
import functools

import streamlit as st

class OLSLookup:
    def __init__(self, ontologies, static_cv_terms):
        self.staticCvTerms = static_cv_terms

        assert len(self.staticCvTerms) == len(static_cv_terms), "number of static CV terms does not match!"
        #self.client = OlsClient()
        self.ontologies = {}
        for ontologyKey in ontologies:
            self.ontologies[ontologyKey] = self.client.ontology(ontologies[ontologyKey])

        assert len(self.ontologies) == len(ontologies), "number of ontologies does not match!"

# using functools.cache to cache the results of the function, since every call to .terms is a network call
    @functools.cache
    def resolve_ontology_term_name(self, ontologyKey, term_obo_id):
        if ontologyKey not in self.ontologies:
            return None
        
        if term_obo_id in self.staticCvTerms:
            return self.staticCvTerms[term_obo_id]["name"]

        terms = self.ontologies[ontologyKey].terms(filters={'obo_id': term_obo_id})
        
        if len(terms) == 1:
            return terms[0].name
        return None
    
    def search_term(self, ontology_keys: List[str], term_name: str) -> List[any]:
        # return wikipedia.search(searchterm) if searchterm else []
        # for ontologyKey in ontology_keys:
        #     terms = self.ontologies[ontologyKey].terms(filters={'name': term_name})
        #     if len(terms) == 1:
        #         return terms[0].obo_id
        # return None
        return None
    
    # def get_child_terms(self, ontologyKey, term_obo_id):
    #     if ontologyKey not in self.ontologies:
    #         return None
    #     self.client.search(ontologyKey, term_obo_id)
    #     terms = self.ontologies[ontologyKey].children(term_obo_id)
    #     return terms

    def resolve_term_name(self, term_obo_id):
        ontologyKey = term_obo_id.split(":")[0]
        return self.resolve_ontology_term_name(ontologyKey, term_obo_id)

    def resolve_term(self, term_obo_id, value=""):
        ontologyKey = term_obo_id.split(":")[0]
        if ontologyKey in self.ontologies:
            return self.resolve_ontology_term(ontologyKey, term_obo_id, value)
        return None

    def quote_term_name(self, term_name):
        if "," in term_name:
            return f"\"{term_name}\""
        return term_name

    # using functools.cache to cache the results of the function, since every call to .terms is a network call
    @functools.cache
    def resolve_ontology_term(self, ontologyKey, term_obo_id, term_value=""):
        if ontologyKey not in self.ontologies:
            return None
        
        if term_obo_id in self.staticCvTerms:
            value = self.staticCvTerms[term_obo_id]["value"]
            if value == None:
                value = ""
            return f"[{self.staticCvTerms[term_obo_id]['cv']}, {self.staticCvTerms[term_obo_id]['term_obo_id']}, {self.staticCvTerms[term_obo_id]['name']}, {value}]"

        terms = self.ontologies[ontologyKey].terms(filters={'obo_id': term_obo_id})
        
        if len(terms) == 1:
            quotedName = terms[0].name
            if "," in terms[0].name:
                quotedName = f"\"{quotedName}\""
            return f"[{self.ontologies[ontologyKey].namespace.upper()}, {term_obo_id}, {quotedName}, {term_value}]"
        return None

#@st.cache_resource()
#def ols_lookup(ontologies, static_cv_terms):
#    return OLSLookup(ontologies, static_cv_terms)