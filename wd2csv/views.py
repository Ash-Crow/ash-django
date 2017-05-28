import csv
from django.http import HttpResponse
from django.shortcuts import render
from .forms import QueryForm
from SPARQLWrapper import SPARQLWrapper, JSON


def index(request):
    if request.method == "POST":
        form = QueryForm(request.POST)
        if form.is_valid():
            headers, rows = process_query(form.cleaned_data)
            return generate_csv(headers, rows)
            # return redirect('post_detail', pk=form.pk)
    else:
        form = QueryForm()

    return render(request, 'wd2csv/index.dtl', {'form': form})


def generate_csv(headers, rows):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="response.csv"'

    writer = csv.DictWriter(response, fieldnames=headers)

    writer.writeheader()

    for key, row in rows.items():
        writer.writerow(row)

    return response


def sparql_query(query):
    endpoint = "https://query.wikidata.org/bigdata/namespace/wdq/sparql"
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results['results']['bindings']


def get_entities(values, type='Q'):
    if type == 'Q' or type == 'L':
        prefix = "wd:"
    elif type == 'P':
        prefix = 'wdt:'
    else:
        raise ValueError('Entity type must be either L, Q or P')

    entities = []
    for v in values:
        if v[0].upper() == type and v[1:].isdigit():
            entities.append(prefix + v)
        else:
            error_text = 'Please enter one {}id per line'.format(type)
            raise ValueError(error_text)

    return entities


def process_query(data):
    print(data)

    items = get_entities(data['qids'], 'Q')
    if len(data['languages']):
        languages = data['languages']
    else:
        languages = "en"

    if data['pids']:
        properties = """
        VALUES ?direct {{
          {}
        }}
        """.format('\n'.join(get_entities(data['pids'], 'P')))
    else:
        properties = ''

    # Sample version of the query: http://tinyurl.com/y9oucmuw
    query = """
SELECT ?item ?itemLabel ?itemDescription ?prop ?propLabel ?value ?valueLabel
WHERE {{
  ?item ?direct ?value .
  ?prop wikibase:directClaim ?direct .

  VALUES ?item {{
  {}
  }}

  #Properties
  {}

  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "{}" }}
}} ORDER BY ?item LIMIT 5000
    """.format(
        '\n'.join(items),
        properties,
        languages)

    results = sparql_query(query)
    print(results)

    headers = ['item', 'label', 'description']
    rows = {}

    for r in results:
        item = r['item']['value'].split('/')[-1]

        if 'itemLabel' in r:
            label = r['itemLabel']['value']
        else:
            label = ''

        if 'itemDescription' in r:
            description = r['itemDescription']['value']
        else:
            description = ""

        if item not in rows:
            rows[item] = {
                'item': item,
                'label': label,
                'description': description
            }

        propId = r['prop']['value'].split('/')[-1]
        propLabel = r['propLabel']['value']

        if data['return_labels_for_properties']:
            prop = propLabel
        else:
            prop = propId

        if prop not in headers:
            headers.append(prop)

        valueRaw = r['value']['value']
        valueLabel = r['valueLabel']['value']

        if data['return_labels_for_values']:
            value = valueLabel
        else:
            if valueRaw[0:31] == 'http://www.wikidata.org/entity/':
                valueRaw = valueRaw[31:]
            value = valueRaw

        rows[item][prop] = value
        print(item, propId, propLabel, valueRaw, valueLabel)

    return headers, rows
