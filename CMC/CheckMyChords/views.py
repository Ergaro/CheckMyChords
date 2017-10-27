from os import path

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http.response import (
    HttpResponse, 
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View

from pyknon.genmidi import Midi
from pyknon.music import NoteSeq

from CMC.settings import MEDIA_ROOT, MEDIA_URL
from .forms import (
    NewPieceForm,
    SelectRulesForm
)
from .harmony_rules import check_harmony_rules, make_piece
from .models import MusicPiece


class SignUpView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'signup.html', {"form": form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            raw_pass = form.cleaned_data['password1']
            user = authenticate(username=username, password=raw_pass)
            login(request, user)
            messages.add_message(
                request,
                messages.SUCCESS,
                'User {} created succesfully'.format(username),
            )
            return redirect("pieces")
        else:
            return render(request, 'signup.html', {'form': form})

class AddPieceView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")
    # Lets You add a new piece manually, strings as an input
    def get(self, request):
        form = NewPieceForm()
        return render(request, 'new_piece.html', {'form':form})
 
    def post(self, request):
        form = NewPieceForm(request.POST)
        if form.is_valid():
            author = request.user
            new_piece = MusicPiece.objects.create(author = author,
                                                  **form.cleaned_data)
            return HttpResponseRedirect(
                reverse("check_piece", kwargs = {"piece_id":new_piece.id})
            )
        else:
            return render(request, 'new_piece.html', {'form':form})
    
class PiecesView(View):
    # Shows all pieces from db, enables checking them and downloading MIDI
    def get(self, request):
        if request.user.is_superuser:
            pieces = MusicPiece.objects.all()
        elif request.user.is_authenticated:
            pieces = MusicPiece.objects.filter(
                Q(author=request.user) | Q(is_public=True),
            )
        else:
            pieces = MusicPiece.objects.filter(is_public=True)
        ctx = {
            "pieces": pieces,
        }
        return render(request, 'pieces.html', ctx)

class CheckPieceView(View):
    # Shows if piece is correct, according to basic harmony rules
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
        if not request.user.is_authenticated:
            return JsonResponse({"url": reverse("login"),
                                 "type": "redirect"})
        piece = MusicPiece.objects.get(id=piece_id)
        # check if user has permission to download this file (in case JS was
        # modified). This doesn't prevent user from downloading file
        # via entering /media/<filename> url if the midi file has been already
        # generated (but such desperate must know not only the ID, but also
        # the title)
        if not (piece.is_public or piece.author == request.user):
            return JsonResponse({"url": reverse("login"),
                                 "type": "redirect"})
        piece = make_piece(piece)
        filename = '{}_{}.mid'.format(piece_id, piece.title)
        # if file exists, don't generate it again - as it's
        # not possible to modify piece in current version
        if not path.isfile(path.join(MEDIA_ROOT,filename)):
            # file doesn't exist - generate it!
            m = Midi(4, tempo=90)
            for idx, voice in enumerate(piece.parts):
                m.seq_notes(piece.parts[voice], idx)
            m.write(path.join(MEDIA_ROOT, filename))
        url = path.join(MEDIA_URL, filename)
        return JsonResponse({"url": url,
                             "type": "file"})

