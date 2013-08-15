from django import forms
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html
from django.forms.util import flatatt

class MapWidget(forms.Widget):
    """
    Just renders a div for the map
    """
    input_type = None # Subclasses must define this.

    def _format_value(self, value):
        if self.is_localized:
            return formats.localize_input(value)
        return value

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(self._format_value(value))
        return format_html("""<input class="geocomplete" type="text" name="asd" />
            <div style="width:500px;height:400px;" class="geocomplete-map" id="id_{0}" ></div>""", name)


class GeopositionWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = (
            forms.TextInput(),
            forms.TextInput(),
            # forms.TextInput(attrs={"class":"geocomplete"}),
            MapWidget(),
        )
        super(GeopositionWidget, self).__init__(widgets, attrs)
    
    def decompress(self, value):
        if value:
            return [value.latitude, value.longitude]
        return [None,None]
    
    def format_output(self, rendered_widgets):
        return render_to_string('geoposition/widgets/geoposition.html', {
            'latitude': {
                'html': rendered_widgets[0],
                'label': _("latitude"),
            },
            'longitude': {
                'html': rendered_widgets[1],
                'label': _("longitude"),
            },
            'location': {
                'html': rendered_widgets[2],
                'label': 'location',
            },
            # 'map': rendered_widgets[3],
        })
    
    class Media:
        js = (
            'http://maps.googleapis.com/maps/api/js?sensor=false&libraries=places',
            'geocomplete/jquery.geocomplete.js',
            'geocomplete/geocomplete.js',
            )
        css = {
            'all': ('geoposition/geoposition.css',)
        }
        