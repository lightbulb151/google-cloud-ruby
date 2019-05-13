# Copyright 2018 Google LLC
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

"""This script is used to synthesize generated parts of this library."""

import synthtool as s
import synthtool.gcp as gcp
import synthtool.languages.ruby as ruby
import logging
import re

logging.basicConfig(level=logging.DEBUG)

gapic = gcp.GAPICGenerator()

v1_library = gapic.ruby_library(
    'bigquery/datatransfer', 'v1',
    artman_output_name='google-cloud-ruby/google-cloud-bigquerydatatransfer',
    config_path='artman_bigquerydatatransfer.yaml'
)
s.copy(v1_library / 'acceptance')
s.copy(v1_library / 'lib')
s.copy(v1_library / 'test')
s.copy(v1_library / 'README.md')
s.copy(v1_library / 'LICENSE')
s.copy(v1_library / '.gitignore')
s.copy(v1_library / '.yardopts')
s.copy(v1_library / 'google-cloud-bigquery-data_transfer.gemspec', merge=ruby.merge_gemspec)

# Copy common templates
templates = gcp.CommonTemplates().ruby_library()
s.copy(templates)

# PERMANENT: Use custom credentials env variable names
s.replace(
    'lib/google/cloud/bigquery/data_transfer/v1/credentials.rb',
    'BIGQUERYDATATRANSFER_KEYFILE', 'DATA_TRANSFER_KEYFILE')
s.replace(
    'lib/google/cloud/bigquery/data_transfer/v1/credentials.rb',
    'BIGQUERYDATATRANSFER_CREDENTIALS', 'DATA_TRANSFER_CREDENTIALS')

# https://github.com/googleapis/gapic-generator/issues/2179
# https://github.com/googleapis/gapic-generator/issues/2196
s.replace(
    [
      'README.md',
      'lib/google/cloud/bigquery/data_transfer.rb',
      'lib/google/cloud/bigquery/data_transfer/v1.rb'
    ],
    '\\[Product Documentation\\]: https://cloud\\.google\\.com/bigquerydatatransfer\n',
    '[Product Documentation]: https://cloud.google.com/bigquery/transfer/\n')

# https://github.com/googleapis/gapic-generator/issues/2242
def escape_braces(match):
    expr = re.compile('^([^`]*(`[^`]*`[^`]*)*)([^`#\\$\\\\])\\{([\\w,]+)\\}')
    content = match.group(0)
    while True:
        content, count = expr.subn('\\1\\3\\\\\\\\{\\4}', content)
        if count == 0:
            return content
s.replace(
    'lib/google/cloud/**/*.rb',
    '\n(\\s+)#[^\n]*[^\n#\\$\\\\]\\{[\\w,]+\\}',
    escape_braces)

# https://github.com/googleapis/gapic-generator/issues/2243
s.replace(
    'lib/google/cloud/bigquery/data_transfer/*/*_client.rb',
    '(\n\\s+class \\w+Client\n)(\\s+)(attr_reader :\\w+_stub)',
    '\\1\\2# @private\n\\2\\3')

# https://github.com/googleapis/gapic-generator/issues/2279
s.replace(
    'lib/**/*.rb',
    '\\A(((#[^\n]*)?\n)*# (Copyright \\d+|Generated by the protocol buffer compiler)[^\n]+\n(#[^\n]*\n)*\n)([^\n])',
    '\\1\n\\6')

# https://github.com/googleapis/gapic-generator/issues/2323
s.replace(
    [
        'lib/**/*.rb',
        'README.md'
    ],
    'https://github\\.com/GoogleCloudPlatform/google-cloud-ruby',
    'https://github.com/googleapis/google-cloud-ruby'
)
s.replace(
    [
        'lib/**/*.rb',
        'README.md'
    ],
    'https://googlecloudplatform\\.github\\.io/google-cloud-ruby',
    'https://googleapis.github.io/google-cloud-ruby'
)

# https://github.com/googleapis/gapic-generator/issues/2393
s.replace(
    'google-cloud-bigquery-data_transfer.gemspec',
    'gem.add_development_dependency "rubocop".*$',
    'gem.add_development_dependency "rubocop", "~> 0.64.0"'
)

s.replace(
    'google-cloud-bigquery-data_transfer.gemspec',
    '"README.md", "LICENSE"',
    '"README.md", "AUTHENTICATION.md", "LICENSE"'
)
s.replace(
    '.yardopts',
    'README.md\n',
    'README.md\nAUTHENTICATION.md\nLICENSE\n'
)

# https://github.com/googleapis/google-cloud-ruby/issues/3058
s.replace(
    'google-cloud-bigquery-data_transfer.gemspec',
    '\nGem::Specification.new do',
    'require File.expand_path("../lib/google/cloud/bigquery/data_transfer/version", __FILE__)\n\nGem::Specification.new do'
)
s.replace(
    'google-cloud-bigquery-data_transfer.gemspec',
    '(gem.version\s+=\s+).\d+.\d+.\d.*$',
    '\\1Google::Cloud::Bigquery::DataTransfer::VERSION'
)
s.replace(
    'lib/google/cloud/bigquery/data_transfer/v1/data_transfer_service_client.rb',
    'require "google/cloud/bigquery/data_transfer/v1/credentials"',
    'require "google/cloud/bigquery/data_transfer/v1/credentials"\nrequire "google/cloud/bigquery/data_transfer/version"'
)
s.replace(
    'lib/google/cloud/bigquery/data_transfer/v1/data_transfer_service_client.rb',
    'Gem.loaded_specs\[.*\]\.version\.version',
    'Google::Cloud::Bigquery::DataTransfer::VERSION'
)
