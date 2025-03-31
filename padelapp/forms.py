from django import forms
from .models import Convocatoria, Team
from django.contrib.auth import get_user_model

User = get_user_model()

class ConvocatoriaForm(forms.ModelForm):
    jugadores = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Jugadores convocados"
    )

    class Meta:
        model = Convocatoria
        fields = ['equipo', 'fecha', 'hora', 'lugar', 'jugadores']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'lugar': forms.TextInput(attrs={'class': 'form-control'}),
            'equipo': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        equipo_id = kwargs.pop('equipo_id', None)
        super().__init__(*args, **kwargs)
        self.fields['jugadores'].widget.attrs.update({'class': 'form-check-input'})

        if equipo_id:
            self.fields['jugadores'].queryset = User.objects.filter(equipo__id=equipo_id)
        else:
            self.fields['jugadores'].queryset = User.objects.none()



class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['nombre', 'tipo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
