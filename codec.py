
import json

from tree import FilterTree


class TreeJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, FilterTree):
            return repr(obj)
        return super().default(obj)


def _enforce_strict_numbers(obj):
    raise ValueError("Number %r is not JSON compliant" % obj)


def dump(obj, fp, cls=TreeJSONEncoder, allow_nan=False, **kwargs):
    return json.dump(obj, fp, cls=cls, allow_nan=allow_nan, **kwargs)


def dumps(obj, cls=TreeJSONEncoder, allow_nan=False, **kwargs):
    return json.dumps(obj, cls=cls, allow_nan=allow_nan, **kwargs)


def load(fp,
         cls=json.JSONDecoder,
         parse_constant=_enforce_strict_numbers,
         object_hook=FilterTree.toInstance,
         **kwargs):
    return json.load(fp,
                     cls=cls, object_hook=object_hook,
                     parse_constant=parse_constant,
                     **kwargs)


def loads(s,
          cls=json.JSONDecoder,
          parse_constant=_enforce_strict_numbers,
          object_hook=FilterTree.toInstance,
          **kwargs):
    return json.loads(s,
                      cls=cls, object_hook=object_hook,
                      parse_constant=parse_constant,
                      **kwargs)



