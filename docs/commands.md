# {{command().title}}
{{ command().description }}
{% if command().examples %}
#### Examples
{% for example in command().examples %}
**{{example.title}}**
```sh
{{example.cmd}}
```
{% if example.extra %}
*{{example.extra}}*
{% endif %}
{% endfor %}
{% endif %}

{% if command().notes %}
{% for note in command().notes %}
#### {{ note.title }}
{{ note.description }}
{% endfor %}
{% endif %}
