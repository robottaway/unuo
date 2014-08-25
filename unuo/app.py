#!/usr/bin/env python

from unuo.factories import default_factory

app = None


if __name__ == '__main__':
    app = default_factory()
    app.run()
