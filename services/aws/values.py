import json


def get_doc_provide_access_lambda():
    document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "sts:AssumeRole"
                ],
                "Principal": {
                    "Service": [
                        "lambda.amazonaws.com"
                    ]
                }
            }
        ]
    }
    return json.dumps(document)


def get_mapping_template():
    map_templ = {
        'key': {
            'name': "$input.params('name')",
            'mfr': "$input.params('mfr')",
        }
    }
    return json.dumps(map_templ)


def get_mapping_template_update():
    map_templ_update = {
        'key': {
            'name': "$input.params('name')",
            'mfr': "$input.params('mfr')",
            'calories': "$input.params('calories')",
            'carbo': "$input.params('carbo')",
            'cups': "$input.params('cups')",
            'fat': "$input.params('fat')",
            'fiber': "$input.params('fiber')",
            'potass': "$input.params('potass')",
            'protein': "$input.params('protein')",
            'rating': "$input.params('rating')",
            'shelf': "$input.params('shelf')",
            'sodium': "$input.params('sodium')",
            'sugar': "$input.params('sugar')",
            'type': "$input.params('type')",
            'vitamins': "$input.params('vitamins')",
            'weight': "$input.params('weight')",
        }
    }
    return json.dumps(map_templ_update)
