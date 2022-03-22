from natasha import (

    PER,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    Doc,
    Segmenter,
    NewsNERTagger,
    NamesExtractor,
    DatesExtractor,
    MoneyExtractor,
    AddrExtractor
)
import itertools


class natasha_NLP:
    def __init__(self):
        self.segmenter = Segmenter()
        self.emb = NewsEmbedding()
        self.morph_tagger = NewsMorphTagger(self.emb)
        self.syntax_parcer = NewsSyntaxParser(self.emb)
        self.morph_vacab = MorphVocab()
        self.ner_tagger = NewsNERTagger(self.emb)
        self.names_extractor = NamesExtractor(self.morph_vacab)
        self.dates_extractor = DatesExtractor(self.morph_vacab)


    def doc_init(self, document):
        self.doc = Doc(document)
        self.doc.segment(self.segmenter)
        self.doc.tag_morph(self.morph_tagger)
        self.doc.parse_syntax(self.syntax_parcer)
        self.doc.tag_ner(self.ner_tagger)

    def get_lems(self):
        for token in self.doc.tokens:
            token.lemmatize(self.morph_vacab)
        return {_.text: _.lemma for _ in self.doc.tokens}

    def get_facts(self):
        self.get_lems()
        for span in self.doc.spans:
            span.normalize(self.morph_vacab)
        facts_2 = []
        for span in self.doc.spans:
            #if span.type == PER:
                #span.extract_fact(self.names_extractor)
                facts_2.append(span.normal)
        #facts = {_.normal: _.fact.as_dict for _ in self.doc.spans if _.type == PER}
        return list(set(facts_2))
    def get_all(self):
        extractors = [
            NamesExtractor(self.morph_vacab),
            AddrExtractor(self.morph_vacab),
            DatesExtractor(self.morph_vacab),
            MoneyExtractor(self.morph_vacab)
        ]
        spans = []
        facts = []
        for extractor in extractors:
            matches = extractor(self.doc)
            spans.extend(_.span for _ in matches)
            facts.extend(_.fact.as_json for _ in matches)
        return facts
    def print_ner(self):
        self.doc.ner.print()
        return