import numbers

import six


class ParameterNotValidError(ValueError):
    """ The given value is not valid for the parameter type """


class Parameter(object):
    def __init__(self, required=True):
        self.required = required

    def to_python(self, value):
        """ Convert the JSON value to a Python object """

        return value

    def to_json(self, value):
        """ Convert a Python object to JSON """

        return value


class ListParameter(Parameter):
    def __init__(self, param_type, *args, **kwargs):
        self.param_type = param_type
        super(ListParameter, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not isinstance(value, list):
            value = [value]

        return [self.param_type.to_python(x) for x in value]

    def to_json(self, value):
        if not isinstance(value, list):
            value = [value]

        return [self.param_type.to_json(x) for x in value]


class StringParameter(Parameter):
    def to_python(self, value):
        if isinstance(value, six.string_types):
            return value
        elif isinstance(value, numbers.Number):
            return six.text_type(value)

        raise ParameterNotValidError('Value must be a string or number')

    def to_json(self, value):
        return six.text_type(value)


class NumberParameter(Parameter):
    def to_python(self, value):
        if isinstance(value, numbers.Number):
            return value
        elif isinstance(value, six.string_types):
            try:
                value = float(value)
                return int(value) if value.is_integer() else value
            except ValueError:
                raise ParameterNotValidError('String is not a number: {}'.format(value))

        raise ParameterNotValidError('Value must be a number')

    def to_json(self, value):
        return value


class IntParameter(NumberParameter):
    def to_python(self, value):
        return int(super(IntParameter, self).to_python(value))

    def to_json(self, value):
        return int(value)


class FloatParameter(NumberParameter):
    def to_python(self, value):
        return float(super(FloatParameter, self).to_python(value))

    def to_json(self, value):
        return float(value)


class BooleanParameter(Parameter):
    def to_python(self, value):
        if isinstance(value, six.string_types):
            if value.lower() == 'true':
                return True
            elif value.lower() == 'false':
                return False
            else:
                raise ParameterNotValidError('Invalid value for boolean parameter: {}'.format(value))

        if isinstance(value, int):
            if value in (0, 1):
                return bool(value)
            else:
                raise ParameterNotValidError('Invalid value for boolean parameter: {}'.format(value))

        if isinstance(value, bool):
            return bool(value)

        raise ParameterNotValidError('Invalid type for boolean parameter: {}'.format(value.__class__.__name__))

    def to_json(self, value):
        return bool(value)


class DictParameter(Parameter):
    def to_python(self, value):
        if isinstance(value, (dict, list)):
            return value

        raise ParameterNotValidError('Invalid type for dict parameter: {}'.format(value.__class__.__name__))

    def to_json(self, value):
        return self.to_python(value)



