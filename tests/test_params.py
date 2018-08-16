import pytest

from task_api.params import Parameter, StringParameter, ListParameter, NumberParameter, ParameterNotValidError, \
    IntParameter, FloatParameter, BooleanParameter, DictParameter


def test_param():
    p = Parameter()
    assert p.required is True
    assert p.to_python('foo') == 'foo'
    assert p.to_json('foo') == 'foo'
    assert Parameter(required=False).required is False


def test_list_param():
    p = ListParameter(StringParameter())
    assert p.to_python(['1', 2]) == ['1', '2']
    assert p.to_python(2) == ['2']
    assert p.to_json(['1', 2]) == ['1', '2']
    assert p.to_json(2) == ['2']


def test_string_param():
    p = StringParameter()
    assert p.to_python('foo') == 'foo'
    assert p.to_python(5) == '5'
    assert p.to_json('foo') == 'foo'
    assert p.to_json(5) == '5'

    with pytest.raises(ParameterNotValidError):
        p.to_python([1, 2, 3])


def test_number_param():
    p = NumberParameter()
    assert p.to_python(5) == 5
    assert p.to_python(5.) == 5.
    assert p.to_python('5') == 5
    assert p.to_python('5.3') == 5.3
    assert p.to_json(5) == 5

    with pytest.raises(ParameterNotValidError):
        p.to_python('foo')


def test_int_param():
    p = IntParameter()
    assert p.to_python(5) == 5
    assert p.to_python(5.2) == 5
    assert p.to_python('5.2') == 5
    assert p.to_json(5.2) == 5


def test_float_param():
    p = FloatParameter()
    assert p.to_python(5.2) == 5.2
    assert p.to_python(5) == 5.
    assert p.to_json(5) == 5.


def test_boolean_param():
    p = BooleanParameter()
    assert p.to_python(True) is True
    assert p.to_python('true') is True
    assert p.to_python('false') is False
    assert p.to_python(1) is True
    assert p.to_python(0) is False
    assert p.to_json(1) is True
    assert p.to_json(0) is False

    with pytest.raises(ParameterNotValidError):
        p.to_python('foo')

    with pytest.raises(ParameterNotValidError):
        p.to_python(2)


def test_dict_param():
    p = DictParameter()
    assert p.to_python({1: 'one'}) == {1: 'one'}
    assert p.to_python([1, 2, 3]) == [1, 2, 3]
    assert p.to_json({1: 'one'}) == {1: 'one'}

    with pytest.raises(ParameterNotValidError):
        p.to_python(5)
