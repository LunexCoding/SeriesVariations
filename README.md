SeriesVariations - a program designed to build interval variation series, as well as calculate some of their statistical estimates.

[RU documentation](docs/readmeRU.md)

# Statistical estimates

* average
* standard deviation
* dispersion

> The degree of rounding for these estimates is `6` decimal places.

# Usage

When launched, the `series.txt` file will be initialized in the directory from which it was launched.

You need to open this file and enter your selection. Numbers must be separated by a space. If your selection 
contains float numbers, you should separate the integer part with a dot or comma: `2.95 3,1`.

After a short load, after the command line prompt appears, you need to enter a degree to round up the calculations. 
This degree affects the construction of the variation series, namely, the resulting intervals.

For example, you have a sample with a total volume of 30, `n=30`, after introducing a certain degree of rounding, 
you can see that the cumulative frequency may be less than the total sample, let's say it will be 29, `ni=29`. In 
this case, increase the degree of rounding until your cumulative frequency equals the sample size.

# Designations

* `array` - sample
* `n` - numeric option
* `max` - maximum sample value
* `min` - minimum sample value
* `k` - the number of intervals according to the Sturges rule
* `h` - interval size
* `x0` - lower bound of the first interval
* `Xe` - arithmetic mean
* `De` - dispersion
* `S^2`- corrected sample variance
* `σ` - standard deviation
* `S` - corrected standard deviation


* `I` - interval number
* `Interval` - Interval [lower bound - upper bound)
  > Last interval [lower bound - upper bound]
* `xi` - the middle of the interval, the interval series is converted into a discrete
* `ni` - frequency
* `xini` - the product of the middle of the interval and the frequency
* `xi(2)ni` - the product of the square of the middle of the interval and the frequency
* `wi` - relative frequency

# Formulas Used

* $k = 1 + 3.322 * lg(n)$ rounded ***down***
* $h = \frac{max - min}k$
* $x0 = min$
* $Xe = \frac{sum(xi)}{n}$
* $De = \surdσ$
* $S^{2}= \frac{n}{n-1}* De$
* $σ = \frac{sum(xini)}{n}$
* $S = \sqrt{S^{2}}$