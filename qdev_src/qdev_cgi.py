from http import HTTPStatus

CGILocals = {
  'http': HTTPStatus,
  'len': len,
  'str': str,
  'int': int,
  'float': float,
  'bin': bin,
  'oct': oct,
  'hex': hex,
  'bool': bool,
  'bytes': bytes,
  'bytearray': bytearray,
  'callable': callable,
  'chr': chr,
  'complex': complex,
}
