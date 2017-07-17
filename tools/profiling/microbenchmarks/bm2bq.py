#!/usr/bin/env python2.7
#
# Convert google-benchmark json output to something that can be uploaded to
# BigQuery
#
#
# Copyright 2017 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import json
import csv
import bm_json

columns = [
  ('jenkins_build', 'integer'),
  ('jenkins_job', 'string'),
  ('date', 'timestamp'),
  ('cpu_scaling_enabled', 'boolean'),
  ('num_cpus', 'integer'),
  ('mhz_per_cpu', 'integer'),
  ('library_build_type', 'string'),
  ('name', 'string'),
  ('fixture', 'string'),
  ('client_mutator', 'string'),
  ('server_mutator', 'string'),
  ('request_size', 'integer'),
  ('response_size', 'integer'),
  ('request_count', 'integer'),
  ('iterations', 'integer'),
  ('time_unit', 'string'),
  ('real_time', 'integer'),
  ('cpu_time', 'integer'),
  ('bytes_per_second', 'float'),
  ('allocs_per_iteration', 'float'),
  ('locks_per_iteration', 'float'),
  ('writes_per_iteration', 'float'),
  ('bandwidth_kilobits', 'integer'),
  ('cli_transport_stalls_per_iteration', 'float'),
  ('cli_stream_stalls_per_iteration', 'float'),
  ('svr_transport_stalls_per_iteration', 'float'),
  ('svr_stream_stalls_per_iteration', 'float'),
  ('atm_cas_per_iteration', 'float'),
  ('atm_add_per_iteration', 'float'),
  ('end_of_stream', 'boolean'),
  ('header_bytes_per_iteration', 'float'),
  ('framing_bytes_per_iteration', 'float'),
  ('nows_per_iteration', 'float'),
]

SANITIZE = {
  'integer': int,
  'float': float,
  'boolean': bool,
  'string': str,
  'timestamp': str,
}

if sys.argv[1] == '--schema':
  print ',\n'.join('%s:%s' % (k, t.upper()) for k, t in columns)
  sys.exit(0)

with open(sys.argv[1]) as f:
  js = json.loads(f.read())

if len(sys.argv) > 2:
  with open(sys.argv[2]) as f:
    js2 = json.loads(f.read())
else:
  js2 = None

writer = csv.DictWriter(sys.stdout, [c for c,t in columns])

for row in bm_json.expand_json(js, js2):
  sane_row = {}
  for name, sql_type in columns:
    if name in row:
      if row[name] == '': continue
      sane_row[name] = SANITIZE[sql_type](row[name])
  writer.writerow(sane_row)
