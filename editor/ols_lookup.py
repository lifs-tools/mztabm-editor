from typing import List
import functools
from ols_client.client import Client, EBIClient
import json

class OLSLookup:
    def __init__(self, ontologies, static_cv_terms):
        self.static_cv_terms = static_cv_terms
        assert len(self.static_cv_terms) == len(static_cv_terms), "number of static CV terms does not match!"
        self.client = EBIClient()
        self.ontologies = {}
        for ontology_key in ontologies:
            self.ontologies[ontology_key] = self.client.get_ontology(ontologies[ontology_key])

        assert len(self.ontologies) == len(ontologies), "number of ontologies does not match!"

# using functools.cache to cache the results of the function, since every call to .terms is a network call
    @functools.cache
    def resolve_ontology_term_name(self, ontology_key, term_obo_id):
        if ontology_key not in self.ontologies:
            return None
        
        if term_obo_id in self.static_cv_terms:
            return self.static_cv_terms[term_obo_id]["name"]

        terms = self.ontologies[ontology_key].terms(filters={'obo_id': term_obo_id})
        print(terms)
        if len(terms) == 1:
            return terms[0].name
        return None
    
    def search_term(self, ontology_keys: List[str], term_name: str) -> List[any]:
        response = self.client.suggest(query = term_name, ontology = ontology_keys)
        print(response)
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
        ontology_key = term_obo_id.split(":")[0]
        return self.resolve_ontology_term_name(ontology_key, term_obo_id)

    def resolve_term(self, term_obo_id, value=""):
        ontology_key = term_obo_id.split(":")[0]
        if ontology_key in self.ontologies:
            return self.resolve_ontology_term(ontology_key, term_obo_id, value)
        return None

    def quote_term_name(self, term_name):
        if "," in term_name:
            return f"\"{term_name}\""
        return term_name

    # using functools.cache to cache the results of the function, since every call to .terms is a network call
    @functools.cache
    def resolve_ontology_term(self, ontology_key, term_obo_id, term_value=""):
        if ontology_key not in self.ontologies:
            return None
        
        if term_obo_id in self.static_cv_terms:
            value = self.static_cv_terms[term_obo_id]["value"]
            if value is None:
                value = ""
            return f"[{self.static_cv_terms[term_obo_id]['cv']}, {self.static_cv_terms[term_obo_id]['term_obo_id']}, {self.static_cv_terms[term_obo_id]['name']}, {value}]"

        terms = self.ontologies[ontology_key].terms(filters={'obo_id': term_obo_id})
        
        if len(terms) == 1:
            quoted_name = terms[0].name
            if "," in terms[0].name:
                quoted_name = f"\"{quoted_name}\""
            return f"[{self.ontologies[ontology_key].namespace.upper()}, {term_obo_id}, {quoted_name}, {term_value}]"
        return None

#@st.cache_resource()
#def ols_lookup(ontologies, static_cv_terms):
#    return OLSLookup(ontologies, static_cv_terms)