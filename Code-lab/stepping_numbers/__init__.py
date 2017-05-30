def profile(func):
    import cProfile
    from os import path
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        try:
            profiler.enable()
            result = func(*args, **kwargs)
            profiler.disable()
            return result
        finally:
            filename = path.join(path.dirname(__file__), f'{func.__qualname__}.pstat')
            profiler.dump_stats(filename)

    return wrapper
