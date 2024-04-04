from django_web_components import component

@component.register("card")
class Card(component.Component):
    template_name = "components/card.html"