try:
    __path__ = __import__('pkgutil').extend_path(__path__, __name__)
except ImportError:
    __import__('pkg_resources').declare_namespace(__name__)
