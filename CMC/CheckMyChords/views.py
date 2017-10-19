from django.shortcuts import render
from django.http.response import (
    HttpResponse, 
    HttpResponseRedirect,
    JsonResponse,
)
from django.urls import reverse
from django.views import View

from .forms import (
    NewPieceForm,
    SelectRulesForm
)
from .models import (
    MusicPiece
)
from .harmony_rules import check_harmony_rules, make_piece
from pyknon.genmidi import Midi
from pyknon.music import NoteSeq

import os
from CMC.settings import MEDIA_ROOT, MEDIA_URL

# Create your views here.

class HelloWorldView(View):
    def get(self, request):
        return HttpResponse('Hello world!')
    

class AddPieceView(View):
    # Lets You add a new piece manually, strings as an input
    def get(self, request):
        form = NewPieceForm()
        return render(request, 'new_piece.html', {'form':form})
 
    def post(self, request):
        form = NewPieceForm(request.POST)
        if form.is_valid():
            new_piece = MusicPiece.objects.create(**form.cleaned_data)
            return HttpResponseRedirect(
                reverse("check_piece", kwargs = {"piece_id":new_piece.id})
            )
        else:
            return render(request, 'new_piece.html', {'form':form})
    
class PiecesView(View):
    def get(self, request):
        
        ctx = {
            "pieces": MusicPiece.objects.all(),
        }
        return render(request, 'pieces.html', ctx)

class CheckPieceView(View):
    def get(self, request, piece_id):
        piece = MusicPiece.objects.get(id=piece_id)
        checked_piece = check_harmony_rules(piece)
        return render(request, 'check_piece.html', {'piece': checked_piece,
                                                    'form': SelectRulesForm()})
    
    def post(self, request, piece_id):
        # Check the piece, but only using the rules chosen in form
        form = SelectRulesForm(request.POST)
        if form.is_valid():
            piece = MusicPiece.objects.get(id=piece_id)
            rules = form.cleaned_data['rules']
            checked_piece = check_harmony_rules(piece, rules)
            # checked_piece is a Piece object, while piece is MusicPiece object
            return render(request, 
                          'check_piece.html', 
                          {'piece':checked_piece, 'form' : SelectRulesForm()})

class GenerateMidiView(View):
    # used to create MIDI file from piece in db. MIDI is generated and uploaded
    # only if user requests it
    def get(self, request, piece_id):
        piece = MusicPiece.objects.get(id=piece_id)
        piece = make_piece(piece)
        filename = '{}_{}.mid'.format(piece_id, piece.title)
        # if file exists, don't generate it again - as it's
        # not possible to modify piece in current version
        if not os.path.isfile(os.path.join(MEDIA_ROOT,filename)):
            # file doesn't exist - generate it!
            m = Midi(4, tempo=90)
            for idx, voice in enumerate(piece.parts):
                m.seq_notes(piece.parts[voice], idx)
            m.write(os.path.join(MEDIA_ROOT, filename))
        url = os.path.join(MEDIA_URL, filename)
        return JsonResponse({"url": url})
