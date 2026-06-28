---
layout: post
title: "Quantity-safe analog literals"
date: 2026-05-02
categories: c++
---

## Analog literals

Analog literals are a cute C++ gadget proposed by Eelis in the seminal article [Multi-Dimensional Analog Literals][analog-literals].
That forward-thinking monument to human mischief finally allowed C++ developers to represent lines, squares and cuboids directly in code:

```cpp
using namespace analog_literals::symbols;

assert( ( o-------------o
          |L             \
          | L             \
          |  L             \
          |   o-------------o
          |   !             !
          !   !             !
          o   |             !
           L  |             !
            L |             !
             L|             !
              o-------------o ).volume == ( o-------------o
                                            |             !
                                            !             !
                                            !             !
                                            o-------------o ).area * int(I-------------I) );
```

Paving the way for a more expressive future is no easy task.
Pioneers might open grand doors and bless the world with such diruptive breakthroughs,
though polishing those new tools until they become what is they always ought to be is the work of a thousand hands.

Indeed the original analog literals weren't free of issues.
Take for example the way lines are calculated:

```cpp
assert( I-I == 0 );
assert( I---I == 1 );
assert( I-----I == 2 );
assert( I-------I == 3 );
```

Due to the [max munch rule][max-munch] of C++ parsing, coupled to the existence of `-` and `--` tokens,
the author had to resort to using $$2N+1$$ dashes to represent $$N$$ units of length.
This choice also gives us a counter-intuitive definition of $$0$$ with a non-zero amount of dashes.

This specific issue was tackled by different authors such as [Hostile Fork][^1] and [Mirai Kuriyama][^2] over the years.
However it is merely one of the several elements of friction plaguing the original implementation.
Eelis themselves highlight a few more:

> The current implementation has one restriction on cuboid dimensions: the height of a cuboid literal must be at least its depth + 2.

In the following sections, I am going to wear the heavy clock of history, and attempt to tackle another one of those shortcomings.
While acknowledging the aforementioned evolutions to analog literals, the rest of the current note is directly based on the original implementation.

## Units, quantities and safety

The XHTML format of the original web page, coupled with its distinct lack of HTTPS support, were already telltales of its age.
Modern eyes however might distinguish other signs of a more innocent era of programming: the apparent lack of strong typing discipline.

Let me explain: the implementation does provide strong `line`, `rectangle` and `cuboid` types corresponding to each category of literals.
Those types even contain the dimensions of the literals as non-type template parameters:

```cpp
template <uint len>
struct line {
    static uint const length;
    operator uint () const { return len; }
};

template <uint x, uint y>
struct rectangle {
    static uint const width, height, area;
};

template <uint x, uint y, uint z>
struct cuboid {
    static uint const width, height, depth, volume;
};
```

But all of that information is cast away whenever any property is queried.
All we get is raw, barely meaningful unsigned integers!

Proof of that distinct lack of dimension safety, the following piece of code compiles and runs perfectly well:

```cpp
assert( ( o-------------o
          |             !
          !             !
          !             !
          o-------------o ).area == 2 * (I-------------I).length );
```

In a time where safety is supposedly everything — including a branding argument in the evergoing programming languages war —,
I coudn't just let something like that slip past our collective vigilance.

_**We need quantity-safe analog literals. And we need them today.**_

We're reaching the part of this article where I have to confess that I was just looking for a fun micro-project to give [mp-units][mp-units] a try.

What is mp-units you ask? It is a C++ library by Mateusz Pusz which attempts to provide compile-time unit & quantities safety guarantees,
all while while remaining ergonomic enough and [ISO/IEC 80000][iso-iec-80000]-compliant.
The library is currently going through the WG21 committee for C++ standardization, with strong consensus to provide vocabulary types for safe scientific computing.

For the sake of simplicity, I am going to assume that the length of `line` is in meters.
Taking advantage of modern C++ features and mp-units, here is a reimplementation of the analog literal types:

```cpp
#include <mp-units/systems/isq.h>
#include <mp-units/systems/si.h>

using namespace mp_units;
using namespace mp_units::si::unit_symbols;

template <unsigned int Length>
struct line:
  L_symbols<line<Length>, 0>
{
  static constexpr quantity<isq::length[m]> length = Length * m;
};

template <unsigned int Width, unsigned int Height>
struct rectangle {
    static constexpr quantity<isq::length[m]> width = Width * m;
    static constexpr quantity<isq::length[m]> height = Height * m;
    static constexpr quantity<isq::area[m*m]> area
        = width * height;
};

template <unsigned int Width, unsigned int Height, unsigned int Depth>
struct cuboid {
    static constexpr quantity<isq::length[m]> width = Width * m;
    static constexpr quantity<isq::length[m]> height = Height * m;
    static constexpr quantity<isq::length[m]> depth = Depth * m;
    static constexpr quantity<isq::volume[m*m*m]> volume
        = width * height * depth;
};
```

I also decided to get rid of the implicit conversion operator in `line`: I consider that a line _has_ a length, not that it _is_ a length.
The choice to provide the conversion was also somewhat dubious from a consistency point of view if we take into account the fact that a `rectangle` does not implicitly convert to its area.

Once the example from the introduction has been adapted to add `.length` accordingly, it still works correctly.
How about the incorrect example? The one we expected to fail?

```
In file included from /usr/include/c++/15.2.1/cassert:46,
                 from [...]/analog-literals/tutorial.cpp:4:
[...]/analog-literals/tutorial.cpp: In function 'int main()':
[...]/analog-literals/tutorial.cpp:113:34: error: no match for 'operator==' (operand types are 'const mp_units::quantity<mp_units::reference<mp_units::isq::area, mp_units::derived_unit<mp_units::power<mp_units::si::metre, 2> > >()>' and 'mp_units::quantity<mp_units::reference<mp_units::isq::length, mp_units::si::metre>()>')
  109 | assert( ( o-------------o
      |         ~~~~~~~~~~~~~~~~~         
  110 |           |             !
      |           ~~~~~~~~~~~~~~~         
  111 |           !             !
      |           ~~~~~~~~~~~~~~~         
  112 |           !             !
      |           ~~~~~~~~~~~~~~~         
  113 |           o-------------o ).area == 2 * (I-------------I).length );
      |           ~~~~~~~~~~~~~~~~~~~~~~ ^~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      |                             |         |
      |                             |         quantity<mp_units::reference<mp_units::isq::length, mp_units::si::metre>()>
      |                             quantity<mp_units::reference<mp_units::isq::area, mp_units::derived_unit<mp_units::power<mp_units::si::metre, 2> > >()>
[...]/analog-literals/tutorial.cpp:113:34: note: there are 3 candidates

... 170 more lines ...
```

That's a mouthful for sure. Especially with the 170 unshown lines.
Keep in mind that GCC has colored diagnostics that I couldn't reproduce here, which actually make the whole thing a bit more palatable.

Anyway, the good news is: the library *does* catch the incorrect comparison of a length with an area at compile time.
We are now mostly safe from a simple dimensional analysis point of view. Can we do better still?

## Quantity kind safety

The [International System of Quantities (ISQ)][isq] goes further than just defining quantities: it defines *quantity kinds*.
An image is sometimes worth a thousand words. Here is the hierarchy of ISQ quantity kinds related to length:

![ISQ hierarchy of different kinds of lengths]({{ site.baseurl }}/assets/images/TSB011/kinds-of-lengths.svg){:.centered}

Quantity kinds allow to go beyond the notions dimension and quantity, and to signal that a specific kind of a given quantity is expected.
Based on the diagram above, a function that expects a quantity of *altitude* kind would accept a quantity of *height* as input, but not a *wavelength* for example.
That additional level safety can be very valuable when working with highly domain-specific code.

Let's try to find quantity kinds that could apply to our `cuboid`:
* `width` can be modelled with `isq::width`.
* `height` can be modelled with `isq::height`.
* `depth` can be modelled with... `isq::length` since the ISQ does not define a specific quantity kind for depth.

This specific problem was actually already encountered by Mateusz Pusz and dubbed the ["3D box problem"][mp-units-box-ambiguity].
Interestingly his model does not have "depth" field but a "length" one instead, despite a box and a cuboid being philosophically similar.
To circumvent the issue, he defines a new `horizontal_length` quantity kind as follows:

```cpp
inline constexpr struct horizontal_length final : quantity_spec<isq::length> {} horizontal_length;
```

We could similarly define a `depth` quantity kind based on `isq::length`.
That said, going down that rabbit hole might not be as good an idea as it originally seemed, for reasons entirely unrelated to the lack of a dedicated ISQ quantity kind.
To understand why, let's look at the following set of additional functions provided by the original analog literals library:

```cpp
template <uint x, uint y, uint z>
rectangle<x, y> front(cuboid<x, y, z>);
template <uint x, uint y, uint z>
rectangle<z, y> side(cuboid<x, y, z>);
template <uint x, uint y, uint z>
rectangle<x, z> top(cuboid<x, y, z>);
```

All three accept a `cuboid` and return a `rectangle`. If we tried to make *those* rectangles quantity kind-safe though, what should they return?
* `front` would return a `isq::width * isq::height`.
* `side` would return a `depth * isq::height`.
* `top` would return a `isq::width * depth`.

That would render the design much more complicated, for dubious added value when we don't know the application domain.
Additional question: what should be the quantity kinds of the sides of the following literal?

```cpp
auto lit = ( o-------------o
             |             !
             !             !
             !             !
             o-------------o );
```

Going further, should `I-------I` be a width? Should it be a horizontal length? If so, how can we represent a raw height with analog literals?

All in all, my gut feeling there is that quantity kinds are a pretty cool tool, which _can_ improve your typing safety in specific scenarios.
However analog literals are _not_ specific enough, and going besides `isq::length` seems like an overreach if we don't know what they will be used for.

**Quantity kinds should be as specific as the application domain requires them to be, and no more than that.**

## Conclusion

I am honestly excited about the perspective of getting [SI units][si] and ISQ quantities as vocabulary types in the C++ standard library in the near future.
Analog literals were a fun playground to think about what it means to be quantity-safe, and what are the challenges of providing useful quantity kinds.

I think that mp-units does lots of things correctly, and salute the effort to implement all cross-cutting concerns of the domain while keeping reasonable ergonomics.
Metrology is not simple, and we should not pretend that it is; the challenges faced in this blog post are barely scratching the surface.

That first hands-on experience, however small, highlighted the following small frustration points:
* The only issue I could fully solve without overthinking it was dimensional analysis. I could not really benefit from quantity kinds because analog literals are not domain-specific enough for them to be consensually useful.
* Getting an instinct of correct default for a quantity type is not easy: I wasn't immediately sure whether I needed to store `quantity<isq::area>`, `quantity<isq::area[pow<2>(isq::meter)]>`, `quantity<isq::area[m*m]>`, etc. Which ones worked or not sometimes felt like flipping a coin, though I guess it gets better with more experience.
* Error messages are okay, but still much longer than anticipated.
* I took the L when trying to use the `mp_units::si::unit_symbols` and `analog_literals::symbols` namespaces together because both use `L` as a symbol (mp-units uses it for litres, which is notably _not_ an SI unit, but the library somehow imports the `non_si::unit_symbols` namespace into the `si::units_symbols` one[^3]).

All in all it was a fun experiment, and I loved shining some light again on that classic piece of cursed C++ code.
Though the fun wasn't the only thing I felt over the course of it: it left me with an odd aftertaste, a sentiment of a project remained unfinished, maybe unloved enough.
As a community, we need more curious nerds to improve the area of analog literals, and help shape a brighter future for what remains to that day a thought-provoking feature.

## Notes

  [^1]: [Tweaking Analog Literals][tweaking-analog-literals], 2009-08-29
  
  [^2]: [H-J-Granger/analog-literals][h-j-granger-analog-literals], 2024

  [^3]: Update 2026-06-28: I discovered in the meantime that the `non_si` namespace corresponds to a [specific list of commmon units][non-si-units] described as "accepted for use with the SI". However it seems that the "accepted" term was recently dropped and BIPM only mentions them as "non-SI units" that are "important to recall".

  
  [analog-literals]: http://www.eelis.net/C++/analogliterals.xhtml
  [h-j-granger-analog-literals]: https://github.com/H-J-Granger/analog-literals
  [iso-iec-80000]: https://en.wikipedia.org/wiki/ISO/IEC_80000
  [isq]: https://en.wikipedia.org/wiki/International_System_of_Quantities
  [max-munch]: https://en.wikipedia.org/wiki/Maximal_munch
  [mp-units]: https://mpusz.github.io/mp-units/latest/
  [mp-units-box-ambiguity]: https://mpusz.github.io/mp-units/latest/blog/2024/11/11/international-system-of-quantities-isq-part-6---challenges/?h=box#ambiguity
  [non-si-units]: https://en.wikipedia.org/wiki/International_System_of_Units#Non-SI_units
  [si]: https://en.wikipedia.org/wiki/International_System_of_Units
  [tweaking-analog-literals]: http://blog.hostilefork.com/tweaking-analog-literals/
