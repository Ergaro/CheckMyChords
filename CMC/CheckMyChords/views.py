from django.shortcuts import render
from django.http.response import HttpResponse
from django.views import View

from .forms import (
    NewPieceForm,
)
from .models import (
    MusicPiece
)
from .harmony_rules import check_harmony_rules

# Create your views here.

class HelloWorldView(View):
    def get(self, request):
        return HttpResponse('Hello world!')
    

class CheckNewPieceView(View):
    def get(self, request):
        form = NewPieceForm()
        return render(request, 'new_piece.html', {'form':form})
 
    def post(self, request):
        form = NewPieceForm(request.POST)
        if form.is_valid():
            # Save piece to database
            new_piece = MusicPiece.objects.create(**form.cleaned_data)
            # Check harmony rules
            checked_piece = check_harmony_rules(new_piece)
            # checked_piece is a Piece object, not MusicPiece object!!!
            #     the results are stored in checked_piece
            
            # Get&Present result (redirect to sth?)
            result = "the piece was checked, result: {} errors, {}".format(checked_piece.err_count, checked_piece.err_w_types)

            return HttpResponse(result)
        else:
            return render(request, 'new_piece.html', {'form':form})
    


