import json


def obj_set_to_json(obj_set):
    obj_list = []
    for obj in obj_set:
        obj_list.append(obj_to_json(obj))
    return obj_list


def obj_to_json(obj):
    if type(obj) != dict:
        obj_dict = obj.__dict__
    else:
        obj_dict = obj
    result_dict = {}
    for key in list(obj_dict):
        if not key.startswith("_"):
            if type(obj_dict[key]) != list:
                result_dict[key] = obj_dict[key].__str__()
            else:
                result_dict[key] = obj_dict[key]
    return result_dict


def json_to_obj(json_str, obj):
    parse_data = json.loads(json_str.strip('\t\r\n'))
    result = obj()
    result.__dict__ = parse_data
    return result


def obj_to_json_str(obj):
    return json.dumps(obj.__dict__, ensure_ascii=True)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
