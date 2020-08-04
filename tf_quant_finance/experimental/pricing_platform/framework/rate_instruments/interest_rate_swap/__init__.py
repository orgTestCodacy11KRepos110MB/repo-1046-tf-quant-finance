# Lint as: python3
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Interest rate swap."""

from tf_quant_finance.experimental.pricing_platform.framework.rate_instruments.interest_rate_swap.interest_rate_swap import InterestRateSwap
from tf_quant_finance.experimental.pricing_platform.framework.rate_instruments.interest_rate_swap.interest_rate_swap import InterestRateSwapConfig

from tensorflow.python.util.all_util import remove_undocumented  # pylint: disable=g-direct-tensorflow-import

_allowed_symbols = [
    "InterestRateSwap",
    "InterestRateSwapConfig",
]

remove_undocumented(__name__, _allowed_symbols)
