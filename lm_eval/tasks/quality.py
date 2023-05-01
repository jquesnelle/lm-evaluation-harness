"""
QuALITY: Question Answering with Long Input Texts, Yes!
https://arxiv.org/pdf/2112.08608.pdf

QuALITY is a multiple-choice QA dataset with
context passages in English that have an average length 
of about 5,000 tokens.

Homepage: https://github.com/nyu-mll/quality
"""
from lm_eval.base import MultipleChoiceTask


_CITATION = """
@inproceedings{pang-etal-2022-quality,
    title = "{Q}u{ALITY}: Question Answering with Long Input Texts, Yes!",
    author = "Pang, Richard Yuanzhe  and
      Parrish, Alicia  and
      Joshi, Nitish  and
      Nangia, Nikita  and
      Phang, Jason  and
      Chen, Angelica  and
      Padmakumar, Vishakh  and
      Ma, Johnny  and
      Thompson, Jana  and
      He, He  and
      Bowman, Samuel",
    booktitle = "Proceedings of the 2022 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies",
    month = jul,
    year = "2022",
    address = "Seattle, United States",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2022.naacl-main.391",
    pages = "5336--5358",
    abstract = "To enable building and testing models on long-document comprehension, we introduce QuALITY, a multiple-choice QA dataset with context passages in English that have an average length of about 5,000 tokens, much longer than typical current models can process. Unlike in prior work with passages, our questions are written and validated by contributors who have read the entire passage, rather than relying on summaries or excerpts. In addition, only half of the questions are answerable by annotators working under tight time constraints, indicating that skimming and simple search are not enough to consistently perform well. Our baseline models perform poorly on this task (55.4{\%}) and significantly lag behind human performance (93.5{\%}).",
}
"""


class QuALITY(MultipleChoiceTask):
    VERSION = 0
    DATASET_PATH = "emozilla/quality"
    DATASET_NAME = None

    def has_training_docs(self):
        return True

    def has_validation_docs(self):
        return True

    def has_test_docs(self):
        return False

    def training_docs(self):
        if self._training_docs is None:
            self._training_docs = list(map(self._process_doc, self.dataset["train"]))
        return self._training_docs

    def validation_docs(self):
        return map(self._process_doc, self.dataset["validation"])

    def _process_doc(self, doc):
        out_doc = {
            "article": doc["article"],
            "query": doc["question"],
            "choices": doc["options"],
            "gold": doc["answer"],
        }
        return out_doc

    def doc_to_text(self, doc):
        return "{}\nQuestion: {}\nAnswer:".format(doc["article"], doc["query"])

    def should_decontaminate(self):
        return True

    def doc_to_decontamination_query(self, doc):
        return doc["article"] + " " + doc["query"]

class QuALITYPruned4K(QuALITY):
    DATASET_PATH = "emozilla/quality-pruned-llama-gptneox-4k"

class QuALITYPruned8K(QuALITY):
    DATASET_PATH = "emozilla/quality-pruned-llama-gptneox-8k"