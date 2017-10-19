from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View

from .forms import (
    NewPieceForm,
    SelectRulesForm
)
from .models import (
    MusicPiece
)
from .harmony_rules import check_harmony_rules

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
            "pieces": MusicPiece.objects.all()
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
            return render(request, 
                          'check_piece.html', 
                          {'piece':checked_piece, 'form' : SelectRulesForm()})

        

