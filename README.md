---------------------------

# <a name="start"></a> Title of Story #

Intro text

## <a name="1stScene"></a> First Scene

Girl in distance says hello

* [look](#a)

* [wave](#b)

* [kick](#c)

## <a name="a"></a> choice a

She has a shiny fur. She a furry!

THE END

## <a name="b"></a> First Scene

She waves back

THE END

## <a name="c"></a> First Scene

She blocks your kick, and kills you with a single punch to the face. Your mouth is full of fur.

THE END

[Restart](#start)

-------------

Update: Due to a new change in pandoc, this works:

# A random story {#start}

Intro text here.

[Walk Forward](#1stScene)

## First Scene {#1stScene}

Girl in distance says hello

* [look](#a) * [wave](#b) * [kick](#c)

## choice a - touch the stranger {#a}

She has a shiny fur. She is a furry!

THE END

* [Restart](#start)

## choice b - wave at the stranger{#b}

She waves back

THE END

* [Restart](#start)

## choice c - kick the stranger{#c}

She blocks your kick, and kills you with a single punch to the face. Your mouth is full of fur.

THE END

* [Restart](#start)
