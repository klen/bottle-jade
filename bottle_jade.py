# Package information
# ===================
from pyjade.ext.html import pyjade, Compiler, local_context_manager
from pyjade.nodes import Extends, CodeBlock
from os import path as op


__version__ = "0.2.1"
__project__ = "bottle-jade"
__author__ = "Kirill Klenov <horneds@gmail.com>"
__license__ = "MIT"


class ExtendCompiler(Compiler):

    def __init__(self, node, env, **options):
        super(ExtendCompiler, self).__init__(node, **options)
        self.env = env
        self.blocks = {node.name: node for node in self.node.nodes if isinstance(node, CodeBlock)}
        while self.node.nodes and isinstance(self.node.nodes[0], Extends):
            compiler = self.env.get_template(self.node.nodes[0].path)
            self.node = compiler.node
            for cblock in compiler.blocks.values():
                if cblock.name in self.blocks:
                    sblock = self.blocks[cblock.name]
                    if sblock.mode == 'prepend':
                        sblock.nodes = sblock.nodes + cblock.nodes
                    elif sblock.mode == 'append':
                        sblock.nodes = cblock.nodes + sblock.nodes
                else:
                    self.blocks[cblock.name] = cblock

    def visitCodeBlock(self, block):
        block = self.blocks.get(block.name, block)
        for node in block.nodes:
            self.visitNode(node)

    def visitInclude(self, node):
        compiler = self.env.get_template(node.path)
        self.visit(compiler.node)


class JadePlugin(object):

    """ The class is used to control the pyjade integration to Flask application. """

    api = 2
    name = 'jade'
    defaults = dict(
        cache_size=100,
        encoding='UTF-8',
        pretty=True,
        template_folder='templates',
    )

    def __init__(self, **options):
        from bottle import request
        self.app = None
        self.env = Environment()
        self.defaults.update(options)
        self.providers = [lambda: {'app': self.app, 'request': request}]

    def setup(self, app):
        self.app = app

        app.config.setdefault('JADE_CACHE_SIZE', self.defaults['cache_size'])
        app.config.setdefault('JADE_PRETTY', self.defaults['pretty'])
        app.config.setdefault('JADE_TEMPLATE_FOLDER', self.defaults['template_folder'])
        app.config.setdefault('JADE_ENCODING', self.defaults['encoding'])

        self.env = Environment(
            cache_size=app.config['JADE_CACHE_SIZE'],
            debug=app.config.get('DEBUG', False),
            pretty=app.config['JADE_PRETTY'],
            encoding=app.config['JADE_ENCODING'],
            template_folder=app.config['JADE_TEMPLATE_FOLDER'],
        )

    @staticmethod
    def apply(callback, route):
        return callback

    def ctx_provider(self, func):
        """ Decorator for adding a context provider.

        ::
            @jade.ctx_provider
            def my_context():
                return {...}
        """
        self.providers.append(func)
        return func

    def render(self, path, **context):
        ctx = dict()
        for provider in self.providers:
            ctx.update(provider())
        ctx.update(context)
        template = self.env.get_template(path)
        return self.env.render(template, **ctx)

    def view(self, template):
        def decorator(callback):
            def wrapper(*args, **kwargs):
                context = callback(*args, **kwargs)
                tmpl = template
                if callable(template):
                    tmpl = template()
                return self.render(tmpl, **context)
            return wrapper
        return decorator


class Environment(object):

    """ Template's environment. """

    cache = {}
    cache_index = []

    def __init__(self, **options):
        self.options = options

    @classmethod
    def clean(cls):
        cls.cache = {}
        cls.cache_index = []

    def load_template(self, path):
        if not path.startswith('/'):
            path = op.join(self.options['template_folder'], path)

        with open(path, 'rb') as f:
            source = f.read().decode(self.options['encoding'])

        return ExtendCompiler(
            pyjade.parser.Parser(source).parse(), pretty=self.options['pretty'],
            env=self, compileDebug=True
        )

    def cache_template(self, path):
        compiler = self.load_template(path)
        if path not in self.cache_index:
            self.cache_index.append(path)
        self.cache[path] = compiler
        if len(self.cache_index) > self.options['cache_size']:
            self.cache.pop(self.cache_index.pop(0))
        return compiler

    def get_template(self, path):
        """ Load and compile template. """

        if self.options['debug'] and self.options['cache_size']:
            return self.cache.get(path, self.cache_template(path))
        return self.load_template(path)

    @staticmethod
    def render(compiler, **context):
        """ Render the template with the context. """
        with local_context_manager(compiler, context):
            return compiler.compile()

# pylama:ignore=E1002,E0203
