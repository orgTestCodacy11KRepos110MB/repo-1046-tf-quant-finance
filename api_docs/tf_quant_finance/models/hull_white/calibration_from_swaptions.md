<!--
This file is generated by a tool. Do not edit directly.
For open-source contributions the docs will be updated automatically.
-->

*Last updated: 2020-11-11.*

<div itemscope itemtype="http://developers.google.com/ReferenceObject">
<meta itemprop="name" content="tf_quant_finance.models.hull_white.calibration_from_swaptions" />
<meta itemprop="path" content="Stable" />
</div>

# tf_quant_finance.models.hull_white.calibration_from_swaptions

<!-- Insert buttons and diff -->

<table class="tfo-notebook-buttons tfo-api" align="left">
</table>

<a target="_blank" href="https://github.com/google/tf-quant-finance/blob/master/tf_quant_finance/models/hull_white/calibration.py">View source</a>



Calibrates the Hull-White model using European Swaptions.

```python
tf_quant_finance.models.hull_white.calibration_from_swaptions(
    *, prices, expiries, floating_leg_start_times, floating_leg_end_times,
    fixed_leg_payment_times, floating_leg_daycount_fractions,
    fixed_leg_daycount_fractions, fixed_leg_coupon, reference_rate_fn,
    mean_reversion, volatility, notional=None, is_payer_swaption=None,
    use_analytic_pricing=True, num_samples=1, random_type=None, seed=None, skip=0,
    time_step=None, optimizer_fn=None, mean_reversion_lower_bound=0.001,
    mean_reversion_upper_bound=0.5, volatility_lower_bound=0.0,
    volatility_upper_bound=0.1, tolerance=1e-06, maximum_iterations=50, dtype=None,
    name=None
)
```



<!-- Placeholder for "Used in" -->

This function estimates the mean-reversion rate and volatility parameters of
a Hull-White 1-factor model using a set of European swaption prices as the
target. The calibration is performed using least-squares optimization where
the loss function minimizes the squared error between the target swaption
prices and the model implied swaption prices.

#### Example
The example shows how to calibrate a Hull-White model with constant mean
reversion rate and constant volatility.

````python
import numpy as np
import tensorflow.compat.v2 as tf
import tf_quant_finance as tff

dtype = tf.float64

mean_reversion = [0.03]
volatility = [0.01]
expiries = np.array(
    [0.5, 0.5, 1.0, 1.0, 2.0, 2.0, 3.0, 3.0, 4.0, 4.0, 5.0, 5.0, 10., 10.])
float_leg_start_times = np.array([
    [0.5, 1.0, 1.5, 2.0, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5],  # 6M x 2Y  swap
    [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0],  # 6M x 5Y  swap
    [1.0, 1.5, 2.0, 2.5, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0],  # 1Y x 2Y  swap
    [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5],  # 1Y x 5Y  swap
    [2.0, 2.5, 3.0, 3.5, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0],  # 2Y x 2Y  swap
    [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5],  # 2Y x 5Y  swap
    [3.0, 3.5, 4.0, 4.5, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],  # 3Y x 2Y  swap
    [3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5],  # 3Y x 5Y  swap
    [4.0, 4.5, 5.0, 5.5, 6.0, 6.0, 6.0, 6.0, 6.0, 6.0],  # 4Y x 2Y  swap
    [4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5],  # 4Y x 5Y  swap
    [5.0, 5.5, 6.0, 6.5, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0],  # 5Y x 2Y  swap
    [5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5],  # 5Y x 5Y  swap
    [10.0, 10.5, 11.0, 11.5, 12.0, 12.0, 12.0, 12.0, 12.0,
     12.0],  # 10Y x 2Y  swap
    [10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0,
     14.5]  # 10Y x 5Y  swap
])
float_leg_end_times = float_leg_start_times + 0.5
max_maturities = np.array(
    [2.5, 5.5, 3.0, 6.0, 4., 7., 5., 8., 6., 9., 7., 10., 12., 15.])
for i in range(float_leg_end_times.shape[0]):
  float_leg_end_times[i] = np.clip(
      float_leg_end_times[i], 0.0, max_maturities[i])

fixed_leg_payment_times = float_leg_end_times
float_leg_daycount_fractions = (
    float_leg_end_times - float_leg_start_times)
fixed_leg_daycount_fractions = float_leg_daycount_fractions
fixed_leg_coupon = 0.01 * np.ones_like(fixed_leg_payment_times)

zero_rate_fn = lambda x: 0.01 * tf.ones_like(x, dtype=dtype)
prices = tff.models.hull_white.swaption_price(
    expiries=expiries,
    floating_leg_start_times=float_leg_start_times,
    floating_leg_end_times=float_leg_end_times,
    fixed_leg_payment_times=fixed_leg_payment_times,
    floating_leg_daycount_fractions=float_leg_daycount_fractions,
    fixed_leg_daycount_fractions=fixed_leg_daycount_fractions,
    fixed_leg_coupon=fixed_leg_coupon,
    reference_rate_fn=zero_rate_fn,
    notional=100.,
    dim=1,
    mean_reversion=mean_reversion,
    volatility=volatility,
    use_analytic_pricing=True,
    dtype=dtype)

calibrated_model = tff.models.hull_white.calibration_from_swaptions(
    prices=prices[:, 0],
    expiries=expiries,
    floating_leg_start_times=float_leg_start_times,
    floating_leg_end_times=float_leg_end_times,
    fixed_leg_payment_times=fixed_leg_payment_times,
    floating_leg_daycount_fractions=float_leg_daycount_fractions,
    fixed_leg_daycount_fractions=fixed_leg_daycount_fractions,
    fixed_leg_coupon=fixed_leg_coupon,
    reference_rate_fn=zero_rate_fn,
    notional=100.,
    mean_reversion=[0.01],  # Initial guess for mean reversion rate
    volatility=[0.005],  # Initial guess for volatility
    maximum_iterations=50,
    dtype=dtype)
# Expected calibrated_model.mean_reversion.values(): [0.03]
# Expected calibrated_model.volatility.values(): [0.01]
````

#### Args:


* <b>`prices`</b>: A rank 1 real `Tensor`. The prices of swaptions used for
  calibration.
* <b>`expiries`</b>: A real `Tensor` of same shape and dtype as `prices`. The time to
  expiration of the swaptions.
* <b>`floating_leg_start_times`</b>: A real `Tensor` of the same dtype as `expiries`.
  The times when accrual begins for each payment in the floating leg. The
  shape of this input should be `expiries.shape + [m]` where `m` denotes
  the number of floating payments in each leg.
* <b>`floating_leg_end_times`</b>: A real `Tensor` of the same dtype as `expiries`.
  The times when accrual ends for each payment in the floating leg. The
  shape of this input should be `expiries.shape + [m]` where `m` denotes
  the number of floating payments in each leg.
* <b>`fixed_leg_payment_times`</b>: A real `Tensor` of the same dtype as `expiries`.
  The payment times for each payment in the fixed leg. The shape of this
  input should be `expiries.shape + [n]` where `n` denotes the number of
  fixed payments in each leg.
* <b>`floating_leg_daycount_fractions`</b>: A real `Tensor` of the same dtype and
  compatible shape as `floating_leg_start_times`. The daycount fractions
  for each payment in the floating leg.
* <b>`fixed_leg_daycount_fractions`</b>: A real `Tensor` of the same dtype and
  compatible shape as `fixed_leg_payment_times`. The daycount fractions
  for each payment in the fixed leg.
* <b>`fixed_leg_coupon`</b>: A real `Tensor` of the same dtype and compatible shape
  as `fixed_leg_payment_times`. The fixed rate for each payment in the
  fixed leg.
* <b>`reference_rate_fn`</b>: A Python callable that accepts expiry time as a real
  `Tensor` and returns a `Tensor` of shape `input_shape + [dim]`. Returns
  the continuously compounded zero rate at the present time for the input
  expiry time.
* <b>`mean_reversion`</b>: A real positive scalar `Tensor` or an Python callable. The
  callable should satisfy the following:
  (a) A left-continuous piecewise constant object (e.g.,
  `tff.math.piecewise.PiecewiseConstantFunc`) that has a property
  `is_piecewise_constant` set to `True`. In this case the object should
  have a method `jump_locations(self)` that returns a `Tensor` of shape
  `[num_jumps]` and `values(self)` that returns a `Tensor` of shape
  `[num_jumps + 1]`. The callable, `mean_reversion(t)` should return a
  `Tensor` of shape `t.shape`, where `t` is a rank 1 `Tensor` of
  the same `dtype` as the output.
  Corresponds to the mean reversion rate to be calibrated. The input
  `Tensor` or the `Tensor` `mean_reversion.values()` is also used as the
  initial point for calibration.
* <b>`volatility`</b>: A real positive scalar `Tensor` of the same `dtype` as
  `mean_reversion` or a callable with the same specs as above.
  Corresponds to the Hull-White volatility parameter to be calibrated.
* <b>`notional`</b>: An optional `Tensor` of same dtype and compatible shape as
  `strikes`specifying the notional amount for the underlying swap.
   Default value: None in which case the notional is set to 1.
* <b>`is_payer_swaption`</b>: A boolean `Tensor` of a shape compatible with `expiries`.
  Indicates whether the prices correspond to payer (if True) or receiver
  (if False) swaption. If not supplied, payer swaptions are assumed.
* <b>`use_analytic_pricing`</b>: A Python boolean specifying if swaption pricing is
  done analytically during calibration. Analytic valuation is only
  supported for constant `mean_reversion` and piecewise constant
  `volatility`. If the input is `False`, then valuation using Monte-Carlo
  simulations is performed.
  Default value: The default value is `True`.
* <b>`num_samples`</b>: Positive scalar `int32` `Tensor`. The number of simulation
  paths during Monte-Carlo valuation of swaptions. This input is ignored
  during analytic valuation.
  Default value: The default value is 1.
* <b>`random_type`</b>: Enum value of `RandomType`. The type of (quasi)-random
  number generator to use to generate the simulation paths. This input is
  relevant only for Monte-Carlo valuation and ignored during analytic
  valuation.
  Default value: `None` which maps to the standard pseudo-random numbers.
* <b>`seed`</b>: Seed for the random number generator. The seed is only relevant if
  `random_type` is one of
  `[STATELESS, PSEUDO, HALTON_RANDOMIZED, PSEUDO_ANTITHETIC,
    STATELESS_ANTITHETIC]`. For `PSEUDO`, `PSEUDO_ANTITHETIC` and
  `HALTON_RANDOMIZED` the seed should be an Python integer. For
  `STATELESS` and  `STATELESS_ANTITHETIC `must be supplied as an integer
  `Tensor` of shape `[2]`. This input is relevant only for Monte-Carlo
  valuation and ignored during analytic valuation.
  Default value: `None` which means no seed is set.
* <b>`skip`</b>: `int32` 0-d `Tensor`. The number of initial points of the Sobol or
  Halton sequence to skip. Used only when `random_type` is 'SOBOL',
  'HALTON', or 'HALTON_RANDOMIZED', otherwise ignored.
  Default value: `0`.
* <b>`time_step`</b>: Scalar real `Tensor`. Maximal distance between time grid points
  in Euler scheme. Relevant when Euler scheme is used for simulation. This
  input is ignored during analytic valuation.
  Default value: `None`.
* <b>`optimizer_fn`</b>: Optional Python callable which implements the algorithm used
  to minimize the objective function during calibration. It should have
  the following interface:
  result = optimizer_fn(value_and_gradients_function, initial_position,
  tolerance, max_iterations)
  `value_and_gradients_function` is a Python callable that accepts a point
  as a real `Tensor` and returns a tuple of `Tensor`s of real dtype
  containing the value of the function and its gradient at that point.
  'initial_position' is a real `Tensor` containing the starting point of the
  optimization, 'tolerance' is a real scalar `Tensor` for stopping tolerance
  for the procedure and `max_iterations` specifies the maximum number of
  iterations.
  `optimizer_fn` should return a namedtuple containing the items: `position`
  (a tensor containing the optimal value), `converged` (a boolean indicating
  whether the optimize converged according the specified criteria),
  `failed` (a boolean indicating if the optimization resulted in a failure),
  `num_iterations` (the number of iterations used), and `objective_value` (
  the value of the objective function at the optimal value).
  The default value for `optimizer_fn` is None and conjugate gradient
  algorithm is used.
* <b>`mean_reversion_lower_bound`</b>: An optional scalar `Tensor` specifying the
  lower limit of mean reversion rate during calibration.
  Default value: 0.001.
* <b>`mean_reversion_upper_bound`</b>: An optional scalar `Tensor` specifying the
  upper limit of mean reversion rate during calibration.
  Default value: 0.5.
* <b>`volatility_lower_bound`</b>: An optional scalar `Tensor` specifying the
  lower limit of Hull White volatility during calibration.
  Default value: 0.
* <b>`volatility_upper_bound`</b>: An optional scalar `Tensor` specifying the
  upper limit of Hull White volatility during calibration.
  Default value: 0.1.
* <b>`tolerance`</b>: Scalar `Tensor` of real dtype. The absolute tolerance for
  terminating the iterations.
  Default value: 1e-6.
* <b>`maximum_iterations`</b>: Scalar positive int32 `Tensor`. The maximum number of
  iterations during the optimization.
  Default value: 50.
* <b>`dtype`</b>: The default dtype to use when converting values to `Tensor`s.
  Default value: `None` which means that default dtypes inferred by
  TensorFlow are used.
* <b>`name`</b>: Python string. The name to give to the ops created by this function.
  Default value: `None` which maps to the default name
  `hw_swaption_calibration`.


#### Returns:

A Tuple of three elements. The first element is an instance of
`HullWhite1F` whose parameters are calibrated to the input
swaption prices. The second and third elements contains the optimization
status (whether the optimization algorithm succeeded in finding the
optimal point based on the specified convergance criteria) and the number
of iterations performed.