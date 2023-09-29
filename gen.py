import genanki
import csv
from typing import NamedTuple



FIELDS = [
    {'name': 'Chinese'},
    {'name': 'Pinyin'},
    {'name': 'English'},
    {'name': 'Notes'},
]
chinese_to_english_template = {
    'name': 'Chinese -> English',
    'qfmt': '{{Chinese}}',
    'afmt': '{{Chinese}} ({{Pinyin}})<hr id="answer">{{English}}<hr>{{Notes}}',
}
english_to_chinese_template = {
    'name': 'English -> Chinese',
    'qfmt': '{{English}}',
    'afmt': '{{English}} <hr id="answer">{{Chinese}} ({{Pinyin}})<hr>{{Notes}}',
}

both_ways_model = genanki.Model(
    7893489284,
    'Chinese Character',
    fields=FIELDS,
    templates=[chinese_to_english_template, english_to_chinese_template]
)

c2e_only_model = genanki.Model(
    89248794237,
    'Chinese Character (C -> E Only)',
    fields=FIELDS,
    templates=[chinese_to_english_template]
)

class Character(NamedTuple):
    guid_hash: str
    chinese: str
    pinyin: str
    english: str
    notes: str = ''

    def as_note(self, *, model=both_ways_model) -> genanki.Note:
        return genanki.Note(
            model=model,
            fields=[self.chinese, self.pinyin, self.english, self.notes],
            guid=genanki.guid_for(self.guid_hash)
        )


def get_radicals():
    with open('./radicals.csv') as f:
        read = csv.DictReader(f, delimiter=',')
        for i, r in enumerate(read):
            chinese = r['T'] + '\uff0c' + r['Variant'] if r['Variant'] else r['T']
            pinyin = r['Pinyin'].replace('(', '').replace(')', '')
            yield Character(
                guid_hash=f'radicals-{i}',
                chinese=chinese,
                pinyin=pinyin,
                english=r['Meaning'],
                notes=r['Comments']
            )


radicals = genanki.Deck(8432933482, 'Chinese::Radicals')

for c in get_radicals():
    radicals.add_note(c.as_note(model=c2e_only_model))

genanki.Package(radicals).write_to_file('chinese.apkg')