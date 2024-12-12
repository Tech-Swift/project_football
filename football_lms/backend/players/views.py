from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Player

class PlayerListView(ListView):
    model = Player
    template_name = 'players/player_list.html'
    context_object_name = 'players'

class PlayerDetailView(DetailView):
    model = Player
    template_name = 'players/player_detail.html'

class PlayerCreateView(CreateView):
    model = Player
    fields = ['name', 'position', 'team', 'age', 'coach']  # Specify fields here
    template_name = 'players/player_form.html'

    def get_success_url(self):
        return self.object.get_absolute_url()

class PlayerUpdateView(UpdateView):
    model = Player
    fields = ['name', 'position', 'team', 'age']  # Specify only the relevant fields here
    template_name = 'players/player_form.html'

class PlayerDeleteView(DeleteView):
    model = Player
    template_name = 'players/player_confirm_delete.html'
    success_url = reverse_lazy('players:player_list')
