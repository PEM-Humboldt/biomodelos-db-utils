# {{command().title}}
{{ command().description }}
{% if command().notes %}
{% for note in command().notes %}
#### {{ note.title }}
{{ note.description }}
{% endfor %}
{% endif %}
