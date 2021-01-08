# Inductor Generator

## Installation and Use

Requires Docker to be installed and configured for the user.

1. Build the docker image using `./build.sh`

2. Run Asitic using `./run.sh`


## Useful Info

Spiral geometry defined by:
- Outer length / width (L)
- Conductor width (W)
- Conductor spacing (S)
- Number of turns (N)

For a given area (A) and metal/oxide/substrate layers, we
wish to select the best (or desired):
- Quality factor (Q)
- Inductance (L)
- Q · L product
- Self-Resonance Frequency (SRF)
- Parasitic Capacitance (Csub, Cox, Cc)

$$\int_{a}^{b} x^2 dx$$


### Useful Links

 - [A Fundamental Approach for Design and Optimization
of a Spiral Inductor](https://www.davidpublisher.org/Public/uploads/Contribute/5bce8a9322551.pdf)

 - [On-Chip Spiral Inductors for RF Applications:
An Overview](http://www.jsts.org/html/journal/journal_files/2004/9/04-011.pdf)
