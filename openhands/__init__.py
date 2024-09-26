def get_version():
    try:
        from importlib.metadata import PackageNotFoundError, version

        try:
            return version('openhands-ai-test')
        except PackageNotFoundError:
            pass
    except ImportError:
        pass

    try:
        from pkg_resources import DistributionNotFound, get_distribution

        try:
            return get_distribution('openhands-ai-test').version
        except DistributionNotFound:
            pass
    except ImportError:
        pass

    return 'unknown'


try:
    __version__ = get_version()
except Exception:
    __version__ = 'unknown'
