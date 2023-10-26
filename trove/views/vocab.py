from django import http
from django.views import View

from trove.render import render_response
from trove.vocab.namespaces import TROVE
from trove.vocab.trove import TROVE_API_VOCAB


class TroveVocabView(View):
    def get(self, request, vocab_term):
        _iri = TROVE[vocab_term]
        try:
            _data = {_iri: TROVE_API_VOCAB[_iri]}
        except KeyError:
            raise http.Http404
        else:
            return render_response(request, _data, _iri)
