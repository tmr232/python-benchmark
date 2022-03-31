class TestCall:
    """Call global or local functions"""

    def test_call_local(self, benchmark):
        """Calls a local function"""
        def run(min=min):
            min(1, 2)
        benchmark(run)

    def test_call_builtin(self, benchmark):
        """Call builtin function"""
        def run():
            min(1, 2)
        benchmark(run)